import mysql.connector
import numpy as np
import os
# 从 MySQL 中加载向量数据
#指定主题向量数据
#从来做相似度检索
def load_vectors_from_mysql(Id):
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

    cursor.execute("SELECT id,vectorized_chunk FROM document_chunks WHERE document_id = %s",(int(Id),))
    rows = cursor.fetchall()

    vectors = []
    ids = []

    for row in rows:
        id = row[0]
        vector = np.frombuffer(row[1], dtype=np.float32)
        vectors.append(vector)
        ids.append(id)

    cursor.close()
    db.close()

    return np.array(vectors), np.array(ids)