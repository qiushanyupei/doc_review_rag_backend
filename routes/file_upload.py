from flask import Flask, Blueprint, request, jsonify
from module.chunk_and_vectorize import *
from module.model_api import *
import mysql.connector
from module.chunk_split import *
import os
from module.db_init import *
from module.db_table import Document,DocumentChunk

up = Blueprint('up', __name__)

# 文件上传、分chunk、向量化、存入数据库接口
@up.route("/upload", methods=["POST"])
def upload_file():
    # 获取用户输入的文档
    data = request.json
    document = data.get('documentContent', '')

    # db_host = os.getenv('DB_HOST', 'localhost')  # 默认值为localhost

    #开始做摘要，用来作为文件的主题

    tmpdocument = document
    result = chunk_text_by_delimiter(tmpdocument,chunk_size=4096)
    tmpdocument = result[0]+ "--------------------------------------\n请用不多于20个字概括这篇文档的内容"
    output_text = call_model(tmpdocument)

    # 使用SQLAlchemy插入文档记录
    document_entry = Document(subject=output_text)
    with get_db() as db:
        db.add(document_entry)#添加文档记录
        db.commit()#例行提交事务，执行更改
        #查询documents表中对应的id
        # 获取插入的文档ID
        document_id = document_entry.id

        #分块+向量化
        chunks, chunk_vectors = chunk_and_vectorize(document)

        for i in range(len(chunks)):
            chunk_entry = DocumentChunk(
                document_id=document_id,
                chunk_text=chunks[i],
                vectorized_chunk=chunk_vectors[i].tobytes()  # 将向量转换为字节流
            )
            db.add(chunk_entry)

        db.commit()
        print("Complete Inserting!!!")

    return jsonify({"message": "File uploaded and processed successfully"})


