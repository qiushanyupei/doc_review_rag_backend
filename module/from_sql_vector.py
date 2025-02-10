import mysql.connector
import numpy as np
from module.db_init import *
from module.db_table import DocumentChunk
# 从 MySQL 中加载向量数据
#指定主题向量数据
#从来做相似度检索
def load_vectors_from_mysql(Id):
    with get_db() as db:

        chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == int(Id)).all()

        vectors = []
        ids = []

        for chunk in chunks:
            vector = np.frombuffer(chunk.vectorized_chunk, dtype=np.float32)
            vectors.append(vector)
            ids.append(chunk.id)

    return np.array(vectors), np.array(ids)