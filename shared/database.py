from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
order_menu_association = Table(
    'order_menu_association',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('menu_item_id', Integer, ForeignKey('menu_items.id'))
)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    is_online = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    menu_items = relationship("MenuItem", back_populates="restaurant")

class MenuItem(Base):
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship("Restaurant", back_populates="menu_items")
    orders = relationship("Order", secondary=order_menu_association, back_populates="menu_items")


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    agent_id = Column(Integer, ForeignKey('delivery_agents.id'), nullable=True)
    menu_items = relationship("MenuItem", secondary=order_menu_association, back_populates="orders")
    status = Column(String, default="pending") # accepted, rejected, delivering, delivered and pending
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    food_rating = Column(Integer, nullable=True)
    delivery_agent_rating = Column(Integer, nullable=True)

class DeliveryAgent(Base):
    __tablename__ = 'delivery_agents'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    is_available = Column(Boolean, default=True)

    