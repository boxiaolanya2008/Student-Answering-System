# 宝塔面板部署指南

## 📋 系统要求

- 宝塔面板 v7.0+
- Python 3.8+
- MySQL 5.7+ (可选，默认使用 SQLite)
- Nginx 或 Apache

---

## 🚀 快速部署步骤

### 第一步：安装宝塔面板

1. **安装宝塔**
   ```bash
   # CentOS/RedHat
   yum install -y wget && wget -O install.sh http://download.bt.cn/install/install_6.0.sh && sh install.sh
   
   # Ubuntu/Debian
   wget -O install.sh http://download.bt.cn/install/install-ubuntu_6.0.sh && sudo bash install.sh
   ```

2. **登录面板**
   - 访问 `http://服务器 IP:8888`
   - 使用安装时显示的账号密码登录

---

### 第二步：创建网站目录

1. **上传项目文件**
   - 进入宝塔面板 → 文件
   - 导航到 `/www/wwwroot/`
   - 创建文件夹 `student-answer`
   - 上传所有项目文件到此目录

2. **目录结构**
   ```
   /www/wwwroot/student-answer/
   ├── app.py
   ├── config.py
   ├── database.py
   ├── requirements.txt
   ├── .env
   ├── templates/
   └── static/
   ```

---

### 第三步：安装 Python 项目管理器

1. **安装插件**
   - 宝塔面板 → 软件商店
   - 搜索 "Python 项目管理器"
   - 点击安装（版本选择 3.8+）

2. **添加项目**
   - Python 项目管理器 → 添加 Python 项目
   - 项目名称：`student-answer`
   - 项目路径：`/www/wwwroot/student-answer`
   - 启动文件：`app.py`
   - Python 版本：3.8 或更高
   - 端口：`5000`

---

### 第四步：安装依赖

1. **打开终端**
   - Python 项目管理器 → 学生答题系统 → 终端

2. **安装依赖包**
   ```bash
   pip install -r requirements.txt
   ```

3. **等待安装完成**
   ```
   Successfully installed Flask-3.0.0 requests-2.31.0 ...
   ```

---

### 第五步：配置环境变量

1. **编辑 .env 文件**
   - 文件 → `/www/wwwroot/student-answer/.env`
   - 修改以下配置：

   ```env
   # Flask 配置
   SECRET_KEY=your-production-secret-key-here
   DEBUG=False
   
   # AI 配置
   AI_API_KEY=sk-cp-k4u74to52poivmts
   AI_BASE_URL=https://cloud.infini-ai.com/maas/coding/v1
   AI_MODEL=kimi-k2.5
   ```

2. **保存文件**

---

### 第六步：初始化数据库

1. **在终端执行**
   ```bash
   cd /www/wwwroot/student-answer
   python database.py
   ```

2. **看到提示**
   ```
   数据库初始化完成！
   ```

---

### 第七步：启动项目

1. **Python 项目管理器**
   - 找到 `student-answer` 项目
   - 点击 "启动"

2. **查看日志**
   - 点击 "日志"
   - 应该看到：
   ```
   学生答题系统启动成功！
   访问地址：http://0.0.0.0:5000
   ```

---

### 第八步：配置网站（反向代理）

#### 方案 A：使用 Nginx（推荐）

1. **添加网站**
   - 网站 → 添加站点
   - 域名：`your-domain.com`（或服务器 IP）
   - 根目录：`/www/wwwroot/student-answer`
   - PHP 版本：纯静态
   - 数据库：SQLite

2. **配置反向代理**
   - 网站设置 → 反向代理
   - 添加反向代理
   - 代理名称：`student-api`
   - 目标 URL：`http://127.0.0.1:5000`
   - 发送域名：`$host`

3. **Nginx 配置文件**（手动）
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
       
       location /uploads/ {
           alias /www/wwwroot/student-answer/uploads/;
       }
       
       location /static/ {
           alias /www/wwwroot/student-answer/static/;
       }
   }
   ```

#### 方案 B：直接访问端口

- 访问：`http://服务器 IP:5000`
- 无需配置反向代理

---

### 第九步：配置防火墙

1. **开放端口**
   - 安全 → 放行端口
   - 如果直接访问：放行 `5000`
   - 如果使用反向代理：放行 `80`（HTTP）或 `443`（HTTPS）

2. **放行规则**
   ```
   端口：5000
   备注：学生答题系统
   ```

---

### 第十步：测试访问

1. **浏览器访问**
   - 反向代理：`http://your-domain.com`
   - 直接访问：`http://服务器 IP:5000`

2. **登录测试**
   - 学号：`admin`
   - 密码：`zzl2008`

3. **验证功能**
   - ✅ 登录成功
   - ✅ 上传作业
   - ✅ AI 批改
   - ✅ 删除作业（管理员）

---

## 🔧 高级配置

### 1. 使用 Gunicorn 生产服务器

**安装 Gunicorn**
```bash
pip install gunicorn
```

**启动命令**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Python 项目管理器配置**
- 启动方式：Gunicorn
- 绑定地址：`0.0.0.0:5000`
- Worker 数量：4

---

### 2. 配置 HTTPS（SSL 证书）

1. **申请证书**
   - 网站 → SSL → Let's Encrypt
   - 免费申请证书

2. **强制 HTTPS**
   - 网站设置 → SSL → 强制 HTTPS
   - 开启

3. **Nginx 配置**
   ```nginx
   server {
       listen 443 ssl;
       server_name your-domain.com;
       
       ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   
   server {
       listen 80;
       server_name your-domain.com;
       return 301 https://$server_name$request_uri;
   }
   ```

---

### 3. 数据库迁移（MySQL）

**安装 MySQL**
- 宝塔面板 → 软件商店 → MySQL 5.7 → 安装

**创建数据库**
```sql
CREATE DATABASE student_answer CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**修改 config.py**
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://用户名：密码@localhost/student_answer'
```

**安装驱动**
```bash
pip install pymysql
```

---

### 4. 定时任务（Token 重置）

**添加系统 Cron**
```bash
# 每天凌晨 1 点重置 token
0 1 * * * cd /www/wwwroot/student-answer && python reset_tokens.py
```

**创建 reset_tokens.py**
```python
import sqlite3
from datetime import datetime

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# 清空当日 token 记录
cursor.execute('DELETE FROM ai_grading_logs WHERE DATE(created_at) < ?', 
               (datetime.now().date().isoformat(),))

conn.commit()
conn.close()
print("Token 计数已重置")
```

---

## 🐛 常见问题

### Q1: 项目无法启动

**检查日志**
```bash
cd /www/wwwroot/student-answer
tail -f logs/error.log
```

**常见错误**
- 端口被占用 → 修改端口
- 依赖缺失 → `pip install -r requirements.txt`
- 权限不足 → `chmod 755 -R /www/wwwroot/student-answer`

---

### Q2: 图片无法上传

**检查目录权限**
```bash
mkdir -p uploads
chmod 777 uploads
```

**Nginx 配置**
```nginx
client_max_body_size 10M;  # 允许上传 10MB
```

---

### Q3: AI 调用失败

**检查网络**
```bash
ping cloud.infini-ai.com
```

**检查 .env 配置**
```env
AI_API_KEY=sk-cp-k4u74to52poivmts
AI_BASE_URL=https://cloud.infini-ai.com/maas/coding/v1
AI_MODEL=kimi-k2.5
```

---

### Q4: 502 Bad Gateway

**原因**: Flask 应用未启动

**解决**:
1. Python 项目管理器 → 启动项目
2. 检查端口是否正确
3. 查看应用日志

---

### Q5: 静态资源 404

**Nginx 配置修正**
```nginx
location /static/ {
    alias /www/wwwroot/student-answer/static/;
    expires 30d;
}

location /uploads/ {
    alias /www/wwwroot/student-answer/uploads/;
}
```

---

## 📊 性能优化

### 1. 启用缓存

**Nginx 缓存配置**
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m;

location / {
    proxy_cache my_cache;
    proxy_cache_valid 200 10m;
}
```

---

### 2. 数据库优化

**使用 MySQL**
```python
# config.py
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:pass@localhost/dbname'
SQLALCHEMY_POOL_SIZE = 20
SQLALCHEMY_MAX_OVERFLOW = 10
```

---

### 3. 并发优化

**Gunicorn 配置**
```bash
gunicorn -w 4 --threads 2 -b 0.0.0.0:5000 app:app
```

**Worker 计算**: `(CPU 核心数 × 2) + 1`

---

## 🔒 安全建议

### 1. 修改默认密码
```sql
UPDATE students SET password='新密码' WHERE student_id='admin';
```

### 2. 限制上传大小
```nginx
client_max_body_size 5M;
```

### 3. 隐藏版本号
```python
# config.py
DEBUG = False
```

### 4. 定期备份
```bash
# 备份脚本
tar -czf backup_$(date +%Y%m%d).tar.gz /www/wwwroot/student-answer
```

---

## 📝 维护日志

### 日常检查清单
- [ ] 查看错误日志
- [ ] 检查磁盘空间
- [ ] 监控 CPU/内存使用率
- [ ] 验证 AI API 可用性
- [ ] 备份数据库

### 更新步骤
1. 停止项目
2. 备份当前版本
3. 上传新版本
4. 安装依赖
5. 执行数据库迁移
6. 启动项目
7. 测试功能

---

## 🎯 总结

通过以上步骤，您应该能在宝塔面板成功部署学生答题系统。

**关键配置**:
- ✅ Python 3.8+
- ✅ 正确的目录权限
- ✅ 反向代理配置
- ✅ 防火墙端口放行
- ✅ 环境变量设置

**遇到问题？**
1. 查看日志
2. 检查配置
3. 重启服务
4. 联系技术支持

---

**祝部署顺利！** 🎉
