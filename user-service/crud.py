from shared.database import *

def create_user(user_data):
    db = SessionLocal()
    print(user_data)
    email = user_data.email.lower()
    user = User(
            name=user_data.name,
            email=email
        )
    try:
        db.add(user)
        db.commit()           # Commit is required to persist data
        db.refresh(user)      # Refresh the instance with updated DB state
        return user
    except Exception as e:
        db.rollback()         # Rollback in case of error
        print("Error:", e)
        return False
    finally:
        db.close()            # Ensure the session is closed

def create_order(order):
    db = SessionLocal()
    menu_items = db.query(MenuItem).filter(MenuItem.id.in_(order.food), MenuItem.restaurant_id == order.restaurant_id).all()
    if len(menu_items) == 0:
        return {"message": "Kindly Select the Dishes from the menu."}
    new_order = Order(
        user_id=order.user_id,
        restaurant_id=order.restaurant_id,
        menu_items=menu_items
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {"order": new_order}

def getMyOrders(user_id):
    db = SessionLocal()
    try:
        my_order = db.query(Order).filter(Order.user_id == user_id).all()
        return {"data": my_order}

    except Exception as e:
        return {e}

    finally:
        db.close()


def rate_order(user_id, order_id, rating, delivery_rating):
    db = SessionLocal()
    try:
        # Find the order belonging to the specific user
        order = db.query(Order).filter(
            Order.id == order_id,
            Order.user_id == user_id,
            Order.status == "delivered"
        ).first()

        if not order:
            return {"error": "Order not found for this user."}

        order.food_rating = rating
        order.delivery_agent_rating = delivery_rating

        db.commit()
        db.refresh(order)

        return {"message": "Ratings submitted successfully.", "Data": order}
    finally:
        db.close()

def getMenu():
    db = SessionLocal()
    restaurants = db.query(Restaurant).filter(
        Restaurant.is_online == True
    )

    result = []
    for restaurant in restaurants:
        item = {
            "name": restaurant.name,
            "available": restaurant.is_online,
            "menu": [
                {
                    "ItemId": menu_item.id,
                    "name": menu_item.name,
                    "price": menu_item.price
                } for menu_item in restaurant.menu_items
            ]
        }
        result.append(item)

    return result