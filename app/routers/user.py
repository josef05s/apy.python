from fastapi import FastAPI, HTTPException, Depends, status,APIRouter
from sqlalchemy.orm import Session 
from .. import database, models, schemas, utils
from typing import List 


router = APIRouter(prefix="/users", tags= ['USERS'])

@router.get("/{id}", response_model = schemas.UserOut)
def get_id(id:int,db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    return user.first()

@router.post("/",response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create(user:schemas.UserCreate,db: Session = Depends(database.get_db)):

    #hash
    hashed_pasword = utils.hash(user.password)
    user.password =  hashed_pasword
    new_User = models.User(**user.dict())
    db.add(new_User)
    db.commit()
    db.refresh(new_User)
    return new_User



