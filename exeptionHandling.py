from fastapi import FastAPI,status,HTTPException,requests
from fastapi.responses import JSONResponse

app=FastAPI()

class userNotFoundExeption(Exception):
    def __init__(self,name:str):
        self.name=name
        
@app.exception_handler(userNotFoundExeption)
def user_not_found_handeler(request:requests,exc:userNotFoundExeption):
    return JSONResponse(
        status_code=404,
        content={
            "status":"error",
            "message":f"user {exc.name} not found" 
        }
    )
        
@app.get("/user/{user_name}")
def get_user(user_name:str):
    if user_name!="Ankit":
        raise userNotFoundExeption(user_name)
    return{
        "name":user_name
    }
    
        


# @app.get("/user/{user_id}")
# def get_user(user_id:int):
#     if user_id!=1:
#         raise HTTPException(
#             status_code=404,
#             detail="user not found"
#         )
#     return{
#         "id":1,
#         "name":"Ankit"
#     }
    
    