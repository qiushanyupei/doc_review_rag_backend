from flask import Flask
from flask_cors import CORS
from routes.file_upload import up
from routes.query_model import q
from routes.render_api import r

#初始化
app = Flask(__name__)
CORS(app)  # 允许跨域访问

#需要的蓝图
app.register_blueprint(up)
app.register_blueprint(q)
app.register_blueprint(r)


if __name__ == '__main__':
    app.run(debug = True,port=5000)


