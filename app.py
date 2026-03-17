"""
Flask 主程序 - 学生答题系统
包含 AI 批改排队系统和 token 控制
"""
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
import sqlite3
import os
import uuid
from datetime import datetime, timedelta
from functools import wraps
import config
import threading
import time
from queue import Queue
import json

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ==================== AI 批改排队系统 ====================

class AIGradingQueue:
    """AI 批改队列管理器"""
    
    def __init__(self):
        self.queue = Queue()
        self.processing = False
        self.current_task = None
        self.completed_count = 0
        self.token_usage = 0
        self.max_daily_tokens = 10000  # 每日 token 限制
        self.daily_token_reset_time = None
        self.lock = threading.Lock()
        
    def add_task(self, assignment_id, image_path, title):
        """添加批改任务到队列"""
        task = {
            'assignment_id': assignment_id,
            'image_path': image_path,
            'title': title,
            'status': 'pending',
            'created_at': datetime.now(),
            'started_at': None,
            'completed_at': None,
            'result': None,
            'token_used': 0
        }
        self.queue.put(task)
        # 估算队列长度（近似值）
        return self.queue.qsize()
    
    def get_queue_status(self):
        """获取队列状态（从数据库读取真实统计）"""
        queue_list = list(self.queue.queue)
        position = 0
        for i, task in enumerate(queue_list):
            if task['assignment_id'] == self.current_task.get('assignment_id') if self.current_task else False:
                position = i + 1
                break
        
        # 从数据库读取今日 token 使用量
        conn = get_db_connection()
        cursor = conn.cursor()
        today = datetime.now().date()
        cursor.execute('''
            SELECT SUM(token_used) as total_tokens 
            FROM ai_grading_logs 
            WHERE DATE(created_at) = ?
        ''', (today.isoformat(),))
        result = cursor.fetchone()
        db_token_usage = result['total_tokens'] if result and result['total_tokens'] else 0
        
        # 读取今日已完成数量
        cursor.execute('''
            SELECT COUNT(*) as count 
            FROM assignments 
            WHERE status = 'completed' 
            AND DATE(upload_time) = ?
        ''', (today.isoformat(),))
        completed_result = cursor.fetchone()
        completed_today = completed_result['count'] if completed_result else 0
        
        conn.close()
        
        return {
            'queue_length': len(queue_list),
            'processing': self.processing,
            'current_task': self.current_task,
            'position': position,
            'completed_today': completed_today,
            'token_usage': db_token_usage,
            'token_limit': self.max_daily_tokens
        }
    
    def check_token_limit(self):
        """检查 token 限制"""
        now = datetime.now()
        
        # 每天重置 token 计数
        if self.daily_token_reset_time is None or now.date() > self.daily_token_reset_time.date():
            self.token_usage = 0
            self.daily_token_reset_time = now
            self.completed_count = 0
        
        return self.token_usage < self.max_daily_tokens
    
    def process_queue(self):
        """处理队列中的任务（支持实时流式推送）"""
        while True:
            if not self.queue.empty() and not self.processing:
                task = self.queue.get()
                
                with self.lock:
                    self.processing = True
                    self.current_task = task
                    task['started_at'] = datetime.now()
                    task['status'] = 'processing'  # 设置为处理中状态
                
                # 更新数据库状态为 processing
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE assignments SET status = ? WHERE id = ?
                ''', ('processing', task['assignment_id']))
                conn.commit()
                conn.close()
                
                # 检查 token 限制
                if not self.check_token_limit():
                    task['status'] = 'failed'
                    task['result'] = '今日 AI 批改次数已达上限，请明日再试'
                    task['completed_at'] = datetime.now()
                    self._update_database(task)
                    with self.lock:
                        self.processing = False
                        self.current_task = None
                    continue
                
                # 执行 AI 批改并实时推送结果
                try:
                    # 使用生成器接收流式结果
                    ai_result_stream = get_ai_result_stream(task['image_path'], task['title'])
                    
                    full_result = ""
                    for chunk in ai_result_stream:
                        if chunk:
                            full_result += chunk
                            # 实时更新数据库中的部分结果
                            task['result'] = full_result
                            self._update_partial_result(task)
                    
                    task['status'] = 'completed'
                    task['result'] = full_result
                    task['token_used'] = len(task['title']) * 100 + len(full_result) * 0.5  # 估算 token 使用
                    
                    with self.lock:
                        self.token_usage += task['token_used']
                        self.completed_count += 1
                    
                except Exception as e:
                    task['status'] = 'failed'
                    task['result'] = f'批改失败：{str(e)}'
                
                task['completed_at'] = datetime.now()
                self._update_database(task)
                
                with self.lock:
                    self.processing = False
                    self.current_task = None
            
            time.sleep(1)  # 每秒检查一次
    
    def _update_partial_result(self, task):
        """更新部分批改结果到数据库（用于流式输出）"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE assignments 
            SET ai_result = ?, status = ?
            WHERE id = ?
        ''', (task['result'], 'processing', task['assignment_id']))
        conn.commit()
        conn.close()
    
    def _update_database(self, task):
        """更新数据库中的批改结果"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 更新作业状态
        cursor.execute('''
            UPDATE assignments 
            SET ai_result = ?, status = ?
            WHERE id = ?
        ''', (task['result'], task['status'], task['assignment_id']))
        
        # 如果是完成状态，记录 token 使用量
        if task.get('token_used') and task['status'] == 'completed':
            cursor.execute('''
                INSERT INTO ai_grading_logs (assignment_id, token_used)
                VALUES (?, ?)
            ''', (task['assignment_id'], task['token_used']))
        
        conn.commit()
        conn.close()

# 初始化 AI 批改队列
ai_queue = AIGradingQueue()

# 启动队列处理线程
queue_thread = threading.Thread(target=ai_queue.process_queue, daemon=True)
queue_thread.start()

# ==================== 辅助函数 ====================

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'student_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_ai_result_stream(image_path, title):
    """
    调用 Infini-AI API 进行批改 - 生成器版本（实时返回每个字）
    """
    import requests
    import base64
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    
    # 检查是否配置了 AI_API_KEY
    if not config.AI_API_KEY or not config.AI_BASE_URL or not config.AI_MODEL:
        raise ValueError("AI 配置未设置，请在 .env 文件中配置 AI_API_KEY、AI_BASE_URL 和 AI_MODEL")
    
    try:
        # 读取图片并转为 base64
        with open(image_path, 'rb') as f:
            image_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        # 构建提示词
        prompt = f"""请批改这份学生作业：{title}
请识别图片中的题目和学生答案，判断每道题是否正确，并给出：
1. 每道题的判断结果 (正确/错误)
2. 错误题目的正确答案（包含详细解题步骤）
3. 总体评价
4. 打分 (0-100)

要求：
- 使用纯文本格式，不要使用任何 Markdown 语法（不要用 **、#、` 等符号）
- 使用简洁清晰的语言
- 换行分隔不同部分
- 可以使用简单的符号如 ✓ ✗ → 等
- **重要**：数学公式必须使用 LaTeX 格式，用 $...$ 包裹（行内公式）或 $$...$$ 包裹（独立公式）
- **重要**：不要省略计算步骤，要完整展示解题过程

（这都是）示例格式："
【批改结果】

第 1 题：正确 ✓
第 2 题：错误 ✗ 
你的答案：A
正确答案：B
解析：根据公式 $E = mc^2$，其中 $m$ 是质量，$c$ 是光速。
计算过程：
$$F = ma = 5 \times 9.8 = 49N$$
所以答案是 49N。

第 3 题：正确 ✓"

总体评价：完成良好，注意计算准确性。
得分：「实际得分」"""
        
        # 调用 AI API
        headers = {
            'Authorization': f'Bearer {config.AI_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "model": config.AI_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "stream": True  # 启用流式输出
        }
        
        # 创建会话并配置重试策略
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        
        # 增加超时时间并启用流式接收
        response = session.post(
            f"{config.AI_BASE_URL}/chat/completions",
            json=payload,
            headers=headers,
            timeout=(10, 180),  # 连接超时 10 秒，读取超时 180 秒
            stream=True
        )
        
        if response.status_code == 200:
            # 流式接收响应 - 实时 yield 每个字
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data: '):
                        data_str = decoded_line[6:]
                        if data_str.strip() == '[DONE]':
                            break
                        try:
                            import json
                            data = json.loads(data_str)
                            if 'choices' in data and len(data['choices']) > 0:
                                delta = data['choices'][0].get('delta', {})
                                content = delta.get('content', '')
                                if content:
                                    # 实时返回每个字符
                                    yield content
                        except json.JSONDecodeError:
                            continue
        else:
            error_msg = f"API 请求失败：HTTP {response.status_code}"
            print(f"Error: {error_msg}")
            print(f"Response: {response.text}")
            raise Exception(error_msg)
            
    except Exception as e:
        print(f"AI 调用异常：{str(e)}")
        raise

def get_ai_result(image_path, title):
    """
    调用 Infini-AI API 进行批改（兼容旧版本，内部调用流式版本）
    """
    full_result = ""
    try:
        for chunk in get_ai_result_stream(image_path, title):
            full_result += chunk
        
        return {
            'success': True,
            'result': full_result,
            'score': None,
            'provider': 'Infini-AI'
        }
    except Exception as e:
        return {
            'success': False,
            'result': f'AI 批改异常：{str(e)}',
            'score': None,
            'provider': 'Infini-AI'
        }

# ==================== 路由处理 ====================

@app.route('/')
def index():
    """首页，重定向到登录页或仪表盘"""
    if 'student_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM students WHERE student_id = ? AND password = ?',
            (student_id, password)
        )
        student = cursor.fetchone()
        conn.close()
        
        if student:
            session['student_id'] = student['student_id']
            session['student_name'] = student['name']
            session['is_admin'] = (student_id == 'admin' and password == 'zzl2008')  # 管理员专属密码
            
            # 设置会话过期时间
            if remember:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=7)
            
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='学号或密码错误')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """登出"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """仪表盘 - 显示所有作业"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取当前学生的所有作业
    cursor.execute('''
        SELECT * FROM assignments 
        WHERE student_id = ? 
        ORDER BY upload_time DESC
    ''', (session['student_id'],))
    
    assignments = cursor.fetchall()
    conn.close()
    
    return render_template('dashboard.html', assignments=assignments)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """上传作业"""
    if request.method == 'POST':
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400
        
        file = request.files['file']
        title = request.form.get('title', '未命名作业')
        
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        if file and allowed_file(file.filename):
            # 生成唯一文件名
            extension = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4()}.{extension}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # 保存文件
            file.save(filepath)
            
            # 保存到数据库（初始状态为排队中）
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO assignments (student_id, title, image_path, ai_result, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (session['student_id'], title, filepath, '正在排队等待批改...', 'queued'))
            
            assignment_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # 添加到 AI 批改队列
            queue_position = ai_queue.add_task(assignment_id, filepath, title)
            
            return jsonify({
                'success': True,
                'message': '已加入批改队列',
                'assignment_id': assignment_id,
                'queue_position': queue_position
            })
        
        return jsonify({'error': '不支持的文件类型'}), 400
    
    return render_template('upload.html')

@app.route('/assignment/<int:assignment_id>')
@login_required
def assignment_detail(assignment_id):
    """作业详情页面"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM assignments 
        WHERE id = ? AND student_id = ?
    ''', (assignment_id, session['student_id']))
    
    assignment = cursor.fetchone()
    conn.close()
    
    if not assignment:
        return '作业不存在', 404
    
    return render_template('detail.html', assignment=assignment)

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    """提供上传文件的访问"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<int:assignment_id>', methods=['POST'])
@login_required
def delete_assignment(assignment_id):
    """删除作业（仅管理员）"""
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': '权限不足'}), 403
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取作业信息
        cursor.execute('SELECT image_path FROM assignments WHERE id = ?', (assignment_id,))
        assignment = cursor.fetchone()
        
        if assignment and assignment['image_path']:
            # 删除图片文件
            try:
                os.remove(assignment['image_path'])
            except FileNotFoundError:
                pass
        
        # 删除数据库记录
        cursor.execute('DELETE FROM assignments WHERE id = ?', (assignment_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': '删除成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/stream-ai-result/<int:assignment_id>')
@login_required
def stream_ai_result(assignment_id):
    """流式输出 AI 批改结果（SSE）"""
    from flask import Response
    
    def generate():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        while True:
            # 查询作业状态和结果
            cursor.execute('''
                SELECT status, ai_result FROM assignments WHERE id = ?
            ''', (assignment_id,))
            assignment = cursor.fetchone()
            
            if not assignment:
                yield f"data: {{\"error\": \"作业不存在\"}}\n\n"
                break
            
            # 发送当前状态
            result_str = assignment['ai_result'] if assignment['ai_result'] else 'null'
            import json
            yield f"data: {{\"status\": \"{assignment['status']}\", \"result\": {json.dumps(result_str)}}}\n\n"
            
            # 如果已完成或失败，停止推送
            if assignment['status'] in ['completed', 'failed']:
                break
            
            # 每秒检查一次
            time.sleep(1)
        
        conn.close()
    
    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
    )

@app.route('/queue-status')
@login_required
def queue_status():
    """查看 AI 批改队列状态"""
    status = ai_queue.get_queue_status()
    return render_template('queue_status.html', queue_info=status)

@app.route('/api/queue-status')
@login_required
def api_queue_status():
    """API: 获取队列状态"""
    status = ai_queue.get_queue_status()
    return jsonify(status)

# ==================== 启动应用 ====================

if __name__ == '__main__':
    # 初始化数据库
    if not os.path.exists('database.db'):
        import database
        database.init_database()
    
    print("=" * 50)
    print("学生答题系统启动成功！")
    print("访问地址：http://localhost:5000")
    print("示例账号:")
    print("  学号：2024001 密码：123456")
    print("  学号：2024002 密码：123456")
    print("AI 批改排队系统已启用")
    print("每日 Token 限制：10000")
    print("=" * 50)
    
    app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)
