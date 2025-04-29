from fastapi import FastAPI, HTTPException, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from schemas import UserBase, TokenResponse, RequestHistory, CipherRequest, CipherResponse, TextRequest, TextResponse
from auth import *
from cipher import encrypt, decrypt
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_user_by_token(token: str):
    users = load_users()
    for data in users.values():
        if data["token"] == token:
            return data
    return None

@app.middleware("http")
async def log_requests(request: Request, call_next):
    if request.headers.get("Authorization"):
        token = request.headers["Authorization"]
        users = load_users()
        user_id = None
        for user_data in users.values():
            if user_data["token"] == token:
                user_id = user_data["id"]
                break
        if user_id:
            add_request_to_history(user_id, request.method, str(request.url.path))
    response = await call_next(request)
    return response

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

@app.get("/all-users")
async def get_all_users():
    users = load_users()
    return list(users.keys())

@app.get("/history", response_model=List[RequestHistory])
async def get_history(token: str):
    users = load_users()
    user_data = None
    for data in users.values():
        if data["token"] == token:
            user_data = data
            break
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    
    return get_user_history(user_data["id"])

@app.delete("/history")
async def delete_history(token: str):
    users = load_users()
    user_data = None
    for data in users.values():
        if data["token"] == token:
            user_data = data
            break
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    
    clear_user_history(user_data["id"])
    return {"message": "История запросов очищена"}

@app.post("/encrypt", response_model=CipherResponse)
async def encrypt_text(request: CipherRequest, token: str):
    users = load_users()
    user_data = None
    for data in users.values():
        if data["token"] == token:
            user_data = data
            break
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    
    try:
        result = encrypt(request.text, request.key)
        return CipherResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/decrypt", response_model=CipherResponse)
async def decrypt_text(request: CipherRequest, token: str):
    users = load_users()
    user_data = None
    for data in users.values():
        if data["token"] == token:
            user_data = data
            break
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    
    try:
        result = decrypt(request.text, request.key)
        return CipherResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/texts", response_model=TextResponse)
async def add_new_text(request: TextRequest, token: str):
    users = load_users()
    user_data = None
    for data in users.values():
        if data["token"] == token:
            user_data = data
            break
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    
    text_entry = add_text(user_data["id"], request.text)
    if not text_entry:
        raise HTTPException(status_code=400, detail="Не удалось сохранить текст")
    
    return TextResponse(
        id=text_entry["id"],
        text=text_entry["text"],
        timestamp=datetime.fromisoformat(text_entry["timestamp"])
    )

@app.get("/texts", response_model=List[TextResponse])
async def get_texts(token: str):
    users = load_users()
    user_data = None
    for data in users.values():
        if data["token"] == token:
            user_data = data
            break
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    
    texts = get_user_texts(user_data["id"])
    return [
        TextResponse(
            id=text["id"],
            text=text["text"],
            timestamp=datetime.fromisoformat(text["timestamp"])
        )
        for text in texts
    ]

@app.get("/texts/{text_id}", response_model=TextResponse)
async def get_text(text_id: int, token: str):
    users = load_users()
    user_data = None
    for data in users.values():
        if data["token"] == token:
            user_data = data
            break
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    
    text = get_text_by_id(user_data["id"], text_id)
    if not text:
        raise HTTPException(status_code=404, detail="Текст не найден")
    
    return TextResponse(
        id=text["id"],
        text=text["text"],
        timestamp=datetime.fromisoformat(text["timestamp"])
    )

@app.delete("/texts/{text_id}")
async def delete_text_by_id(text_id: int, token: str):
    users = load_users()
    user_data = None
    for data in users.values():
        if data["token"] == token:
            user_data = data
            break
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    
    if not delete_text(user_data["id"], text_id):
        raise HTTPException(status_code=404, detail="Текст не найден")
    
    return {"message": "Текст успешно удален"}

@app.patch("/texts/{text_id}", response_model=TextResponse)
async def update_existing_text(text_id: int, request: TextRequest, token: str):
    users = load_users()
    user_data = None
    for data in users.values():
        if data["token"] == token:
            user_data = data
            break
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    
    updated_text = update_text(user_data["id"], text_id, request.text)
    if not updated_text:
        raise HTTPException(status_code=404, detail="Текст не найден или не принадлежит пользователю")
    
    return TextResponse(
        id=updated_text["id"],
        text=updated_text["text"],
        timestamp=datetime.fromisoformat(updated_text["timestamp"])
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)