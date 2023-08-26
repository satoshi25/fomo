from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    content = Column(String(1500), nullable=True)
    journal = Column(String(50), nullable=False)
    url = Column(String(2083), nullable=False)
    view = Column(Integer, nullable=False)
    publish_date = Column(Date, nullable=False)

    def __repr__(self):
        return (f"Article(id={self.id}, title={self.title}, content={self.content}, "
                f"journal={self.journal}, url={self.url}, publish_date={self.publish_date})")
