from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel) :
    tittle: str
    content: str
    published : bool=True
    rating: Optional[ int] =None
   
my_posts  = [ 
    {"tittle":"my post 1","content": "content 1", "id":1} ,
    {"tittle":"my post 2","content": "content 2", "id":2} ,
    {"tittle":"my post 3","content": "content 3", "id":3} ,
            
            ]
@app.get("/")

def read_msg():
    return {"message":"Bienvenidos a miAPI REST, una aplicacion de post."
            }
@app.get("/items/{item_id}")
def read_item(item_id:int,msg):
    return {"item_id":item_id,"msg":msg}

#recuperando todos los datos

@app.get("/posts")
def get_posts():
    return {"data":my_posts}


def find_post(id):

    for i in my_posts:
        if i["id"] == id:
            return i
        
        
def find_post_2(id):

    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/posts/{id}")
def get_posts_id (id:int):

    post = find_post(id)
    return {"data":post}

#CREATE POST

@app.post("/posts")
def create_post(post:Post):
    diccionario=post.dict()
    diccionario[ "id"] = randrange(0,1000000)
    my_posts.append(diccionario)
    return {"data":diccionario}

#UPDATE POST

@app.put("/posts/{id}")

def update_post(id:int, post:Post):
    index = find_post_2(id)
    if index is None: 
        raise HTTPException(status_code=404, detail="Post not found")
    update_post = post.dict()
    
    my_posts [ index] = update_post
    my_posts [ index] ["id" ] = id
    

    
    
    
   

    return{"data":update_post}


#Delete

@app.delete("/posts/{id}")
def delete_post(id:int):

    post_id = find_post_2(id)

    my_posts.pop(post_id)

    return{"data":f"Se elimino exitosamente {post_id+1}"}