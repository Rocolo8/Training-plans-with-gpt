# backend/app/auth/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.user import User
from app.database import get_db
from app.auth.password import get_password_hash, verify_password
import jwt
from datetime import timedelta, datetime

SECRET_KEY = 'your_secret_key_here'  # Cambia esto por una clave secreta real
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


def create_access_token(email: str, user_id: int, expires_delta: timedelta = None):
    to_encode = {"sub": email, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




# toma los datos del usuario, encripta la contraseña y crea un nuevo registro de usuario en la base de datos.
@router.post('/register')
def register(user_data: dict, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user_data['password'])
    new_user = User(email=user_data['email'], password_hash=hashed_password, name=user_data['name'],
                    age=user_data['age'], weight=user_data['weight'], height=user_data['height'])
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'message': 'User registered successfully'}

# verifica si el correo electrónico y la contraseña proporcionados coinciden con un usuario registrado. Si es así, genera un token de acceso utilizando JWT y lo devuelve al cliente.
from pydantic import BaseModel

class LoginData(BaseModel):
    username: str
    password: str

@router.post('/login')
def login(login_data: LoginData, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(email=user.email, user_id=user.id, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}

@router.post('/logout')
def logout():
    # Implementa la lógica de cierre de sesión aquí.
    pass
