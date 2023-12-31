from fastapi import FastAPI, HTTPException, Depends, status,APIRouter
from sqlalchemy.orm import Session 
from .. import database, models, schemas, oauth2
from typing import List, Optional 


router = APIRouter(prefix="/posts",tags=['POST'])


@router.get("/",response_model= List[schemas.Post])
def get_posts(db: Session = Depends(database.get_db), current_user:int=Depends(oauth2.get_current_user),
              search:Optional[str] = "", limit:int=10 , skip:int=0):
    posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).limit(limit).offset(skip).all()
    return posts

@router.get("/{id}", response_model = schemas.Post)
def get_id(id:int,db: Session = Depends(database.get_db), current_user:int=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    return post

@router.post("/",response_model=schemas.Post)
def create(post:schemas.PostCreate,db: Session = Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{id}",response_model=schemas.Post)
def update(post: schemas.PostCreate,id:int,db: Session = Depends(database.get_db), current_user:int=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_recovery = post_query.first()
    if post_recovery == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post_recovery.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    
    return post_query.first()

@router.delete("/{id}")
def delete(id:int,db: Session = Depends(database.get_db), current_user:int=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return{"data":f'delete succefull posts number {id}'}