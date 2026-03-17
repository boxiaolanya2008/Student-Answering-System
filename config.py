# 配置文件

# Flask 配置
SECRET_KEY = 'your-secret-key-here-change-in-production'  # 请修改为随机密钥
DEBUG = True

# 数据库配置
DATABASE = 'database.db'

# 上传文件配置
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大上传大小 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 百度 AI 配置 (后续填写)
BAIDU_API_KEY = ''  # 百度文心一言 API Key
BAIDU_SECRET_KEY = ''  # 百度文心一言 Secret Key
BAIDU_AI_MODEL = 'ernie-bot-4'  # AI 模型名称
