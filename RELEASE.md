# 📦 发布说明 - 学生答题系统 v1.0

## 🎉 项目概述

一个基于 Python Flask 的现代化学生答题系统，集成了 AI 自动批改、智能排队系统和专业的 UI 设计。

**GitHub 仓库**: https://github.com/boxiaolanya2008/Student-Answering-System

## ✨ 核心功能

### 1. 用户认证系统
- ✅ 学号 + 密码登录
- ✅ Session 会话管理
- ✅ 安全的身份验证

### 2. 作业管理
- ✅ 图片上传（支持拖拽）
- ✅ 实时预览
- ✅ 作业列表展示
- ✅ 详情查看

### 3. AI 批改系统
- ✅ 智能排队系统
- ✅ 自动顺序批改
- ✅ 实时状态更新
- ✅ Token 消耗控制（每日限额 10,000）

### 4. 队列状态监控
- ✅ 实时队列长度显示
- ✅ 批改进度跟踪
- ✅ Token 使用统计
- ✅ 自动刷新（3 秒间隔）

### 5. UI/UX 优化
- ✅ 专业 SVG 图标系统
- ✅ 流畅线性动画
- ✅ 响应式设计
- ✅ 现代化配色方案

## 🛠️ 技术栈

### 后端
- **框架**: Flask 3.0.0
- **数据库**: SQLite
- **ORM**: SQLAlchemy 2.0.23
- **HTTP 库**: requests 2.31.0
- **图像处理**: Pillow >=10.0.0

### 前端
- **框架**: HTML5 + CSS3 + JavaScript
- **样式**: 自定义主题 CSS
- **图标**: Custom SVG
- **动画**: CSS Keyframe Animations

### AI 集成
- **服务**: 百度文心一言（可选配置）
- **模型**: ernie-bot-4
- **备用**: 模拟批改模式

## 📁 项目结构

```
Student-Answering-System/
├── app.py                 # Flask 主程序（AI 排队系统）
├── config.py              # 配置文件
├── database.py            # 数据库初始化
├── requirements.txt       # Python 依赖
├── README.md              # 项目说明
├── .gitignore            # Git 忽略文件
├── static/
│   ├── css/
│   │   └── theme.css     # 主题样式
│   └── icons/
│       ├── logo.svg      # Logo 图标
│       ├── document.svg  # 文档图标
│       ├── camera.svg    # 相机图标
│       ├── queue.svg     # 队列图标
│       └── README.md     # 图标使用说明
├── templates/
│   ├── login.html        # 登录页面
│   ├── dashboard.html    # 作业列表
│   ├── detail.html       # 作业详情
│   ├── upload.html       # 上传页面
│   └── queue_status.html # 队列状态页
└── uploads/              # 图片上传目录
```

## 🚀 快速开始

### 方法一：一键启动（推荐）
```bash
# Windows 用户
双击运行：启动.bat
```

### 方法二：手动启动
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 初始化数据库
python database.py

# 3. 启动服务器
python app.py

# 4. 访问系统
浏览器打开：http://localhost:5000
```

## 👤 示例账号

| 学号 | 密码 | 姓名 |
|------|------|------|
| 2024001 | 123456 | 张三 |
| 2024002 | 123456 | 李四 |
| 2024003 | 123456 | 王五 |
| 2024004 | 123456 | 赵六 |

## ⚙️ AI 配置（可选）

如需启用真实的 AI 批改功能：

1. **获取百度 AI 密钥**
   - 访问 [百度智能云](https://cloud.baidu.com/product/wenxinworkshop)
   - 注册并创建应用
   - 获取 API Key 和 Secret Key

2. **配置密钥**
   ```python
   # 编辑 config.py
   BAIDU_API_KEY = '你的 API Key'
   BAIDU_SECRET_KEY = '你的 Secret Key'
   BAIDU_AI_MODEL = 'ernie-bot-4'
   ```

3. **未配置时**
   - 系统自动使用模拟批改模式
   - 不影响基本功能使用

## 🎨 特色亮点

### 1. AI 批改排队系统
```python
class AIGradingQueue:
    - 自动队列管理
    - 后台线程处理
    - Token 智能控制
    - 实时状态同步
```

### 2. SVG 图标系统
- 完全替代 emoji
- 统一设计风格
- 跨平台一致性
- 可定制动画

### 3. 流畅动画效果
- `fadeInUp` - 页面加载
- `cardEnter` - 卡片入场
- `pulse` - Logo 脉冲
- `bounce` - 图标弹跳
- `shimmer` - 进度条闪烁

### 4. Token 管控机制
- 每日自动重置
- 实时使用统计
- 超额自动停止
- 精确估算公式

## 📊 系统截图

### 主要界面
- **登录页**: 简洁专业的登录界面
- **仪表盘**: 卡片式作业列表
- **上传页**: 拖拽式图片上传
- **详情页**: 左右分栏展示
- **队列页**: 实时监控批改进度

## 🔒 安全特性

- ✅ 密码验证
- ✅ Session 保护
- ✅ 文件类型检查
- ✅ 大小限制（16MB）
- ✅ SQL 注入防护（参数化查询）

## 📝 API 端点

| 路由 | 方法 | 描述 | 认证 |
|------|------|------|------|
| `/` | GET | 首页（重定向） | ❌ |
| `/login` | GET/POST | 登录 | ❌ |
| `/logout` | GET | 登出 | ✅ |
| `/dashboard` | GET | 作业列表 | ✅ |
| `/upload` | GET/POST | 上传作业 | ✅ |
| `/assignment/<id>` | GET | 作业详情 | ✅ |
| `/queue-status` | GET | 队列状态页 | ✅ |
| `/api/queue-status` | GET | 队列 API | ✅ |
| `/uploads/<filename>` | GET | 文件访问 | ✅ |

## 🐛 已知问题

目前暂无已知问题。如发现问题，请在 GitHub 提交 Issue。

## 🗺️ 未来计划

- [ ] 教师管理端
- [ ] 多题目类型支持
- [ ] 批量上传功能
- [ ] 成绩统计分析
- [ ] 导出 PDF 报告
- [ ] WebSocket 实时更新
- [ ] Docker 容器化部署

## 📄 许可证

本项目仅供学习交流使用。

## 🤝 贡献指南

欢迎提交 Pull Request！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📞 联系方式

- **GitHub Issues**: [提交问题](https://github.com/boxiaolanya2008/Student-Answering-System/issues)
- **Email**: （可选填写）

## 🙏 致谢

感谢以下开源项目：
- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Bootstrap](https://getbootstrap.com/)
- [百度文心一言](https://cloud.baidu.com/product/wenxinworkshop)

---

**开发团队**: 白小狼  
**版本**: v1.0  
**发布日期**: 2026 年 3 月 17 日  
**最后更新**: 2026 年 3 月 17 日
