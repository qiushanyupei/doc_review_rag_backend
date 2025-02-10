from sqlalchemy import Column, Integer, String, Text, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from .db_config import Base

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String(255), nullable=True)

    # 关系映射：一个文档可以有多个文档片段
    chunks = relationship("DocumentChunk", back_populates="document")

    def __repr__(self):
        return f"<Document(id={self.id}, subject='{self.subject}')>"

class DocumentChunk(Base):
    __tablename__ = 'document_chunks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=True)
    chunk_text = Column(Text, nullable=True)
    vectorized_chunk = Column(LargeBinary, nullable=True)

    # 关系映射：一个文档片段属于一个文档
    document = relationship("Document", back_populates="chunks")

    def __repr__(self):
        return f"<DocumentChunk(id={self.id}, document_id={self.document_id})>"