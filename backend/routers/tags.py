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

        tags = session.query(TAGS).filter(TAGS.tag_id.between(1,10)).all()
        session.commit()
        
        for tag in tags:
            tags_arr.append({'id': tag.tag_id, 'name': tag.tag_name})
        
    except:
        flag = False
    
    finally:
        session.close()
        
    if flag: 
        return JSONResponse(status_code=200, content=tags_arr)

@router.post("/v1/add_tag/")
async def add_tag(tag: Tags):
    try:
        flag = True
        session = Session()

        new_tag = TAGS(tag_name = tag.tag_name.upper())  
        session.add(new_tag)

        session.commit()
        
    except:
        flag = False
    
    finally:
        session.close()
        
    if flag: 
        return Response(status_code=200)