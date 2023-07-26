from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def read_msg():
    return {"message":"hola mundo, soy ...."
            }
@app.get("/items/{item_id}")
def read_item(item_id:int,msg):
    return {"item_id":item_id,"msg":msg}



