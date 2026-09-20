# GraphQL Server

A backend GraphQL API built with **Python, FastAPI, Strawberry GraphQL, SQLAlchemy, MySQL, and JWT Authentication**.

This project was developed as part of an internship task to practice GraphQL queries, mutations, subscriptions, database integration, and authentication.

## 🚀 Features

- GraphQL API using Strawberry
- FastAPI integration
- MySQL database
- SQLAlchemy ORM
- User and Product resources
- GraphQL Queries
- GraphQL Mutations
- Product CRUD operations
- User registration
- Password hashing with bcrypt
- JWT authentication
- Protected `me` query
- Real-time GraphQL subscriptions
- WebSocket support

## 🛠️ Technologies

- Python
- FastAPI
- Strawberry GraphQL
- SQLAlchemy
- MySQL
- PyMySQL
- JWT
- bcrypt
- Uvicorn
- WebSockets

## 📁 Project Structure

```text
graphql-server/
│
├── main.py
├── models.py
├── database.py
├── requirements.txt
├── notes.md
├── .gitignore
└── README.md

# GraphQL Server

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/DevEens-ali/GraphQl-Server.git
   ```

2. **Open the project**
   ```bash
   cd GraphQl-Server
   ```

3. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

4. **Activate virtual environment**
   * **Windows:**
     ```bash
     venv\Scripts\activate
     ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🗄️ Database Setup

1. **Create a MySQL database:**
   ```sql
   CREATE DATABASE graphql_db;
   ```

2. **Update the database connection** in `database.py` according to your MySQL credentials.
   * **Example:**
     ```python
     DATABASE_URL = "mysql+pymysql://root:YOUR_PASSWORD@localhost/graphql_db"
     ```

## ▶️ Run the Server

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The GraphQL interface will be available at: [http://127.0.0.1:8000/graphql](http://127.0.0.1:8000/graphql)

## 📌 GraphQL Operations

### Query Products
```graphql
query {
  products {
    id
    name
    description
    price
    quantity
  }
}
```

### Query Users
```graphql
query {
  users {
    id
    name
    email
  }
}
```

### Create Product
```graphql
mutation {
  createProduct(
    product: {
      name: "Laptop"
      description: "Gaming Laptop"
      price: 1200.0
      quantity: 5
    }
  ) {
    id
    name
    description
    price
    quantity
  }
}
```

### Register User
```graphql
mutation {
  registerUser(
    user: {
      name: "Anees"
      email: "anees@example.com"
      password: "password123"
    }
  ) {
    id
    name
    email
  }
}
```

### Login
```graphql
mutation {
  loginUser(
    login: {
      email: "anees@example.com"
      password: "password123"
    }
  ) {
    accessToken
  }
}
```
*The returned access token can be used as a Bearer token for protected operations.*

### Protected User Query
```graphql
query {
  me {
    id
    name
    email
  }
}
```
Add the JWT token in the GraphQL client's authorization settings:
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## 🔄 Real-Time Subscription

The project supports real-time product creation notifications using GraphQL subscriptions and WebSockets.

```graphql
subscription {
  productCreated {
    id
    name
    description
    price
    quantity
  }
}
```
*When a new product is created, connected subscribers receive the new product automatically.*

## 🔑 Authentication

Authentication is implemented using:
* `bcrypt` password hashing
* JWT access tokens
* Protected GraphQL operations
* Bearer token authentication

*Note: Passwords are never stored as plain text.*

## 📚 Learning Objectives

This project helped practice:
* GraphQL schema design
* Queries and resolvers
* Mutations CRUD operations
* SQLAlchemy ORM
* MySQL integration
* Password security
* JWT authentication
* WebSocket communication
* Real-time GraphQL subscriptions
* FastAPI integration

## 👨‍💻 Author

**Anees Ali**  
GitHub: [DevEens-ali](https://github.com/DevEens-ali)
