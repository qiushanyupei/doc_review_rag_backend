from flask import Blueprint,request,jsonify
from module.model_api import *
from module.from_sql_text import *
from module.from_sql_vector import *
from module.chunk_and_vectorize import *
import faiss

#注册需要的蓝图
q = Blueprint('query', __name__)

@q.route("/query", methods=["POST"])
def query():
# 获取用户输入的问题
        data = request.json
        user_question = data.get('question', '')
        Id = data.get('Id','')
        if not user_question:
                return jsonify({'error': 'No question provided'}), 400
        #faiss索引操作
        # 从 MySQL 加载向量
        vectors,ids = load_vectors_from_mysql(Id)

        # 构建 FAISS 索引
        dimension = vectors.shape[1]  # 向量维度
        index1 = faiss.IndexFlatL2(dimension)  # 使用 L2 距离
        # index1.add(vectors)  # 将向量添加到索引中
        index=faiss.IndexIDMap(index1)
        index.add_with_ids(vectors, ids)

        #对问题进行向量化
        query_chunk,query_vector = chunk_and_vectorize(user_question)

        print(query_vector.shape)

        k = min(5,len(vectors))  # 查询返回的最近邻个数
        distances, indices = index.search(query_vector, k)

        # 暂时还不确定这个indices是否准确
        texts = load_texts_from_mysql(indices[0])
        # 组合问题，准备传给大模型
        context =""
        for text in texts:
            context += text+"\n"


        result = chunk_text_by_delimiter(context, chunk_size=4096)
        final_result = result[0]
        final_result  += "__________________________\n以上是语境，"+user_question
        print(final_result)
        output_text = call_model(final_result)
        # 回显结果
        return jsonify({'answer': output_text}), 200


