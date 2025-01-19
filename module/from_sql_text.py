import mysql.connector
import numpy as np
import os
# 从 MySQL 中加载文本数据
def load_texts_from_mysql(ids):
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
    texts = []

    for id in ids:
        cursor.execute("SELECT chunk_text FROM document_chunks WHERE id = %s", (int(id),))
        row = cursor.fetchall()
        texts.append(str(row[0][0]))

    cursor.close()
    db.close()

    return np.array(texts)