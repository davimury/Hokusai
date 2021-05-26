from fastapi import APIRouter, Request, HTTPException, Depends
from starlette.responses import Response, JSONResponse
from db.db_main import Session, TAGS
from sqlalchemy import or_
from models import Tags
from routers.login import manager

router = APIRouter()

@router.get("/v1/tags/")
async def get_all_tags():
    try:
        flag = True
        tags_arr = []
        session = Session()

        tags = session.query(TAGS).all()
        print(tags)
        
        for tag in tags:
            tags_arr.append({'id': tag.tag_id, 'name': tag.tag_name.title()})
        
    except:
        flag = False
    
    finally:
        session.close()
        
    if flag:
        if len(tags_arr) == 0:
            tags_arr.append({'id': None, 'name': 'Nenhuma tag encontrada, digite para criar novas tags!'}) 

        return JSONResponse(status_code=200, content=tags_arr)

@router.post("/v1/add_tag")
async def add_tag(tag: Tags):
    try:
        print(tag)
        flag = True
        session = Session()

        new_tag = TAGS(tag_name = tag.name.lower())  
        session.add(new_tag)

        session.commit()
        session.refresh(new_tag)
    except:
        flag = False
    
    finally:
        session.close()
        
    if flag: 
        return JSONResponse(content={'id': new_tag.tag_id, "name": new_tag.tag_name}, status_code=200)

@router.get("/v1/user/tags")
async def get_user_tags(user=Depends(manager)):
    try:
        flag = True
        tag_arr = []
        session = Session()

        tags = session.query(TAGS).filter(TAGS.tag_id.in_(user.tags)).all()

        for tag in tags:
            tag_arr.append(tag.tag_name)

        print(tag_arr)
    except:
        flag = False
    
    finally:
        session.close()

    if flag: 
        return JSONResponse(status_code=200, content=tag_arr)