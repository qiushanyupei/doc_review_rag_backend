from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os

# 数据库连接字符串（请根据你的数据库配置修改这里）
driver = "mysql+mysqlconnector"
username = "root"
password = "MEIlong750712!"
host = os.getenv("DB_HOST", "localhost")
port ="3306"
database_name = "doc_review_rag"
DATABASE_URL = driver+"://" + username + ":" + password +  "@" + host + ":" + port +"/" + database_name

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True)

# 创建基础类
Base = declarative_base()

# 创建Session类，用于数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
