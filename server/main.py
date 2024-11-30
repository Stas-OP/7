from fastapi import FastAPI, HTTPException
from .schemas import UserBase, TokenResponse
from .auth import *

app = FastAPI()

@app.post("/register", response_model=TokenResponse)
async def register(user: UserBase):
    users = load_users()
    if user.username in users:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    user_id = generate_id()
    token = generate_token()
    users[user.username] = {
        "id": user_id,
        "password_hash": get_password_hash(user.password),
        "token": token
    }
    save_users(users)
    return TokenResponse(id=user_id, token=token, message="Регистрация успешна")

@app.post("/login", response_model=TokenResponse)
async def login(user: UserBase):
    users = load_users()
    if user.username not in users:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    
    stored_user = users[user.username]
    if not verify_password(user.password, stored_user["password_hash"]):
        raise HTTPException(status_code=400, detail="Неверный пароль")
    
    return TokenResponse(id=stored_user["id"], token=stored_user["token"], 
                        message="Вход выполнен успешно")

@app.patch("/change-password", response_model=TokenResponse)
async def change_password(old_password: str, new_password: str, token: str):
    users = load_users()
    user_data = None
    username = None
    
    for uname, data in users.items():
        if data["token"] == token:
            user_data = data
            username = uname
            break
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    
    if not verify_password(old_password, user_data["password_hash"]):
        raise HTTPException(status_code=400, detail="Неверный старый пароль")
    
    new_token = generate_token()
    users[username]["password_hash"] = get_password_hash(new_password)
    users[username]["token"] = new_token
    save_users(users)
    
    return TokenResponse(id=user_data["id"], token=new_token, 
                        message="Пароль успешно изменен") 