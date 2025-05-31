from fastapi import FastAPI, Path
from shared.database import engine, Base
from pydantic import BaseModel
from .crud import *
from typing import Annotated

class User(BaseModel):
    name : str
    email : str

class Order(BaseModel):
    user_id : int
    restaurant_id : int
    food : list

class Rate(BaseModel):
    user_id: int
    order_id : int
    food_rating: int
    delivery_agent_rating : int

app = FastAPI()

Base.metadata.create_all(bind=engine)
@app.get("/")
async def root(user: User):
    return {"message": "Hello World"}


@app.post("/register")
async def func(user: User):
    print(user)
    x = create_user(user)
    if x != False:
        return {"message": "User Created Successfully", "user": x}
    else:
        return {"message": "User exsist"}
    

@app.post("/order")
async def func(order: Order):
    return create_order(order)

@app.get("/getAllMenu")
async def func():
    return getMenu()

@app.get("/getUsersOrders/{user_id}")
async def func(user_id: Annotated[int, Path(title="The ID of the user")]):
    return getMyOrders(user_id)

@app.post("/rate")
async def func(rating : Rate):
    return rate_order(rating.user_id,rating.order_id, rating.food_rating, rating.delivery_agent_rating)


    
