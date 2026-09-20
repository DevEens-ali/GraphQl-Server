from fastapi import FastAPI, Request
import strawberry
from strawberry.fastapi import GraphQLRouter
from models import User as UserModel
import jwt
import asyncio
from strawberry.types import Info
from datetime import datetime, timedelta, timezone
from database import SessionLocal
from models import Product as ProductModel
from typing import AsyncGenerator

import bcrypt
subscribers: set[asyncio.Queue] = set()


def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    return hashed_password.decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

SECRET_KEY = "my_super_secret_key"
ALGORITHM = "HS256"


def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")

    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

def get_current_user_id(request: Request) -> int:
    token = get_token(request)

    payload = verify_token(token)

    user_id = payload.get("sub")

    if user_id is None:
        raise Exception("Invalid token")

    return int(user_id)


@strawberry.type
class User:
    id: int
    name: str
    email: str


@strawberry.type
class Product:
    id: int
    name: str
    description: str
    price: float
    quantity: int


@strawberry.input
class ProductInput:
    name: str
    description: str
    price: float
    quantity: int

@strawberry.input
class UserInput:
    name: str
    email: str
    password: str

@strawberry.input
class LoginInput:
    email: str
    password: str


@strawberry.type
class Query:
    
    @strawberry.field
    def me(self, info: Info) -> User:
        request = info.context["request"]

        user_id = get_current_user_id(request)

        db = SessionLocal()

        user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

        db.close()

        if user is None:
            raise Exception("User not found")

        return User(
        id=user.id,
        name=user.name,
        email=user.email
    )

    @strawberry.field
    def hello(self) -> str:
        return "Hello GraphQL!"

    @strawberry.field
    def products(self) -> list["Product"]:

        db = SessionLocal()

        products = db.query(ProductModel).all()

        db.close()

        return [
            Product(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
                quantity=product.quantity
            )
            for product in products
        ]
    @strawberry.field()
    def product(self , id:int) -> Product | None:
        db = SessionLocal()
        
        product = db.query(ProductModel).filter(
        ProductModel.id == id
        ).first()

        db.close()

        if product is None:
            return None

        return Product(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity
    )
        
    @strawberry.field
    def users(self) -> list["User"]:

        db = SessionLocal()

        users = db.query(UserModel).all()

        db.close()

        return [
            User(
            id=user.id,
            name=user.name,
            email=user.email
        )
        for user in users
    ]
@strawberry.field
def user(self, id: int) -> User | None:

        db = SessionLocal()

        user = db.query(UserModel).filter(
        UserModel.id == id
    ).first()

        db.close()

        if user is None:
            return None

        return User(
        id=user.id,
        name=user.name,
        email=user.email
    )
@strawberry.type
class LoginResponse:
    access_token: str

def get_token(request: Request) -> str:
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise Exception("Authentication required")

    if not authorization.startswith("Bearer "):
        raise Exception("Invalid authorization header")

    token = authorization.replace("Bearer ", "", 1)

    return token


@strawberry.type
class Mutation:
    
    
    

    @strawberry.mutation
    async def create_product(self, product: ProductInput) -> Product:
        db = SessionLocal()

        new_product = ProductModel(
            name=product.name,
            description=product.description,
            price=product.price,
            quantity=product.quantity
    )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        db.close()

        new_product_data = Product(
            id=new_product.id,
            name=new_product.name,
            description=new_product.description,
            price=new_product.price,
            quantity=new_product.quantity
        )

        for queue in subscribers:
            await queue.put(new_product_data)

        return new_product_data
    
    
    
    @strawberry.mutation
    def update_product(
    self,
    id: int,
    product: ProductInput
    ) -> Product | None:

        db = SessionLocal()

        existing_product = db.query(ProductModel).filter(
        ProductModel.id == id
    ).first()

        if existing_product is None:
            db.close()
            return None

        existing_product.name = product.name
        existing_product.description = product.description
        existing_product.price = product.price
        existing_product.quantity = product.quantity

        db.commit()
        db.refresh(existing_product)

        db.close()

        return Product(
        id=existing_product.id,
        name=existing_product.name,
        description=existing_product.description,
        price=existing_product.price,
        quantity=existing_product.quantity
    )
    @strawberry.mutation
    def delete_product(self, id: int) -> bool:

        db = SessionLocal()

        existing_product = db.query(ProductModel).filter(
        ProductModel.id == id
    ).first()

        if existing_product is None:
            db.close()
            return False

        db.delete(existing_product)

        db.commit()

        db.close()

        return True
    @strawberry.mutation
    def register_user(self, user: UserInput) -> User:
        db = SessionLocal()

        hashed_password = hash_password(user.password)

        new_user = UserModel(
            name=user.name,
            email=user.email,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.close()

        return User(
            id=new_user.id,
            name=new_user.name,
            email=new_user.email
        )

    @strawberry.mutation
    def login_user(self, login: LoginInput) -> LoginResponse:
        db = SessionLocal()

        user = db.query(UserModel).filter(
            UserModel.email == login.email
        ).first()

        if user is None:
            db.close()
            raise Exception("Invalid email or password")

        if not verify_password(login.password, user.password):
            db.close()
            raise Exception("Invalid email or password")

        token = create_access_token(user.id)

        db.close()

        return LoginResponse(
            access_token=token
        )

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def product_created(
        self
    ) -> AsyncGenerator[Product, None]:

        queue = asyncio.Queue()
        subscribers.add(queue)

        try:
            while True:
                product = await queue.get()
                yield product

        finally:
            subscribers.remove(queue)
    

    



schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)

# async def get_context(request: Request):
#     return {
#         "request": request
#     }

graphql_app = GraphQLRouter(schema)

app = FastAPI()

app.include_router(
    graphql_app,
    prefix="/graphql"
)