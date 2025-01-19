from flask import Flask, Blueprint, request, jsonify
from module.chunk_and_vectorize import *
from module.model_api import *
import mysql.connector
from module.chunk_split import *
import os

up = Blueprint('up', __name__)

# 文件上传、分chunk、向量化、存入数据库接口
@up.route("/upload", methods=["POST"])
def upload_file():
    # 获取用户输入的文档
    data = request.json
    document = data.get('documentContent', '')

    db_host = os.getenv('DB_HOST', 'localhost')  # 默认值为localhost
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', 'MEIlong750712!')
    db_name = os.getenv('DB_NAME', 'doc_review_rag')
    #首先创建这个文件相对应的主题，用于后续索引
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    cursor = db.cursor()
    #开始做摘要，用来作为文件的主题

    tmpdocument = document
    result = chunk_text_by_delimiter(tmpdocument,chunk_size=4096)
    tmpdocument = result[0]+ "--------------------------------------\n请用不多于20个字概括这篇文档的内容"
    output_text = call_model(tmpdocument)
    insert_query = "INSERT INTO documents (subject) VALUES (%s)"
    cursor.execute(insert_query, (output_text,))

    #例行提交事务，执行更改
    db.commit()
    #查询documents表中对应的id
    cursor.execute("SELECT id FROM documents WHERE subject = %s", (output_text,))
    rows = cursor.fetchall()#后面document_chunks表需要的外键

    #分块+向量化
    chunks, chunk_vectors = chunk_and_vectorize(document)

    for i in range(len(chunks)):
        # 将向量存储到 MySQL 数据库
        insert_query = "INSERT INTO document_chunks (document_id,chunk_text, vectorized_chunk) VALUES (%s,%s, %s)"
        cursor.execute(insert_query, (rows[0][0],chunks[i], chunk_vectors[i].tobytes()))  # 将向量转换为字节流存储

    db.commit()
    cursor.close()
    db.close()
    print("Complete Inserting!!!")

    return jsonify({"message": "File uploaded and processed successfully"})


