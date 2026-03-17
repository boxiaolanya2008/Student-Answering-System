# 配置文件
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Flask 配置
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')  # 请修改为随机密钥
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# 数据库配置
DATABASE = 'database.db'

# 上传文件配置
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大上传大小 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# AI 配置（从环境变量读取）
AI_API_KEY = os.getenv('AI_API_KEY', '')  # API Key
AI_BASE_URL = os.getenv('AI_BASE_URL', '')  # API 基础 URL
AI_MODEL = os.getenv('AI_MODEL', '')  # AI 模型名称

# 备用百度 AI 配置（如果使用百度）
BAIDU_API_KEY = os.getenv('BAIDU_API_KEY', '')  # 百度文心一言 API Key
BAIDU_SECRET_KEY = os.getenv('BAIDU_SECRET_KEY', '')  # 百度文心一言 Secret Key
BAIDU_AI_MODEL = os.getenv('BAIDU_BAIDU_AI_MODEL', 'ernie-bot-4')  # AI 模型名称
