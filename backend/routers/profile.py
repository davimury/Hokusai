import base64
import random
from fastapi import APIRouter, Depends
from sqlalchemy import and_
from db.db_main import Session, USERS, POSTS, TAGS, LIKES
from routers.login import manager
from models import Profile, Base64

router = APIRouter()

@router.post("/v1/first_login")
async def fisrt_login(profile: Profile, user=Depends(manager)):

    """ Update profile image """
    imgdata = base64.b64decode(profile.image.replace("data:image/jpeg;base64,", ""))
    filename = str(user.user_id) + ".jpg"

    with open('../frontend/src/assets/img/profile/' + filename, "wb") as f:
        f.write(imgdata)
   
    """ Update user favorite tags """

    try:
        session = Session()

        user.tags = profile.tags
        
        session.merge(user)
        session.commit()
    except Exception as e:
        print(e)
        #raise HTTPException(status_code=409, detail="email ou username já cadastrados!")
    
    finally:
        session.close()
        
    """ if flag: 
        return Response(status_code=200) """

@router.post("/v1/change/profile")
async def change_profile(base: Base64, user=Depends(manager)):
    filename = str(user.user_id) + ".jpg"

    with open('../frontend/src/assets/img/profile/' + filename, "wb") as f:
        f.write(base64.b64decode(base.base[base.base.find(",")+1:]))

@router.post("/v1/change/header")
async def change_header(base: Base64, user=Depends(manager)):
    """ Update profile image """
    filename = str(user.user_id) + ".jpg"

    with open('../frontend/src/assets/img/header/' + filename, "wb") as f:
        f.write(base64.b64decode(base.base[base.base.find(",")+1:]))

@router.get("/v1/user/{username}/info")
async def get_user_info(username: str, user=Depends(manager)):
    try:
        session = Session()
        posts_arr = []
        tags_arr = []

        this_user = session.query(USERS).filter_by(username = username).first()
        posts = session.query(POSTS).filter_by(post_author=this_user.user_id).order_by(POSTS.post_id.desc()).all()
        tags = session.query(TAGS).filter(TAGS.tag_id.in_(this_user.tags)).all()

        for tag in tags:
            tags_arr.append(tag.tag_name)

        for post in posts:
            like_obj = session.query(LIKES).filter_by(post_id = post.post_id, user_id=user.user_id).first()
            like = False
            dislike = False

            if like_obj and like_obj.like_type == True:
                like = True
            elif like_obj and like_obj.like_type == False:
                dislike = True
            
            posts_arr.append({
                'post_id': post.post_id,
                'description': post.post_body,
                'slides': post.post_img,
                'username': post.author.username,
                'name': post.author.name,
                'author_id': post.author.user_id,
                'postType': post.post_type,
                'likes': post.likes,
                'likes': post.likes,
                'like': like,
                'dislike': dislike,
            })
    except Exception as e:
        print(e)
        #raise HTTPException(status_code=409, detail="email ou username já cadastrados!")
    
    finally:
        session.close()

    return {
        'user_id': user.user_id,
        'name': user.name,
        'tags': tags_arr,
        'posts_count': len(posts_arr),
        'posts': posts_arr,
    }
    
@router.get("/v1/user/suggestedUsers")
async def get_suggested_users(user=Depends(manager)):
    try:
        session = Session()
        sugested_array = session.query(USERS).filter(and_(USERS.tags.contains(user.tags), USERS.user_id != user.user_id)).all()
        users_arr = []

        for user_ in sugested_array:
            users_arr.append({
                'user_id': user_.user_id,
                'username': user_.username,
                'name': user_.name,
            })
            
    except Exception as e:
        print(e)
        #raise HTTPException(status_code=409, detail="email ou username já cadastrados!")
    
    finally:
        session.close()

    return users_arr
    