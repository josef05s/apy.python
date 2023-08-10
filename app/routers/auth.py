from fastapi import FastAPI, HTTPException, Depends, status,APIRouter
from sqlalchemy.orm import Session 
from .. import database, models, schemas, utils, oauth2



router = APIRouter(tags= ['Authentication' ])

@router.post("/login")
def login(user_credential: schemas.UserLogin, db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credential.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inavalid Credential")
    
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inavalid Credential")
    
    #create token

    access_token = oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}
    
    




