# 🌟 学生答题系统 - GitHub 项目

## 📦 项目信息

**仓库地址**: https://github.com/boxiaolanya2008/Student-Answering-System

**公开可见**: ✅ 是

**主要语言**: Python

**许可证**: 学习交流使用

## 🎯 项目亮点

### ✨ 核心功能
- 🔐 学生登录认证系统
- 📤 图片上传（拖拽 + 预览）
- 🤖 AI 自动批改
- ⏳ 智能排队系统
- 💰 Token 消耗控制
- 📊 实时队列监控
- 🎨 专业 SVG 图标
- 📱 响应式设计

### 🚀 技术特色
- **后端**: Flask + SQLite
- **前端**: HTML5 + CSS3 + JS
- **动画**: 流畅线性动画
- **图标**: 自定义 SVG 系统
- **AI**: 百度文心一言（可选）

## 📥 快速部署

```bash
# 克隆仓库
git clone https://github.com/boxiaolanya2008/Student-Answering-System.git

# 进入目录
cd Student-Answering-System

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python database.py

# 启动服务
python app.py

# 访问系统
# http://localhost:5000
```

## 👥 默认账号

| 学号 | 密码 |
|------|------|
| 2024001 | 123456 |
| 2024002 | 123456 |
| 2024003 | 123456 |
| 2024004 | 123456 |

## 📁 文件结构

```
Student-Answering-System/
├── 📄 app.py                 # 主程序（AI 排队系统）
├── 📄 config.py              # 配置文件
├── 📄 database.py            # 数据库脚本
├── 📄 requirements.txt       # 依赖列表
├── 📖 README.md              # 项目说明
├── 📖 RELEASE.md             # 发布说明
├── 🎨 static/
│   ├── css/theme.css        # 主题样式
│   └── icons/               # SVG 图标
├── 🎭 templates/            # HTML 模板
│   ├── login.html          # 登录页
│   ├── dashboard.html      # 仪表盘
│   ├── upload.html         # 上传页
│   ├── detail.html         # 详情页
│   └── queue_status.html   # 队列状态
└── 📂 uploads/              # 上传目录
```

## 🔧 配置选项

### 基础配置 (config.py)
```python
SECRET_KEY = 'your-secret-key'
DEBUG = True
DATABASE = 'database.db'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

### AI 配置（可选）
```python
BAIDU_API_KEY = ''           # 百度 API Key
BAIDU_SECRET_KEY = ''        # 百度 Secret Key
BAIDU_AI_MODEL = 'ernie-bot-4'
```

## 📊 系统特性

### AI 批改排队系统
- ✅ 自动队列管理
- ✅ 后台线程处理
- ✅ 实时状态同步
- ✅ Token 限额控制

### Token 管理
- 每日限额：10,000 tokens
- 自动重置：每日零点
- 超额保护：自动停止
- 实时统计：精确计算

### UI/UX
- 无 emoji 设计（全 SVG）
- 流畅动画效果
- 响应式布局
- 现代化配色

## 🎨 图标系统

所有图标均为自定义 SVG：
- `logo.svg` - 书本形状 Logo
- `document.svg` - 文档图标
- `camera.svg` - 相机图标
- `queue.svg` - 队列图标

特点：
- ✅ 完全可控
- ✅ 跨平台一致
- ✅ 支持动画
- ✅ 可定制

## 📈 开发路线图

### v1.0 (当前版本)
- ✅ 基础功能完成
- ✅ AI 批改系统
- ✅ 排队机制
- ✅ SVG 图标

### v1.1 (计划中)
- [ ] 教师端功能
- [ ] 批量上传
- [ ] 成绩统计
- [ ] WebSocket 实时更新

### v2.0 (未来)
- [ ] 多题目类型
- [ ] PDF 导出
- [ ] Docker 部署
- [ ] 移动端优化

## 🐛 问题反馈

如遇到问题，请提交 Issue：
https://github.com/boxiaolanya2008/Student-Answering-System/issues

提交时请提供：
1. 问题描述
2. 复现步骤
3. 环境信息
4. 截图（如有）

## 🤝 贡献代码

欢迎提交 Pull Request！

```bash
# Fork 仓库
# 创建分支
git checkout -b feature/your-feature

# 提交更改
git commit -m "feat: add your feature"

# 推送
git push origin feature/your-feature

# 创建 PR
```

## 📞 联系方式

- **GitHub**: [@boxiaolanya2008](https://github.com/boxiaolanya2008)
- **项目地址**: https://github.com/boxiaolanya2008/Student-Answering-System

## 📄 许可证

本项目仅供学习交流使用。

---

**⭐ 如果这个项目对你有帮助，请给一个 Star！**

**最后更新**: 2026 年 3 月 17 日
