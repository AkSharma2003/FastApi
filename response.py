from fastapi import FastAPI
from pydantic import BaseModel

app =FastAPI()

class User(BaseModel):
    name:str
    age:int
    password:str
    
class user_response(BaseModel):
    name:str
    age:int

@app.post("/user",response_model=user_response)
def get_user():
    return{
        "name":"Ankit Kumar Sharma",
        "age":23,
        "password":12345   
    }