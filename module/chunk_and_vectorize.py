import numpy as np
from module.chunk_split import *
from sentence_transformers import SentenceTransformer

#如果是输入问题的情况，要假设问题不是两段而且不会超过最大token

def chunk_and_vectorize(document):
    print("Start Spliting Chunk!!!")
    #分chunk
    chunks = chunk_text_by_delimiter(document)
    print(len(chunks))

    print("Complete Spliting Chunk!!!")
    # 加载预训练的Sentence-BERT模型
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Start vectorizing!!!")

    # 获取每个段落的向量表示
    chunk_vectors = model.encode(chunks)

    print("Complete vectorizing!!!")

    return np.array(chunks),np.array(chunk_vectors)
    # #对于大型文档，测试输出前10条向量化表达
    #print(paragraph_vectors[:10])