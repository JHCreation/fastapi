import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
# from pydantic.main import 
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form

class FilesUpload(BaseModel):
    file: UploadFile
    name: str
    path: str 
    chunk_number: int
    total_chunks: int
    @classmethod
    def as_form(
        cls,
        file: UploadFile = File(...),  # File to be uploaded
        name: str = Form(...),  # Name of the file
        path: str = Form(...), 
        chunk_number: int = Form(0),  # Current chunk number
        total_chunks: int = Form(1),
    ):
        return cls(file=file, name=name, path=path, chunk_number=chunk_number, total_chunks=total_chunks)
    

class FilesDelete(BaseModel):
    path: str

class FilesDeletes(BaseModel):
    paths: str