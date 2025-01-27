import os
from datetime import timedelta, datetime
from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from meme.database import get_db
from meme.domain.user import user_crud, user_schema
from meme.domain.user.user_crud import pwd_context
from pydantic import ValidationError

from corenzohouse.route import router, router2
from corenzohouse.database import get_db
print('corenzo-user_router', os.environ.get('DB_NAME'))


@router.get("/test", 
            #  status_code=status.HTTP_204_NO_CONTENT
             )
def user_test(request: Request):
    return {'user test': str(request.base_url)}

@router2.post("/call") 
def user_call(request: Request, 
              id: user_schema.User,
              db: Session = Depends(get_db),
              ):
    user = user_crud.get_user(db, id.userid)
    print(user, 'result')
    res=''
    if( user ):
        userObj= user.__dict__
        res=userObj['userid']
        print(userObj['userid'])
    return {'user call2': f"{res}  {str(request.base_url)}sss"}
