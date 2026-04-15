# 学生答题系统

> 基于 Flask + AI 的智能作业批改平台，支持实时流式批改和队列管理

## 功能特点

- **用户认证**：学号密码登录，支持记住我功能
- **作业上传**：支持拖拽上传，实时预览，最大 16MB
- **AI 批改**：集成 Infini-AI API，支持流式实时输出
- **队列管理**：智能批改队列，支持并发控制
- **Token 控制**：每日 API 调用限额管理
- **响应式设计**：Bootstrap 5 美观界面，适配各种设备
- **实时推送**：SSE 技术实现批改结果实时显示
- **管理员功能**：支持删除作业、查看队列状态

## 技术架构

### 后端技术栈
- **Flask 3.0.0**：轻量级 Web 框架
- **SQLite**：嵌入式数据库
- **Threading**：多线程队列处理
- **Requests**：HTTP 请求库（AI API 调用）
- **Pillow**：图像处理

### 前端技术栈
- **Bootstrap 5**：响应式 UI 框架
- **Server-Sent Events (SSE)**：实时数据推送
- **原生 JavaScript**：无依赖的轻量级实现

### AI 集成
- **Infini-AI API**：OpenAI 兼容接口
- **流式输出**：实时显示 AI 生成过程
- **自动重试**：网络异常自动重试（最多 3 次）

## 项目结构

```
学生答题/
├── docs/                   # 文档目录
│   ├── 宝塔面板部署.md
│   └── AGENTS.md
├── data/                   # 数据目录
│   └── database.db         # SQLite 数据库
├── src/                    # 源代码目录
│   ├── app.py              # Flask 主程序
│   ├── config.py           # 配置文件
│   ├── database.py         # 数据库初始化
│   ├── models/             # 数据模型
│   ├── routes/             # 路由
│   └── services/           # 业务逻辑
├── static/                 # 静态文件
│   ├── css/
│   │   └── theme.css
│   └── icons/
├── templates/              # 模板文件
│   ├── login.html
│   ├── dashboard.html
│   ├── detail.html
│   ├── upload.html
│   └── queue_status.html
├── uploads/                # 上传文件目录
├── scripts/                # 脚本目录
│   └── start.bat           # Windows 启动脚本
├── tests/                  # 测试目录
├── .env                    # 环境变量
├── .env.example            # 环境变量示例
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt        # Python 依赖
└── run.py                  # 入口文件
```

## 快速开始

### 环境要求
- Python 3.8 或更高版本
- pip 包管理器

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd 学生答题
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
cp .env.example .env
```

编辑 `.env` 文件，配置以下参数：
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
AI_API_KEY=your-ai-api-key
AI_BASE_URL=https://api.example.com
AI_MODEL=gpt-4-vision-preview
```

4. **初始化数据库**
```bash
python src/database.py
```

5. **启动服务器**
```bash
python run.py
```

或使用 Windows 快速启动脚本：
```bash
scripts\start.bat
```

6. **访问系统**
浏览器打开：http://localhost:5000

### 默认账号
| 角色 | 学号 | 密码 |
|------|------|------|
| 管理员 | admin | zzl2008 |
| 学生 | 2024001 | 123456 |
| 学生 | 2024002 | 123456 |
| 学生 | 2024003 | 123456 |
| 学生 | 2024004 | 123456 |

## 配置说明

### 基础配置 (src/config.py)

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `SECRET_KEY` | Flask 会话密钥 | 需修改 |
| `DEBUG` | 调试模式 | True |
| `DATABASE` | 数据库文件名 | ../data/database.db |
| `UPLOAD_FOLDER` | 上传目录 | ../uploads |
| `MAX_CONTENT_LENGTH` | 最大上传大小 | 16MB |
| `ALLOWED_EXTENSIONS` | 允许的文件格式 | png, jpg, jpeg, gif |

### AI 批改配置

系统支持 OpenAI 兼容的 API 接口，如：
- Infini-AI
- OpenAI GPT-4 Vision
- 百度文心一言
- 阿里通义千问

在 `.env` 文件中配置：
```env
AI_API_KEY=your-api-key
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4-vision-preview
```

### Token 控制

- **每日限额**：10,000 tokens
- **自动重置**：每天 00:00 自动重置
- **超额处理**：达到限额后自动暂停批改，提示用户明日再试

## 使用说明

### 上传作业流程

1. 登录系统
2. 点击"上传新作业"
3. 输入作业标题
4. 选择或拖拽图片文件（支持 JPG/PNG/GIF）
5. 点击"提交作业"
6. 系统自动加入批改队列
7. 实时查看 AI 批改结果（流式输出）

### 查看批改结果

1. 在作业列表点击任意作业卡片
2. 左侧显示作业原图
3. 右侧显示 AI 批改结果
4. 包含：题目判断、正确答案、解析、得分

### 队列状态监控

- 访问 `/queue-status` 查看实时队列状态
- 显示：队列长度、当前任务、已完成数量、Token 使用情况

### 管理员功能

- **删除作业**：仅管理员可删除任意作业
- **查看队列**：监控所有批改任务状态

## 核心架构说明

### AI 批改队列系统

系统采用生产者-消费者模式处理批改任务：

1. **任务提交**：用户上传作业后，任务加入队列
2. **后台处理**：独立线程持续处理队列中的任务
3. **流式输出**：AI 结果实时推送到前端
4. **状态管理**：pending → processing → completed/failed

### 实时推送机制

使用 Server-Sent Events (SSE) 实现：
- 每 0.3 秒检查一次状态变化
- 内存缓存 + 数据库双重存储
- 仅推送变化部分，减少网络流量

### 数据库设计

**students 表**
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    student_id TEXT UNIQUE,
    password TEXT,
    name TEXT,
    created_at TIMESTAMP
)
```

**assignments 表**
```sql
CREATE TABLE assignments (
    id INTEGER PRIMARY KEY,
    student_id TEXT,
    title TEXT,
    image_path TEXT,
    ai_result TEXT,
    status TEXT,  -- queued/processing/completed/failed
    upload_time TIMESTAMP
)
```

**ai_grading_logs 表**
```sql
CREATE TABLE ai_grading_logs (
    id INTEGER PRIMARY KEY,
    assignment_id INTEGER,
    token_used INTEGER,
    created_at TIMESTAMP
)
```

## 常见问题

### Q: 上传图片失败？
**A:** 检查以下几点：
- 图片格式是否为 JPG/PNG/GIF
- 图片大小是否超过 16MB
- `uploads` 文件夹是否有写入权限
- 浏览器控制台是否有错误信息

### Q: AI 批改不工作？
**A:** 
- 检查 `.env` 中的 API Key 配置是否正确
- 确认 API 服务是否可用
- 检查网络连接
- 查看服务器控制台错误日志
- 确认 Token 限额是否已用完

### Q: 如何添加新学生？
**A:** 
方法 1：直接操作数据库
```bash
sqlite3 database.db
INSERT INTO students (student_id, password, name) 
VALUES ('2024005', '123456', '新学生');
```

方法 2：修改 `src/database.py` 中的示例数据，重新运行初始化

### Q: 如何修改每日 Token 限额？
**A:** 编辑 `src/app.py` 第 36 行：
```python
self.max_daily_tokens = 10000  # 修改为所需值
```

### Q: 批改速度很慢怎么办？
**A:** 
- 检查 API 服务的响应速度
- 考虑使用更快的 AI 模型
- 优化网络连接
- 减少并发任务数量

## 部署指南

### 本地部署
参考上述"快速开始"章节

### 宝塔面板部署
详细步骤请参考 `docs/宝塔面板部署.md`

### Docker 部署（可选）
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

## 安全建议

- **修改 SECRET_KEY**：生产环境必须使用随机密钥
- **密码加密**：当前使用明文存储，建议使用 bcrypt 加密
- **HTTPS**：生产环境建议启用 HTTPS
- **文件验证**：加强上传文件的类型和内容验证
- **API 密钥保护**：妥善保管 API Key，不要提交到版本控制

## 性能优化

- 使用连接池管理数据库连接
- 添加 Redis 缓存队列状态
- 图片上传前进行压缩
- 使用 CDN 加速静态资源

## 贡献指南

欢迎提交 Issue 和 Pull Request

## 许可证

本项目仅供学习交流使用

## 技术支持

如有问题，请检查：
1. Python 版本 >= 3.8
2. 所有依赖已正确安装
3. 端口 5000 未被占用
4. 查看控制台错误日志
5. 检查 API 服务状态

---

**祝使用愉快！**
