from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from pydantic import BaseModel

templates = Jinja2Templates(directory="templates")
app = FastAPI()
users = []

ant_id = Annotated[int, Path(ge=1, le=100, description="Enter User ID", example="1")]
ant_name = Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")]
ant_age = Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]


class User(BaseModel):
    id: int = None
    username: str
    age: int


users.append(User(id=1, username="Петров", age=24))
users.append(User(id=2, username="Иванов", age=28))
users.append(User(id=3, username="Сидоров", age=38))


@app.get('/')
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get('/users/{user_id}')
async def get_user(request: Request, user_id: ant_id) -> HTMLResponse:
    user = next((x for x in users if x.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User was not found")

    return templates.TemplateResponse("users.html", {"request": request, "user": user})


@app.post('/user/{username}/{age}')
async def add_user(username: ant_name, age: ant_age) -> User:
    user_id = max(users, key=lambda k: k.id).id + 1 if len(users) else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: ant_id, username: ant_name, age: ant_age) -> User:
    user = next((x for x in users if x.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User was not found")

    user.username = username
    user.age = age
    return user


@app.delete('/user/{user_id}')
async def del_user(user_id: ant_id) -> User:
    user = next((x for x in users if x.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User was not found")

    users.remove(user)
    return user
