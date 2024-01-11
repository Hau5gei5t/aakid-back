from datetime import timedelta
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, Token, get_current_active_user

import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# @app.get("/test", response_model=schemas.User)
# async def get_data(db: Session = Depends(get_db)):
#     return db.query(models.User).all()
#
#
# @app.post("/test", response_model=schemas.User)
# async def create_user(email:str, db: Session = Depends(get_db)):
#     db_user = models.User(
#         email=email
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
# @app.post("/test/{id}")
# async def create_role(id:int, db: Session = Depends(get_db)):
#     db_role = models.Role(
#         role_name="sad1"
#     )
#     db.query(models.User).filter(models.User.id == id).first().role = db_role
#     db.add(db_role)
#     db.commit()
#     db.refresh(db_role)
#     return db_role
# @app.post("/token", response_model=Token)
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
#
# @app.get("/users/me/", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return current_user
