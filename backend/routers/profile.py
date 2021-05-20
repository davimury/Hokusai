from fastapi import APIRouter, Request, HTTPException, Depends
from starlette.responses import Response
from db.db_main import Session, USERS
from datetime import datetime
from sqlalchemy import exc
from models import Posts
from routers.login import manager

router = APIRouter()


@router.post("/v1/update/profile")
async def update_profile(image: str, user=Depends(manager)):
    try:
        flag = True
        session = Session()

        imgdata = base64.b64decode(usuario_dict["user_photo"].replace("data:image/png;base64,", ""))

        filename = user.user_id + ".png"
        with open("static/img/users/" + filename, "wb") as f:
            f.write(imgdata)

        session.commit()
        
        for tag in tags:
            tags_arr.append({'id': tag.tag_id, 'name': tag.tag_name})
        
    except:
        flag = False
    
    finally:
        session.close()