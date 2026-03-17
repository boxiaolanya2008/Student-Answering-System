# 学生答题系统

一个基于 Python Flask 的学生答题系统，支持图片上传和 AI 自动批改功能。

## 🎯 功能特点

- ✅ **用户登录**：学号 + 密码验证
- ✅ **作业管理**：查看、上传作业
- ✅ **图片上传**：支持拖拽上传，实时预览
- ✅ **AI 批改**：集成百度文心一言 API（可选）
- ✅ **响应式设计**：Bootstrap 5 美观界面

## 📁 项目结构

```
学生答题/
├── app.py              # Flask 主程序
├── config.py           # 配置文件
├── database.py         # 数据库初始化
├── database.db         # SQLite 数据库 (运行后生成)
├── requirements.txt    # Python 依赖
├── uploads/            # 图片上传目录
└── templates/          # HTML 模板
    ├── login.html      # 登录页面
    ├── dashboard.html  # 作业列表
    ├── detail.html     # 作业详情
    └── upload.html     # 上传页面
```

## 🚀 快速开始

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python database.py
```

### 3. 启动服务器

```bash
python app.py
```

### 4. 访问系统

浏览器打开：http://localhost:5000

**示例账号：**
- 学号：2024001
- 密码：123456

其他可用账号：2024002, 2024003, 2024004（密码都是 123456）

## ⚙️ 配置说明

### 基础配置 (config.py)

```python
SECRET_KEY = 'your-secret-key-here'  # 修改为随机密钥
DEBUG = True  # 开发环境设为 True
DATABASE = 'database.db'
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大上传 16MB
```

### AI 批改配置 (可选)

如需启用 AI 批改功能，需要申请百度文心一言 API：

1. 访问 [百度智能云](https://cloud.baidu.com/product/wenxinworkshop)
2. 注册并创建应用获取 API Key 和 Secret Key
3. 在 `config.py` 中配置：

```python
BAIDU_API_KEY = '你的 API Key'
BAIDU_SECRET_KEY = '你的 Secret Key'
BAIDU_AI_MODEL = 'ernie-bot-4'  # 或其他可用模型
```

**注意**：未配置 AI 时，系统会使用模拟的批改结果进行演示。

## 📝 使用说明

### 上传作业

1. 登录后点击"➕ 上传新作业"
2. 输入作业标题
3. 选择或拖拽图片文件
4. 点击"✅ 提交作业"
5. 系统会自动调用 AI 批改（如已配置）

### 查看批改

1. 在作业列表点击任意作业卡片
2. 左侧显示作业图片
3. 右侧显示 AI 批改结果
4. 可查看详细信息（时间、状态等）

## 🔧 常见问题

### Q: 上传图片失败？
A: 检查以下几点：
- 图片格式是否为 JPG/PNG/GIF
- 图片大小是否超过 16MB
- `uploads` 文件夹是否有写入权限

### Q: AI 批改不工作？
A: 
- 检查 `config.py` 中的 API Key 配置
- 确保有百度 AI API 调用额度
- 查看控制台错误信息

### Q: 如何添加新学生？
A: 
方法 1：直接编辑数据库
```bash
sqlite3 database.db
INSERT INTO students (student_id, password, name) VALUES ('2024005', '123456', '新学生');
```

方法 2：修改 `database.py` 中的示例数据，重新运行

## 🛠️ 技术栈

- **后端**: Python 3.x + Flask
- **数据库**: SQLite
- **前端**: HTML5 + CSS3 + JavaScript
- **UI 框架**: Bootstrap 5
- **AI 服务**: 百度文心一言 (可选)

## 📞 技术支持

如有问题，请检查：
1. Python 版本 >= 3.8
2. 所有依赖已正确安装
3. 端口 5000 未被占用
4. 查看控制台错误日志

## 📄 许可证

本项目仅供学习交流使用。

---

**祝使用愉快！** 🎉
