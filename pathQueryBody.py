from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()
users=[]

class User(BaseModel):
    name:str
    age:int
    
@app.post("/users")
def create_user(user:User):
    users.append(user)
    return{
        "message":"user created susscfull",
        "data":user
    }
    
@app.put("/users/{user_id}")
def updat_user(user_id:int,user:User,notify:bool=False):
    if(user_id<len(users)):
        users[user_id]=user
        return{
            "message":"User updated",
            "notify":notify,
            "data":user
        }
    return{
        "error":"user not fpund"
    }