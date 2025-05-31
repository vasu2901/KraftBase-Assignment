from fastapi import FastAPI, Path
from pydantic import BaseModel
from .crud import *
from typing import Annotated


class Restaurant(BaseModel):
    name : str
    is_online: bool
    userId: int

class RestaurantStatus(BaseModel):
    status : bool
    restaurantId: int
    userId: int

class Menu(BaseModel):
    userId: int
    restaurantId: int
    name: str
    price: int

class OrderStatus(BaseModel):
    order_id: int
    restaurant_id : int
    status : str

app = FastAPI()

@app.post("/addRestaurant")
async def root(user: Restaurant):
    return create_restaurant(user)


@app.post("/addItemsinMenu")
async def func(data: Menu):
    return addItemsinMenu(data)

@app.post("/updateMenuItem/{item_id}")
async def func(item_id: Annotated[int, Path(title="The ID of the item to get")], data: Menu):
    return updateMenu(item_id, data)

@app.get("/getAllOrders/{restaurant_id}/")
async def func(restaurant_id: Annotated[int, Path(title="The ID of the restaurant")]):
    return getOrders(restaurant_id)

@app.post('/updateStatus')
async def func(data: RestaurantStatus):
    return updateStatus(data)

@app.post("/updateOrder")
async def func(data: OrderStatus):
    print(data)
    return updateOrderStatus(data.order_id, data.restaurant_id, data.status)

@app.get("/getRestaurantRatings/{restaurant_id}")
async def func(restaurant_id: Annotated[int, Path(title="The Id of the Restaurant")]):
    return displayRestaurantRatings(restaurant_id)