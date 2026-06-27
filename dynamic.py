from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()
@app.get("/")
def home():
    return {"This is home page"}

@app.get("/users/{user_id}")
def user(user_id):
    return{
        "user id is ":user_id
    }
    
# optional parameater
@app.get("/product")
def product(name:str=None):
    return{"name":name}

# default value
@app.get("/item")
def item(limit: int=10):
    return{"limit":limit}

# multiple parameater
@app.get("/cart")
def cart(name: str=None, price:int=100):
    return{
        "name":name,
        "price":price
    }
    
    
# POST API
@app.post("/creat_user")
def creat_uiser(name:str,agg:int):
    return{
        "name":name,
        "age":agg
    }
    
# pydantic : first importe padnatics from basse modle
class User(BaseModel):
    name:str
    age:int


@app.post("/creat_user2")
def creat_uiser2(user:User):
    return{
        "data":user
    }
    
    
# nested modele
class Address(BaseModel):
    city:str
    pincode:int
    
class comoplete(BaseModel):
    name:str
    agg:int
    address:Address
    
    
@app.post("/details")
def details(det:comoplete):
    return{
        "data":det
    }