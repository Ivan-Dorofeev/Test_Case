import os
import time
import uuid
from typing import Optional

from fastapi import APIRouter, File, HTTPException, UploadFile
from starlette.responses import JSONResponse, StreamingResponse

from app.services.s3_client import initialize_s3, s3_client

router = APIRouter()

# Константы для путей
PUBLIC_IMAGE_PREFIX = "images/public/"
PRIVATE_IMAGE_PREFIX = "images/private/"


def get_unique_filename(filename: str) -> str:
    """Генерация уникального имени файла"""
    ext = filename.split(".")[-1] if "." in filename else ""
    unique_name = f"{uuid.uuid4()}_{int(time.time())}"
    return f"{unique_name}.{ext}" if ext else unique_name


@router.on_event("startup")
async def startup_event():
    """Инициализация при запуске"""
    if not initialize_s3():
        raise Exception("Не удалось инициализировать S3")


@router.post("/documents/upload/", summary="Загрузить документ")
async def upload_document(file: UploadFile = File(...)):
    """Загрузить документ"""
    try:
        file_extension = os.path.splitext(file.filename)[1]
        object_name = f"{uuid.uuid4()}{file_extension}"

        file_content = await file.read()
        uploaded_name = s3_client.upload_file_from_memory(file_content, object_name, file.content_type)

        if uploaded_name:
            file_url = s3_client.get_file_url(object_name)

            return JSONResponse(
                {
                    "message": "Файл успешно загружен",
                    "filename": file.filename,
                    "object_name": object_name,
                    "url": file_url,
                    "content_type": file.content_type,
                }
            )
        else:
            raise HTTPException(status_code=500, detail="Ошибка при загрузке файла")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/documents/{object_name}", summary="Получить URL документа")
async def get_document_url(object_name: str):
    """Получить URL документа"""
    try:
        if not s3_client.file_exists(object_name):
            raise HTTPException(status_code=404, detail="Файл не найден")

        file_url = s3_client.get_file_url(object_name)
        if file_url:
            return {"url": file_url}
        else:
            raise HTTPException(status_code=500, detail="Ошибка при получении URL")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/documents/{object_name}", summary="Удалить документ")
async def delete_document(object_name: str):
    """Удалить документ"""
    try:
        if not s3_client.file_exists(object_name):
            raise HTTPException(status_code=404, detail="Файл не найден")

        if s3_client.delete_file(object_name):
            return {"message": "Файл успешно удален"}
        else:
            raise HTTPException(status_code=500, detail="Ошибка при удалении файла")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/documents/", summary="Получить список всех документов")
async def list_documents():
    """Получить список всех документов"""
    try:
        files = s3_client.list_files()
        return {"count": len(files), "files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/images/upload/", summary="Загрузка изображения")
async def upload_image(file: UploadFile = File(...), is_public: bool = False):
    """Загрузка изображения"""
    try:
        unique_filename = get_unique_filename(file.filename)

        prefix = PUBLIC_IMAGE_PREFIX if is_public else PRIVATE_IMAGE_PREFIX
        object_name = f"{prefix}{unique_filename}"

        file_content = await file.read()

        result = s3_client.upload_file_from_memory(
            data=file_content, object_name=object_name, content_type=file.content_type or "application/octet-stream"
        )

        if result:
            return {
                "filename": unique_filename,
                "is_public": is_public,
                "url": f"/images/public/{unique_filename}" if is_public else f"/images/private/{unique_filename}",
                "message": "Изображение успешно загружено",
            }
        else:
            raise HTTPException(status_code=500, detail="Ошибка загрузки изображения")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при загрузке: {str(e)}") from e


@router.get("/images/public/{filename}", summary="Получение публичного изображения")
async def get_public_image(filename: str):
    """Получение публичного изображения"""
    object_name = f"{PUBLIC_IMAGE_PREFIX}{filename}"

    if not s3_client.file_exists(object_name):
        raise HTTPException(status_code=404, detail="Изображение не найдено")

    try:
        response = s3_client.client.get_object(s3_client.bucket_name, object_name)
        content_type = response.getheader("Content-Type") or "application/octet-stream"

        return StreamingResponse(
            response.stream(), media_type=content_type, headers={"Content-Disposition": f"inline; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении изображения: {str(e)}") from e


@router.get("/images/private/{filename}", summary="Получение подписного URL для приватного изображения")
async def get_private_image_url(filename: str, expires: int = 3600):
    """Получение подписного URL для приватного изображения"""
    object_name = f"{PRIVATE_IMAGE_PREFIX}{filename}"

    if not s3_client.file_exists(object_name):
        raise HTTPException(status_code=404, detail="Изображение не найдено")

    try:
        url = s3_client.get_file_url(object_name, expires)
        if url:
            return {"url": url, "expires_in": expires}
        else:
            raise HTTPException(status_code=500, detail="Не удалось сгенерировать URL")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при генерации URL: {str(e)}") from e


@router.put("/images/{filename}", summary="Замена изображения")
async def replace_image(filename: str, file: UploadFile = File(), is_public: Optional[bool] = None):
    """Замена изображения"""
    try:
        public_object_name = f"{PUBLIC_IMAGE_PREFIX}{filename}"
        private_object_name = f"{PRIVATE_IMAGE_PREFIX}{filename}"

        if s3_client.file_exists(public_object_name):
            current_object_name = public_object_name
            current_is_public = True
        elif s3_client.file_exists(private_object_name):
            current_object_name = private_object_name
            current_is_public = False
        else:
            raise HTTPException(status_code=404, detail="Изображение не найдено")

        new_is_public = is_public if is_public is not None else current_is_public
        prefix = PUBLIC_IMAGE_PREFIX if new_is_public else PRIVATE_IMAGE_PREFIX
        new_object_name = f"{prefix}{filename}"

        if current_object_name != new_object_name:
            s3_client.delete_file(current_object_name)

        file_content = await file.read()
        result = s3_client.upload_file_from_memory(
            data=file_content, object_name=new_object_name, content_type=file.content_type or "application/octet-stream"
        )

        if result:
            return {"filename": filename, "is_public": new_is_public, "message": "Изображение успешно заменено"}
        else:
            raise HTTPException(status_code=500, detail="Ошибка замены изображения")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при замене: {str(e)}") from e


@router.delete("/images/{filename}", summary="Удаление изображения (из любой папки)")
async def delete_image(filename: str):
    """Удаление изображения (из любой папки)"""
    try:
        public_object_name = f"{PUBLIC_IMAGE_PREFIX}{filename}"
        private_object_name = f"{PRIVATE_IMAGE_PREFIX}{filename}"

        if s3_client.file_exists(public_object_name):
            deleted = s3_client.delete_file(public_object_name)
        elif s3_client.file_exists(private_object_name):
            deleted = s3_client.delete_file(private_object_name)
        else:
            raise HTTPException(status_code=404, detail="Изображение не найдено")

        if deleted:
            return {"message": "Изображение успешно удалено"}
        else:
            raise HTTPException(status_code=500, detail="Ошибка удаления изображения")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {str(e)}") from e


@router.get("/images/", summary="Получение списка изображений")
async def list_images(is_public: Optional[bool] = False):
    """Получение списка изображений"""
    try:
        files = []

        if is_public:
            # Получаем публичные изображения
            public_files = s3_client.list_files(prefix=PUBLIC_IMAGE_PREFIX)
            files.extend(
                [
                    {
                        "filename": obj["name"].replace(PUBLIC_IMAGE_PREFIX, ""),
                        "size": obj["size"],
                        "last_modified": obj["last_modified"],
                        "is_public": True,
                        "url": f"/images/public/{obj['name'].replace(PUBLIC_IMAGE_PREFIX, '')}",
                    }
                    for obj in public_files
                ]
            )

        if not is_public:
            private_files = s3_client.list_files(prefix=PRIVATE_IMAGE_PREFIX)
            files.extend(
                [
                    {
                        "filename": obj["name"].replace(PRIVATE_IMAGE_PREFIX, ""),
                        "size": obj["size"],
                        "last_modified": obj["last_modified"],
                        "is_public": False,
                        "url": f"/images/private/{obj['name'].replace(PRIVATE_IMAGE_PREFIX, '')}",
                    }
                    for obj in private_files
                ]
            )

        return {"images": files, "count": len(files)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении списка: {str(e)}") from e


@router.get("/images/info/{filename}", summary="Получение информации об изображении")
async def get_image_info(filename: str):
    """Получение информации об изображении"""
    try:
        public_object_name = f"{PUBLIC_IMAGE_PREFIX}{filename}"
        private_object_name = f"{PRIVATE_IMAGE_PREFIX}{filename}"

        if s3_client.file_exists(public_object_name):
            stat = s3_client.client.stat_object(s3_client.bucket_name, public_object_name)
            info = {
                "filename": filename,
                "size": stat.size,
                "last_modified": stat.last_modified,
                "etag": stat.etag,
                "is_public": True,
                "content_type": stat.content_type,
            }
        elif s3_client.file_exists(private_object_name):
            stat = s3_client.client.stat_object(s3_client.bucket_name, private_object_name)
            info = {
                "filename": filename,
                "size": stat.size,
                "last_modified": stat.last_modified,
                "etag": stat.etag,
                "is_public": False,
                "content_type": stat.content_type,
            }
        else:
            raise HTTPException(status_code=404, detail="Изображение не найдено")

        return info

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении информации: {str(e)}") from e
