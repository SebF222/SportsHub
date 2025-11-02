#where I will initialize SQLAlchemy and create my models
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, String, ForeignKey 
from datetime import date 

#Create Base Model to be inherited from 
class Base(DeclarativeBase):
    pass

#Instatiate db and set Base model
db = SQLAlchemy(model_class=Base)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(500), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)


    favorite_teams: Mapped[list['FavoriteTeam']] = relationship( back_populates='user', cascade ='all, delete-orphan') 


class FavoriteTeam(Base):
    __tablename__ = 'favorite_teams'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    team_id: Mapped[int] = mapped_column(nullable=False)
    team_name: Mapped[str] = mapped_column(String(360), nullable=False)
    team_logo: Mapped[str] = mapped_column(String(500), nullable=False)
    league: Mapped[str] = mapped_column(String(250), nullable=True)
    country: Mapped[str] = mapped_column(String(200), nullable=True)

    user: Mapped['User'] = relationship (back_populates='favorite_teams')