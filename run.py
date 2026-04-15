"""
学生答题系统 - 入口文件
"""
import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
