from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from db.db_main import Session, TAGS, USERS
from typing import List
from models import Tag
from routers.auth import manager

router = APIRouter()


@router.get("/tags/recommended")
async def get_all_tags(user=Depends(manager)):
    try:
        flag = True
        tags_arr = []
        session = Session()

        tags = session.query(TAGS).all()

        for tag in tags:
            if tag.tag_id not in user.tags:
                tags_arr.append({'tag_id': tag.tag_id, 'name': tag.tag_name.title()})

    except:
        flag = False

    finally:
        session.close()

    if flag:
        if len(tags_arr) == 0:
            tags_arr.append({'tag_id': None, 'name': 'Nenhuma tag encontrada!'})

        return JSONResponse(status_code=200, content=tags_arr)


@router.get("/tags/{username}")
async def get_tags_by_username(username: str, user=Depends(manager)):
    try:
        flag = True
        tag_arr = []
        session = Session()

        user_ = session.query(USERS).filter_by(username=username).first()
        tags = session.query(TAGS).filter(TAGS.tag_id.in_(user_.tags)).all()

        for tag in tags:
            tag_arr.append({'tag_id': tag.tag_id, 'name': tag.tag_name.title()})

    except:
        flag = False

    finally:
        session.close()

    if flag:
        return JSONResponse(status_code=200, content=tag_arr)


@router.post("/tag/new")
async def new_tag(tag: Tag, user=Depends(manager)):
    try:
        flag = True
        session = Session()
        session.expire_on_commit = False

        cur_user = session.query(USERS).filter_by(email=user.email).first()
        new_tag = TAGS(tag_name=tag.name.lower())
        new_tag.update_date()

        session.add(new_tag)
        session.commit()
        session.refresh(new_tag)

        cur_user.add_tag(session, new_tag.tag_id)
    except Exception as e:
        print(e)
        flag = False

    finally:
        session.close()

    if flag:
        return JSONResponse(content={'id': new_tag.tag_id, "name": new_tag.tag_name}, status_code=200)
    else:
        return JSONResponse(content={'status': e}, status_code=500)
        

@router.post("/tags/remove")
async def remove_tag(tags: List[Tag], user=Depends(manager)):
    try:
        flag = True
        session = Session()

        for tag in tags:
            user.tags.remove(tag.tag_id)

        session.merge(user)
        session.commit()

    except Exception as e:
        flag = False
    
    finally:
        session.close()
    
    if flag:
        return True
    else:
        return JSONResponse(content={'status': e}, status_code=500)


@router.post("/tags/add")
async def add_tag(tags: List[Tag], user=Depends(manager)):
    try:
        flag = True
        session = Session()

        for tag in tags:
            user.tags.append(tag.tag_id)

        session.merge(user)
        session.commit()

    except Exception as e:
        flag = False

    finally:
        session.close()
    
    if flag:
        return True
    else:
        return JSONResponse(content={'status': e}, status_code=500)

