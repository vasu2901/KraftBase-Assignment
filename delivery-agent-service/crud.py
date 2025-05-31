from shared.database import *

def create_delivery_agent(data):
    db = SessionLocal()
    try:
        agent = DeliveryAgent(
            name=data.name,
            is_available=data.status
        )
        db.add(agent)
        db.commit()
        db.refresh(agent)
        return {"data": agent}
    except Exception as e:
        db.rollback()
        return {"Error": e}
    finally:
        db.close() 

def  getallOrders(agentId):
    db = SessionLocal()
    #check if the user has created the restaurant or not.
    try:
        data = db.query(Order).filter(
            Order.agent_id == agentId,
            Order.status == "accepted"
        ).all()

        return {"orders": data}

    except Exception as e:
        return {e}
    finally:
        db.close()

def updateAgentStatus(agent_id, status):
    db = SessionLocal()
    try:
        agent = db.query(DeliveryAgent).filter(DeliveryAgent.id == agent_id).first()
        if agent is None:
            return {"message": "Agent Not Found"}
        agent.is_available = status
        db.commit()
        db.refresh(agent)
        return {"agent": agent}

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()

def updateOrderStatus(order_id, agent_id, status):
    db = SessionLocal()
    try:
        agent = db.query(Order).filter(Order.id == order_id, Order.agent_id == agent_id).first()
        if agent is None:
            return {"message": "Agent Not Found"}
        agent.status = status
        db.commit()
        db.refresh(agent)
        return {"order": agent}

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()

def getAllRatings(agent_id):
    db = SessionLocal()
    try:
        orders = db.query(Order).filter(Order.agent_id == agent_id, Order.status == "delivered" ).all()
        if orders is None or len(orders) == 0:
            return {"message": "No deliveries done yet."}
        result = []
        for order in orders:
            order_data = {
                "order_id": order.id,
                "user_id": order.user_id,
                "status": order.status,
                "created_at": order.created_at,
                "agent_rating": order.delivery_agent_rating
            }
            result.append(order_data)

        return {"data": result}

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()