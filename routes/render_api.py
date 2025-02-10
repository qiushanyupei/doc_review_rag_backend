from flask import Flask, jsonify,Blueprint
from module.db_init import *
from module.db_table import Document

#渲染用的端口的蓝图
r = Blueprint('render', __name__)
#查找documents表中的id和subject
@r.route('/subjects', methods=['GET'])
def get_subjects():

    with get_db() as db:  # 使用上下文管理器
        # ORM 查询数据
        documents = db.query(Document.id, Document.subject).all()

        # 转换为字典格式
        subjects = [{'id': doc.id, 'subject_name': doc.subject} for doc in documents]

    return jsonify(subjects)  # 返回数据

