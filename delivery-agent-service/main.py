from fastapi import FastAPI, Path
from pydantic import BaseModel
from .crud import *
from typing import Annotated
class User(BaseModel):
    name : str
    status: bool

class UserStatus(BaseModel):
    agent_id : int
    status: bool

class OrderStatus(BaseModel):
    order_id : int
    agent_id : int
    status : str


app = FastAPI()

@app.post("/registerAgent")
async def root(user: User):
    return create_delivery_agent(user)

@app.get("/getallorders/{agentId}")
async def func(agentId: Annotated[int, Path(title="The ID of the delivery Agent")]):
    return getallOrders(agentId)

@app.post("/updateorderStatus")
async def func(data: OrderStatus):
    return updateOrderStatus(data.order_id, data.agent_id, data.status)

@app.post("/updateStatus")
async def func(data: UserStatus):
    return updateAgentStatus(data.agent_id, data.status)

@app.get("/getmyratings/{agent_id}")
async def func(agent_id: Annotated[int, Path(title="The ID of the delivery Agent")]):
    return getAllRatings(agent_id)