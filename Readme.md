# 🍔 Food Delivery Microservices System

This repository contains a full-stack microservices-based backend system for a food delivery platform. The system is divided into three core services:

* **User Service** (`user-service`)
* **Restaurant Service** (`restaurant-service`)
* **Delivery Agent Service** (`delivery-agent-service`)

All services share a common `shared` module for database models and configuration.

---

## 📁 Project Structure

```
.
├── user-service
│   ├── crud.py
│   └── main.py
│
├── restaurant-service
│   ├── crud.py
│   └── main.py
│
├── delivery-service
│   ├── crud.py
│   └── main.py
│
└── shared
    └── database.py
```

---

# 🚀 API Routes

## 🔐 User Service (`/user-service`)

### ➕ Register a User

* **POST** `/register`

```json
{
  "name": "John",
  "email": "john@example.com"
}
```

### 🍽️ Place an Order

* **POST** `/placeOrder`

```json
{
  "user_id": 1,
  "restaurant_id": 2,
  "menu_ids": [1, 3]
}
```

### ⭐ Rate Order

* **POST** `/rateOrder`

```json
{
  "user_id": 1,
  "order_id": 3,
  "food_rating": 4,
  "delivery_agent_rating": 5
}
```

### 📦 Get All Orders

* **GET** `/getAllOrders/{user_id}`

---

## 🏪 Restaurant Service (`/restaurant-service`)

### ➕ Add Restaurant

* **POST** `/addRestaurant`

```json
{
  "name": "Pizza Palace",
  "is_online": true,
  "userId": 1
}
```

### 🧾 Add Menu Item

* **POST** `/addItemsinMenu`

```json
{
  "userId": 1,
  "restaurantId": 2,
  "name": "Pepperoni Pizza",
  "price": 599
}
```

### ✏️ Update Menu Item

* **POST** `/updateMenuItem/{item_id}`

```json
{
  "userId": 1,
  "restaurantId": 2,
  "name": "Veg Pizza",
  "price": 499
}
```

### 📜 Get All Orders for Restaurant

* **GET** `/getAllOrders/{restaurant_id}`

### ✅ Update Restaurant Online Status

* **POST** `/updateStatus`

```json
{
  "status": true,
  "restaurantId": 2,
  "userId": 1
}
```

### 🚚 Update Order Status (Accept/Reject)

* **POST** `/updateOrder`

```json
{
  "order_id": 3,
  "restaurant_id": 2,
  "status": "accepted"
}
```

### 🌟 View Restaurant Ratings

* **GET** `/getRestaurantRatings/{restaurant_id}`

---

## 🛵 Delivery Agent Service (`/delivery-service`)

### 📝 Register Delivery Agent

* **POST** `/registerAgent`

```json
{
  "name": "Alex",
  "status": true
}
```

### 📥 Get All Orders Assigned

* **GET** `/getallorders/{agentId}`

### ✅ Update Order Status (Delivered)

* **POST** `/updateorderStatus`

```json
{
  "order_id": 3,
  "agent_id": 1,
  "status": "delivered"
}
```

### 📶 Update Availability

* **POST** `/updateStatus`

```json
{
  "agent_id": 1,
  "status": false
}
```

### ⭐ View Delivery Ratings

* **GET** `/getmyratings/{agent_id}`

---

# 🔗 Shared Module

The `shared` directory contains the database connection and models, reused by all services.

---

# ⚙️ Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repo.git
```

2. Set up virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate 
# For Windows
# ./venv/bin/activate
pip install -r requirements.txt
```


3. Create a .env file, and store your DATABASE_URL in it.

4. Run each service in separate terminals:

```bash
# Terminal 1
uvicorn user-service.main:app --reload --port 8001

# Terminal 2
uvicorn restaurant-service.main:app --reload --port 8002

# Terminal 3
uvicorn delivery-agent-service.main:app --reload --port 8003
```

---

# Deployed URLs
1. [User-Service]( https://kraftbase-assignment.onrender.com/)
2. [Restaurant-Service](https://restaurant-service-kraftbase.onrender.com/)
3. [Delivery-Agent-Service](https://delivery-agent-service-kraftbase.onrender.com/)

# Postman APIs
I have attached the postman requests collection json in the Github Repo. Kindly import it in Postman and run the APIs.

# Docker
I have created a Dockerfile for User-Service.
For running the User-Service server
```bash
docker build -t user-service .
docker run -p 8000:8000 user-service
```

For running the Restaurant-Service Server
```bash
docker build -t restaurant-service .
docker run -p 8001:8000 restaurant-service uvicorn restaurant-service.main:app --host 0.0.0.0 --port 8000
```

For running the Delivery-Agent-Service Server 
```bash
docker build -t delivery-agent-service .
docker run -p 8002:8000 delivery-agent-service uvicorn delivery-agent-service.main:app --host 0.0.0.0 --port 8000
```


For creating Docker Images and Running Docker Container, please ensure you have Docker installed in your system and Docker Desktop instance is running.
---
