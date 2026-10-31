from sqlalchemy import Integer, String, Boolean

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


"""class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
"""


from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = 'tasks'
    id:Mapped[int] = mapped_column(Integer,primary_key=True,)
    title: Mapped[str] = mapped_column(String(100),nullable=False,)
    is_completed:Mapped[bool] = mapped_column(Boolean,nullable=False,default=False)
