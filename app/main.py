from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from api.routes.routes import task_router
from tortoise.contrib.fastapi import register_tortoise
from api.models.models import User
from auth.auth import get_current_user
from auth.auth_util import create_access_token, get_password_hash, verify_password
from data import user_db

app = FastAPI()
app.include_router(task_router)

oAuth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register")
async def register_user(username: str, password: str):
    if username in user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_password = get_password_hash(password)
    user_db[username] = {"username": username, "password": hashed_password}
    return {"msg": "User registered successfully"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "email": current_user.email}

register_tortoise(
    app=app,
    db_url="postgres://postgres:task.db",
    add_exception_handlers=True,
    generate_schemas=True,
    modules={"models": ["api.models.models"]},
)

@app.get("/")
def index():
    return {"status": "Task tracker"}