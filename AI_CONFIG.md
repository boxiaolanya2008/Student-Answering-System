# 🔑 AI 配置说明

## ✅ 当前配置状态

您的 AI API 已配置完成，系统现在使用 **Infini-AI** 服务进行作业批改。

### 配置信息

| 配置项 | 值 | 状态 |
|--------|-----|------|
| API Provider | Infini-AI | ✅ 已启用 |
| API Key | sk-cp-k4u74to52poivmts | ✅ 已配置 |
| Base URL | https://cloud.infini-ai.com/maas/coding/v1 | ✅ 已配置 |
| Model | kimi-k2.5 | ✅ 已配置 |

## 📁 配置文件位置

所有敏感配置都存储在 `.env` 文件中（已在 `.gitignore` 中排除）：

```
.env                    # 环境变量配置（不上传到 Git）
config.py              # 配置加载模块
app.py                 # AI 调用逻辑
```

## 🔄 工作原理

### 1. 配置加载流程
```python
# config.py
from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件

AI_API_KEY = os.getenv('AI_API_KEY')      # 读取 API Key
AI_BASE_URL = os.getenv('AI_BASE_URL')    # 读取 API 地址
AI_MODEL = os.getenv('AI_MODEL')          # 读取模型名称
```

### 2. AI 调用优先级
```
1️⃣ Infini-AI (当前配置) → 如果配置了 AI_API_KEY
2️⃣ Baidu AI (备用方案)   → 如果配置了 BAIDU_API_KEY
3️⃣ Demo Mode (演示模式)  → 如果都未配置
```

### 3. 调用流程
```
用户上传作业
    ↓
加入批改队列
    ↓
AI 处理任务
    ↓
调用 Infini-AI API
    ↓
返回批改结果
    ↓
更新数据库
```

## 📝 完整的 .env 配置

```env
# Flask 配置
SECRET_KEY=student-answer-system-secret-key-2026
DEBUG=True

# AI 配置（当前使用的 API）
AI_API_KEY=sk-cp-k4u74to52poivmts
AI_BASE_URL=https://cloud.infini-ai.com/maas/coding/v1
AI_MODEL=kimi-k2.5

# 备用百度 AI 配置（如需要切换）
# BAIDU_API_KEY=your_baidu_api_key
# BAIDU_SECRET_KEY=your_baidu_secret_key
# BAIDU_AI_MODEL=ernie-bot-4
```

## 🧪 测试方法

### 方法一：上传测试
1. 登录系统（学号：2024001，密码：123456）
2. 点击"上传新作业"
3. 选择一张作业图片
4. 提交后观察批改结果

### 方法二：查看日志
服务器控制台会显示 AI 调用信息：
```
AI 调用异常：...  # 如果有错误会显示
```

### 预期结果
- ✅ **成功**: 显示 AI 批改的详细结果
- ⚠️ **失败**: 自动切换到演示模式（模拟结果）

## 🔍 故障排查

### 问题 1: API 调用失败
**症状**: 显示 "API 请求失败：HTTP 401"
**原因**: API Key 无效或过期
**解决**: 
1. 检查 `.env` 中的 `AI_API_KEY` 是否正确
2. 联系 API 提供商确认密钥状态

### 问题 2: 连接超时
**症状**: 显示 "Connection timeout"
**原因**: 网络问题或 API 服务不可用
**解决**:
1. 检查网络连接
2. 尝试访问 API Base URL 确认服务可用
3. 增加超时时间（修改 `app.py` 中的 `timeout=60`）

### 问题 3: 模型不存在
**症状**: 显示 "Model not found"
**原因**: 配置的模型名称错误
**解决**:
1. 检查 `.env` 中的 `AI_MODEL` 是否正确
2. 确认该模型在您的账户中可用

## 🎯 性能优化

### Token 控制
- 每日限额：10,000 tokens
- 估算公式：标题长度×100 + 结果长度×0.5
- 自动重置：每日零点

### 超时设置
```python
# app.py
response = requests.post(
    url,
    json=payload,
    headers=headers,
    timeout=60  # 60 秒超时
)
```

### 错误重试（可选扩展）
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def call_ai_with_retry():
    # AI 调用代码
    pass
```

## 📊 监控与统计

### 实时查看
访问 `/queue-status` 页面查看：
- 当前队列长度
- Token 使用情况
- 今日已完成数量

### 日志记录（可选扩展）
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_ai_result(image_path, title):
    logger.info(f"开始批改作业：{title}")
    # ... AI 调用代码
    logger.info(f"批改完成，使用 Provider: {result['provider']}")
```

## 🔄 切换到其他 AI 服务

### 切换到百度 AI
编辑 `.env`:
```env
# 注释掉 Infini-AI 配置
# AI_API_KEY=sk-cp-k4u74to52poivmts
# AI_BASE_URL=https://cloud.infini-ai.com/maas/coding/v1
# AI_MODEL=kimi-k2.5

# 启用百度 AI 配置
BAIDU_API_KEY=your_baidu_key
BAIDU_SECRET_KEY=your_baidu_secret
BAIDU_AI_MODEL=ernie-bot-4
```

重启服务器即可自动切换。

## 🔒 安全建议

1. **不要提交 `.env` 到 Git**
   - 已在 `.gitignore` 中排除
   - 创建 `.env.example` 作为模板

2. **定期更换密钥**
   - 建议每月更换一次 API Key
   - 使用强随机 SECRET_KEY

3. **限制访问**
   - 生产环境设置防火墙规则
   - 使用 HTTPS 加密传输

## 📞 获取帮助

如遇到问题：
1. 检查服务器日志
2. 验证 `.env` 配置
3. 测试 API 连通性
4. 提交 GitHub Issue

---

**配置完成时间**: 2026 年 3 月 17 日  
**当前状态**: ✅ 正常运行  
**AI Provider**: Infini-AI (kimi-k2.5)
