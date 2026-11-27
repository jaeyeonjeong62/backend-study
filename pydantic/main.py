# main2.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Memo(BaseModel):
    title: str
    content: str
    is_important: Optional[bool] = None

@app.post("/memos/")
async def create_memo(memo:Memo):
    return {"memo": memo.model_dump()}

class UserSignup(BaseModel):
    username: str
    email: str
    password: str
    age: int
    marketing_agree: Optional[bool] = False

@app.post("/users/signup")
async def signup(user:UserSignup):
    return {"message": f"{user.username}님, 가입을 환영합니다!",
            "user": {"username": user.username,
                     "email": user.email,
                     "age": user.age,
                     "marketing_agree": user.marketing_agree}}

class Order(BaseModel):
    product_name: str
    price: float
    quantity: int
    coupon_code: Optional[str] = None

@app.post("/orders/")
async def orders(order:Order):
    total_price = order.price*order.quantity
    discount = total_price*0.1 if order.coupon_code == "WELCOME10" else 0
    return {"product_name": order.product_name,
            "quantity": order.quantity,
            "total_price": total_price,
            "discount": discount,
            "final_price": total_price-discount}

class MemoUpdate(BaseModel):
    title: str
    content: str
    is_important: Optional[bool] = None

@app.put("/memos/{memo_id}")
async def update(memo_id:int, memo:MemoUpdate):
    return {"memo_id": memo_id,
            "updated_memo": memo.model_dump()}

class Todo(BaseModel):
    task: str
    priority: Optional[int] = 3
    done: Optional[bool] = False

todo_db = []

@app.post("/todos/")
async def add_todo(todo:Todo):
    todo_db.append(todo.model_dump())
    return {"todo_id": len(todo_db) - 1, "todo": todo_db[-1]}

@app.get("/todos/")
async def todos(skip:int=0, limit:int=10):
    return {"total": len(todo_db),
            "todos": todo_db[skip:skip+limit]}

@app.get("/todos/{todo_id}")
async def todos_more(todo_id:int):
    if 0 <= todo_id < len(todo_db):
        return {"todo_id": todo_id,
                "todo": todo_db[todo_id]}
    return {"error": f"{todo_id}번 할 일이 없습니다."}
