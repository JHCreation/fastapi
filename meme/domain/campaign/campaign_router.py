from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends

from meme.database import get_db
from meme.domain.campaign import campaign_crud, campaign_schema
from meme.domain.user.user_crud import pwd_context
from pydantic import ValidationError
from sqlalchemy.orm import Session

from meme.domain.user.user_auth import ALGORITHM, REFRESH_KEY_NAME, REFRESH_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, create_refresh_token, set_cookie, delete_cookie

router = APIRouter(
    prefix="/api/campaign",
)
# print(oauth2_scheme.__dir__())

@router.post("/create")
def campaign_create(
    item: campaign_schema.CampaignCreate,
    # item: campaign_schema.CampaignCreate= Depends(),
    db: Session = Depends(get_db)
):  
    campaign_crud.create_campaign(db, item)
    return {"message": "Hello World"}