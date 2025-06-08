from passlib.context import CryptContext
from sqlalchemy.orm import Session
from meme.domain.campaign.campaign_schema import CampaignCreate
from meme.models import Campaign
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

schema= CampaignCreate.model_json_schema()

def myfunc(schema=None, **kwargs):
    # print(kwargs)
    # return
    schemaDict= schema.model_dump()
    # print(schemaDict)
    # print(schema.dict())
    # return
    obj={}
    for key in kwargs:
        obj[key]= schemaDict[key]
        print( obj[key], schemaDict[key] )
    # print(obj)
    return obj

# mydict = {'person1': "Faraz", 'person2': "Rukhshan", 'person3': "Muzammil"}


def create_campaign(db: Session, campaign_create: CampaignCreate):
    # print(campaign_create)
    # param= myfunc(campaign_create, **schema['properties'])
    param= campaign_create.model_dump()
    obj={}
    for key in param:
        obj[key]= param[key]
        # print(param[key])
    print(obj)
    return
    # print(param)
    # return 
    db_campaign = Campaign(**campaign_create.model_dump())
    """ db_campaign = Campaign(biz_title=campaign_create.biz_title,
                   channel=campaign_create.channel,
                   type=campaign_create.type,
                   category=campaign_create.category,
                   content=campaign_create.content,
                   address=campaign_create.address,
                   phone=campaign_create.phone,
                   msg=campaign_create.msg,
                   keyword=campaign_create.keyword,
                   personnel=campaign_create.personnel,
                   available_dayname=campaign_create.available_dayname,
                   unvailable_dayname=campaign_create.unvailable_dayname,
                   available_time=campaign_create.available_time,
                   run_start_date=campaign_create.run_start_date,
                   run_end_date=campaign_create.run_end_date,
                   apply_start_date=campaign_create.apply_start_date,
                   apply_end_date=campaign_create.apply_start_date,
                   create_date=campaign_create.create_date,
                   user_id=campaign_create.user_id,
                    ) """
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    # return { 
    #     'id': db_campaign.id,
    #     'userid': db_campaign.userid,
    #     'status': 'success'
    # }


def get_existing_user(db: Session, campaign_create: CampaignCreate):
    return db.query(Campaign).filter(
        (Campaign.userid == campaign_create.userid) |
        (Campaign.sns_id == campaign_create.sns_id) |
        (Campaign.email == campaign_create.email)
    ).first()

def get_user(db: Session, userid: str):
    return db.query(Campaign).filter(Campaign.userid == userid).first()