from typing import List

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse

from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security
from fastapi.encoders import jsonable_encoder

from meme.database import get_db
from meme.domain.category import category_crud, category_schema
from meme.domain._comm import comm_crud, comm_schema
from pydantic import ValidationError
from sqlalchemy.orm import Session
from meme.domain.user.user_auth import api_bearer_token
import json

import os
import uuid
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(
    prefix="/api/files",
)

def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True, mode=0o777)
from meme.domain.files import files_crud
from meme.domain.files.files_schema import FilesUpload, FilesDelete, FilesDeletes

ROOT_PATH= os.environ.get('ROOT_PATH')
UPLOAD_PATH= os.environ.get('UPLOAD_PATH')
UPLOADS_PATH= f"{ROOT_PATH}\\{UPLOAD_PATH}"

@router.post("/uploads")
async def upload_file( form_data: FilesUpload = Depends(FilesUpload.as_form),
                      api_key: str = Security(api_bearer_token) ):
    """
    Handles file uploads with chunked transfer
    (if total_chunks > 1) or single-file upload.

    Raises:
        HTTPException: If a validation error occurs
        (e.g., missing data, invalid file size).
    """
      # Generate a unique file name for the chunk
    FILE_PATH= form_data.path
    CHUNK_PATH= f"{UPLOADS_PATH}/temp"
    UPLOADS_FILE_PATH= f"{UPLOADS_PATH}/{FILE_PATH}"
    

    return await files_crud.file_chunk_upload(
        files_upload=form_data, CHUNK_PATH=CHUNK_PATH, UPLOADS_FILE_PATH=UPLOADS_FILE_PATH, FILE_PATH=FILE_PATH
    )
    
@router.post("/update")
async def upload_file( form_data: FilesUpload = Depends(FilesUpload.as_form), 
                      api_key: str = Security(api_bearer_token) ):
    print('update', form_data.path)
    CHUNK_PATH= f"{UPLOADS_PATH}/temp"
    UPLOADS_FILE_PATH= f"{UPLOADS_PATH}/{form_data.path}"
    files_delete= { 'path': UPLOADS_FILE_PATH }
    files_crud.delete_files(files_delete=files_delete)

    return await files_crud.file_chunk_upload(
        files_upload=form_data, CHUNK_PATH=CHUNK_PATH, UPLOADS_FILE_PATH=UPLOADS_FILE_PATH 
    )

@router.delete("/delete")
def delete_files(files_delete: FilesDelete, api_key: str = Security(api_bearer_token)):
    delte_path=files_delete.model_dump(exclude_unset=True)
    # print(delte_path['path'])
    path= delte_path['path'].replace("/", "\\")
    # print(path)
    delete_path= f"{UPLOADS_PATH}/{path}"
    return files_crud.delete_files(delete_path)

@router.delete("/deletes")
def delete_files(files_delete: FilesDeletes, api_key: str = Security(api_bearer_token)):
    print(files_delete)
    # return
    delte_path=files_delete.model_dump(exclude_unset=True)
    paths= json.loads(delte_path['paths'])
    # print(paths)

    res= []
    for p in paths:
        # print(path)
        path= p.replace("/", "\\")
        delete_path= f"{UPLOADS_PATH}/{path}"
        print(delete_path)
        res.append(files_crud.delete_files(delete_path))
    
    print('res', res)
    return res












@router.post("/files/")
async def create_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@router.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    UPLOAD_DIR = "./photo"
    makedirs(UPLOAD_DIR)
    content = await files.read()
    filename = f"{str(uuid.uuid4())}.jpg"  # uuid로 유니크한 파일명으로 변경
    with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
        fp.write(content)  # 서버 로컬 스토리지에 이미지 저장 (쓰기)

    return {"filenames": [file.filename for file in files]}


@router.post("/uploadfile/")
async def create_upload_files(file: UploadFile):
    UPLOAD_DIR = "./photo"
    makedirs(UPLOAD_DIR)
    content = await file.read()
    filename = f"{str(uuid.uuid4())}.jpg"  # uuid로 유니크한 파일명으로 변경
    with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
        fp.write(content)  # 서버 로컬 스토리지에 이미지 저장 (쓰기)

    return {"filenames": [file.filename for file in file]}



from tempfile import NamedTemporaryFile
from typing import IO

from fastapi import FastAPI, File, UploadFile

async def save_file(file: IO):
    # s3 업로드라고 생각해 봅시다. delete=True(기본값)이면
    # 현재 함수가 닫히고 파일도 지워집니다.
    with NamedTemporaryFile("wb", delete=False) as tempfile:
        tempfile.write(file.read())
        return tempfile.name


@router.post("/file/store")
async def store_file(file: UploadFile = File(...)):
    path = await save_file(file.file)
    print(path)
    return {"filepath": path}



import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable

from fastapi import UploadFile


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


def handle_upload_file(
    upload_file: UploadFile, handler: Callable[[Path], None]
) -> None:
    tmp_path = save_upload_file_tmp(upload_file)
    try:
        handler(tmp_path)  # Do something with the saved temp file
    finally:
        tmp_path.unlink()  # Delete the temp file





import asyncio
import os
import random

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse



def supermakedirs(path, mode):
    if not path or os.path.exists(path):
        return []
    (head, tail) = os.path.split(path)
    res = supermakedirs(head, mode)
    os.mkdir(path)
    os.chmod(path, mode)
    res += [path]
    return res

class ResponseContext:
    """Response context."""

    def __init__(self) -> None:
        self.data = None
        self.is_success = False
        self.error_message: str | None = None

@router.post("/upload-chunks/")
async def upload_chunks(id: str, file_name: str, file: UploadFile = File(...)):
    """Upload chunks."""
    print(f"Uploading chunk {id} for {file_name}")
    print(f"File size: {file.size}")
    print(f"File Name: {file.filename}")
    # print(os.path.realpath(__file__))
    # print(os.getcwd())
    # return
    # chunk_path= os.path.join(os.getcwd(),"temp", f"{id}_{file_name}")
    chunk_path = f"./temp/{id}_{file_name}"
    makedirs(chunk_path)

    response_context = ResponseContext()
    try:
        with open(os.path.join(chunk_path, f"{file_name}.jpg"), "wb") as buffer:
            buffer.write(await file.read())
            response_context.is_success = True

        # content = await file.read()
        # filename = f"{str(uuid.uuid4())}.jpg"  # uuid로 유니크한 파일명으로 변경
        # with open(os.path.join(chunk_path, filename), "wb") as fp:
        #     fp.write(content)  # 서버 로컬 스토리지에 이미지 저장 (쓰기)
        #     response_context.is_success = True

    except Exception as ex:
        response_context.error_message = str(ex)
        response_context.is_success = False

    # Sleep for random time to simulate network latency
    # await asyncio.sleep(random.randint(1, 5))

    return JSONResponse(content=response_context.__dict__)


@router.post('/upload-complete/')
async def upload_complete(file_name: str):
    """Upload complete."""
    response_context = ResponseContext()

    try:
        temp_path = "temp/"
        new_path = f"files/{file_name}"
        chunk_files = sorted(
            [file for file in os.listdir(
                temp_path) if file.endswith(file_name)],
            key=lambda x: int(x.split('_')[0])
        )

        with open(new_path, 'wb') as buffer:
            for file in chunk_files:
                chunk_path = os.path.join(temp_path, file)
                with open(chunk_path, 'rb') as chunk_buffer:
                    buffer.write(chunk_buffer.read())
                os.remove(chunk_path)
        response_context.is_success = True
    except Exception as ex:
        response_context.error_message = str(ex)
        response_context.is_success = False

    return JSONResponse(content=response_context.__dict__)




