from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from db.db_main import Session, TAGS, USERS
from sqlalchemy import or_
from models import Tags
from routers.auth import manager

router = APIRouter()


@router.get("/v1/tags/")
async def get_all_tags():
    try:
        flag = True
        tags_arr = []
        session = Session()

        tags = session.query(TAGS).all()

        for tag in tags:
            tags_arr.append({'id': tag.tag_id, 'name': tag.tag_name.title()})

    except:
        flag = False

    finally:
        session.close()

    if flag:
        if len(tags_arr) == 0:
            tags_arr.append({'id': None, 'name': 'Nenhuma tag encontrada!'})

        return JSONResponse(status_code=200, content=tags_arr)


@router.get("/v1/user/tags")
async def get_user_tags(user=Depends(manager)):
    try:
        flag = True
        tag_arr = []
        session = Session()

        tags = session.query(TAGS).filter(TAGS.tag_id.in_(user.tags)).all()

        for tag in tags:
            tag_arr.append(tag.tag_name)
    except:
        flag = False

    finally:
        session.close()

    if flag:
        return JSONResponse(status_code=200, content=tag_arr)


@router.post("/v1/add_tag")
async def add_tag(tag: Tags, user=Depends(manager)):
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
        