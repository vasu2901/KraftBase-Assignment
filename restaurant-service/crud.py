from shared.database import *

def create_restaurant(restro_data):
    db = SessionLocal()
    try:
        restro = Restaurant(
            name=restro_data.name,
            is_online=restro_data.is_online,
            created_by=restro_data.userId
        )
        db.add(restro)
        db.commit()
        db.refresh(restro)
        return {"restaurant": restro}
    except Exception as e:
        db.rollback()
        return {"Error": e}
    finally:
        db.close() 

def addItemsinMenu(data):
    db = SessionLocal()
    #check if the user has created the restaurant or not.
    is_restaurant = db.query(Restaurant).filter(
        Restaurant.id == data.restaurantId,
        Restaurant.created_by == data.userId
    )

    if not is_restaurant:
        return {"Message": "Sorry, you are not the owner of this restaurant"}

    else:
        try:
            menu = MenuItem(
                name = data.name,
                price = data.price,
                restaurant_id = data.restaurantId
            )
            db.add(menu)
            db.commit()
            db.refresh(menu)
            return {"message": "Menu Added Successfully", "data": menu}
        except Exception as e:
            db.rollback()
            return {"error": e}
        finally:
            db.close()

def updateMenu(item_id, data):
    db = SessionLocal()

    try:

        is_restaurant = db.query(Restaurant).filter(
            Restaurant.id == data.restaurantId,
            Restaurant.created_by == data.userId
        ).first()

        if not is_restaurant:
            return {"message": "Sorry, you are not the owner of this restaurant"}

        menu = db.query(MenuItem).filter(
            MenuItem.id == item_id,
            MenuItem.restaurant_id == data.restaurantId
        ).first()

        if not menu:
            return {"message": "Menu item not found for update"}

        menu.name = data.name
        menu.price = data.price

        db.commit()
        db.refresh(menu)
        return {
            "message": "Menu Updated Successfully",
            "data": {
                "id": menu.id,
                "name": menu.name,
                "price": menu.price,
                "restaurant_id": menu.restaurant_id
            }
        }
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()

def getOrders(restaurant_id):
    db = SessionLocal()
    try:
        orders = db.query(Order).filter(Order.restaurant_id == restaurant_id, Order.status.in_(["pedning", "rejected"])).all()
        result = []

        for order in orders:
            order_data = {
                "order_id": order.id,
                "user_id": order.user_id,
                "status": order.status,
                "created_at": order.created_at,
                "menu_items": [
                    {
                        "id": item.id,
                        "name": item.name,
                        "price": item.price
                    }
                    for item in order.menu_items
                ]
            }
            result.append(order_data)

        return {"data": result}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def updateStatus(data):
    db = SessionLocal()

    try:

        is_restaurant = db.query(Restaurant).filter(
            Restaurant.id == data.restaurantId,
            Restaurant.created_by == data.userId
        ).first()

        if not is_restaurant:
            return {"message": "Sorry, the data does not exsist"}

        is_restaurant.is_online = data.status

        db.commit()
        db.refresh(is_restaurant)
        return {
            "message": "Status Updated Successfully",
            "data": is_restaurant
        }
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()
    

def updateOrderStatus(order_id, restaurant_id, status):
    db = SessionLocal()
    try:
        order = db.query(Order).filter(
            Order.id == order_id,
            Order.restaurant_id == restaurant_id
        ).first()
        if status == "rejected":
            order.status = status
            db.commit()
            db.refresh(order)
            return {"order": order}
        delivery_agents = db.query(DeliveryAgent).filter(DeliveryAgent.is_available == True).first()
        if delivery_agents == None:
            return {"message": "No Agents are available"}
        print(order)
        order.status = status
        order.agent_id = delivery_agents.id
        db.commit()
        db.refresh(order)
        return {"order": order}
    except Exception as e:
        return {e}
    finally:
        db.close()

def displayRestaurantRatings(restaurant_id):
    db = SessionLocal()
    try:
        orders = db.query(Order).filter(Order.restaurant_id == restaurant_id, Order.status == "delivered" ).all()
        if orders is None or len(orders) == 0:
            return {"message": "No deliveries done yet."}
        result = []
        for order in orders:
            order_data = {
                "order_id": order.id,
                "user_id": order.user_id,
                "status": order.status,
                "created_at": order.created_at,
                "Ratings": order.food_rating
            }
            result.append(order_data)

        return {"data": result}

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()

