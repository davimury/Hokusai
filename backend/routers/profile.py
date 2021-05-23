import base64
from fastapi import APIRouter, Depends
from db.db_main import Session, USERS
from routers.login import manager
from models import Profile

router = APIRouter()

@router.post("/v1/first_login")
async def fisrt_login(profile: Profile, user=Depends(manager)):

    """ Update profile image """
    """ imgdata = base64.b64decode(profile.image.replace("data:image/jpeg;base64,", ""))
    filename = str(user.user_id) + ".jpg"

    with open('../frontend/src/assets/img/profile/' + filename, "wb") as f:
        f.write(imgdata)
    """
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
    