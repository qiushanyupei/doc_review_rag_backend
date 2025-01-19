from flask import Flask, jsonify,Blueprint
import mysql.connector
import os

#渲染用的端口的蓝图
r = Blueprint('render', __name__)
#查找documents表中的id和subject
@r.route('/subjects', methods=['GET'])
def get_subjects():
    db_host = os.getenv('DB_HOST', 'localhost')  # 默认值为localhost
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', 'MEIlong750712!')
    db_name = os.getenv('DB_NAME', 'doc_review_rag')
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = db.cursor()



    cursor.execute("SELECT id,subject FROM documents")
    rows = cursor.fetchall()

    cursor.close()
    db.close()

    #将查询结果转换为字典模式
    subjects = [{'id': row[0], 'subject_name': row[1]} for row in rows]
    return jsonify(subjects)  # 返回数据

