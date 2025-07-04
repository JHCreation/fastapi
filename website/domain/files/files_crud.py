import os
from fastapi import status
from fastapi.responses import JSONResponse
from .files_schema import FilesUpload
from fastapi import Depends, status
import shutil
from pathlib import Path
from typing import List

from dotenv import load_dotenv
load_dotenv()
ROOT_PATH= os.environ.get('ROOT_PATH')
UPLOAD_PATH= os.environ.get('UPLOAD_PATH')
UPLOADS_PATH= f"{ROOT_PATH}\\{UPLOAD_PATH}"

def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True, mode=0o777)

async def file_chunk_upload (
        files_upload: FilesUpload,
        CHUNK_PATH: str = '',
        UPLOADS_FILE_PATH: str = '',
        FILE_PATH: str= ''
):
    name= files_upload.name
    file= files_upload.file
    path= files_upload.path
    chunk_number= files_upload.chunk_number
    total_chunks= files_upload.total_chunks
    
    makedirs(Path(UPLOADS_FILE_PATH))
    makedirs(Path(CHUNK_PATH))

    isLast = (int(chunk_number) + 1) == int(
        total_chunks
    )  # Check if it's the last chunk
    file_name = f"{name}_{chunk_number}"

    # Write the chunk to a file in the 'chunks' directory
    with open(f"{CHUNK_PATH}/{file_name}", "wb") as buffer:
        buffer.write(await file.read())
    buffer.close()
  
    if isLast:  # If it's the last chunk, concatenate all chunks into the final file
        with open(f"{UPLOADS_FILE_PATH}/{name}", "wb") as buffer:
            chunk = 0
            while chunk < total_chunks:
                with open(f"{CHUNK_PATH}/{name}_{chunk}", "rb") as infile:
                    buffer.write(infile.read())  # Write the chunk to the final file
                    infile.close()
                os.remove(f"{CHUNK_PATH}/{name}_{chunk}")  # Remove the chunk file
                chunk += 1
        buffer.close()
        return JSONResponse(
            {
                "status": "File success",
                "url": f"{FILE_PATH}/{name}"
            }, status_code=status.HTTP_200_OK
        )

    return JSONResponse(
        {"status": "Chunk success"}, status_code=status.HTTP_200_OK)

def delete_files(path: str):
    dir=Path(path)
    try:
      res= shutil.rmtree(dir)
      return JSONResponse(
        {"status": "success"}, status_code=status.HTTP_200_OK)
    except:
      print('에러발생')
      return JSONResponse(
        {"status": "fail"}, status_code=status.HTTP_200_OK)


def delete_multiple_files(root_path:str, paths:List[str]):
    res= []
    for p in paths:
        delete_path= f"{root_path}/{p}"
        # print(delete_path)
        res.append(delete_files(delete_path))
    
    return { "status": "success", "result": res }, 
    
