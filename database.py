"""
数据库初始化模块
创建学生表和作业表，并插入示例数据
"""
import sqlite3
from datetime import datetime

def init_database():
    """初始化数据库，创建表结构并插入示例数据"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # 创建学生表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建作业表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            title TEXT NOT NULL,
            image_path TEXT NOT NULL,
            ai_result TEXT,
            status TEXT DEFAULT 'pending',
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    ''')
    
    # 插入示例学生数据（仅用于测试）
    sample_students = [
        ('2024001', '123456', '张三'),
        ('2024002', '123456', '李四'),
        ('2024003', '123456', '王五'),
        ('2024004', '123456', '赵六'),
    ]
    
    for student_id, password, name in sample_students:
        try:
            cursor.execute('''
                INSERT INTO students (student_id, password, name)
                VALUES (?, ?, ?)
            ''', (student_id, password, name))
        except sqlite3.IntegrityError:
            pass  # 如果已存在则跳过
    
    # 注意：不再插入示例作业数据，保持数据库干净
    
    conn.commit()
    conn.close()
    print("数据库初始化完成！")

if __name__ == '__main__':
    init_database()
