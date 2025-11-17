import os
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Base, User, Audio
from schemas import Token, UserOut, AudioOut, AudioCreate
from auth import get_yandex_user, create_access_token, get_current_user, oauth2_scheme, init_db, get_db
from config import settings



# Инициализация приложения
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Эндпоинты
@app.post("/auth/yandex", response_model=Token)
async def login_yandex(code: str, db: AsyncSession = Depends(get_db)):
    yandex_user = await get_yandex_user(code)
    print('yandex_user =',yandex_user)
    if not yandex_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate Yandex credentials"
        )

    async with db as session:
        result = await session.execute(
            select(User).where(User.yandex_id == yandex_user["id"])
        )
        user = result.scalars().first()

        if not user:
            user = User(
                email=yandex_user["default_email"],
                yandex_id=yandex_user["id"]
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}


@app.post("/token/refresh", response_model=Token)
async def refresh_token(current_user: UserOut = Depends(get_current_user)):
    access_token = create_access_token(data={"sub": current_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserOut)
async def read_user_me(current_user: UserOut = Depends(get_current_user)):
    return current_user


@app.post("/audio/", response_model=AudioOut)
async def upload_audio(
        file: UploadFile,
        filename: str,
        current_user: UserOut = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    file_ext = os.path.splitext(file.filename)[1]
    unique_name = f"{current_user.id}_{int(datetime.now().timestamp())}{file_ext}"
    filepath = os.path.join(settings.AUDIO_STORAGE_PATH, unique_name)

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    async with db as session:
        audio = Audio(
            filename=filename,
            filepath=filepath,
            owner_id=current_user.id
        )
        session.add(audio)
        await session.commit()
        await session.refresh(audio)
        return audio


@app.get("/audio/", response_model=list[AudioOut])
async def get_audio_list(
        current_user: UserOut = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    async with db as session:
        result = await session.execute(
            select(Audio).where(Audio.owner_id == current_user.id)
        )
        return result.scalars().all()


@app.delete("/users/{user_id}")
async def delete_user(
        user_id: int,
        current_user: UserOut = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Forbidden")

    async with db as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await session.delete(user)
        await session.commit()
        return {"message": "User deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)