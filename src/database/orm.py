from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

from src.schema.scrap import ArticleModel


Base = declarative_base()


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    image = Column(String(2083), nullable=False)
    journal = Column(String(50), nullable=False)
    url = Column(String(2083), nullable=False)
    view = Column(Integer, nullable=False)
    publish_date = Column(Date, nullable=False)

    def __repr__(self):
        return (f"Article(id={self.id}, title={self.title}, image={self.image}, "
                f"journal={self.journal}, url={self.url}, publish_date={self.publish_date})")

    def update_image(self, image: str):
        self.image = image

    def update_url(self, url: str):
        self.url = url

    @classmethod
    def create_article(cls, article: dict | ArticleModel) -> "Article":
        return cls(
            title=article.get("title"),
            image=article.get("image"),
            journal=article.get("journal"),
            url=article.get("url"),
            view=article.get("view"),
            publish_date=article.get("publish_date")
        )


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)
    role = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Article(id={self.id}, username={self.username}"

    @classmethod
    def create_user(cls, username: str, password: str, role: int) -> 'User':
        return cls(
            username=username,
            password=password,
            role=role
        )
