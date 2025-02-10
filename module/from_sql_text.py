import mysql.connector
import numpy as np
import os
from module.db_init import *
from module.db_table import DocumentChunk
# 从 MySQL 中加载文本数据
def load_texts_from_mysql(ids):

    texts = []
    with get_db() as db:
        for id in ids:
            # 使用SQLAlchemy ORM查询
            chunk = db.query(DocumentChunk).filter(DocumentChunk.id == int(id)).first()

            texts.append(str(chunk.chunk_text))

    return np.array(texts)