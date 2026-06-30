from fastapi import FastAPI,status,HTTPException

app=FastAPI()

@app.post("/create_user",status_code=status.HTTP_201_CREATED)
def create_user():
    return{
        "message":"user created successfuly"
    }
    
@app.get("/user")
def get_users():
    return{
        "status":"successfull",
        "message":"user data gfet successfully",
        "data":{
            "name":"Ankit Kumar Sharma",
            "age":23,
            "password":1234
        }
    }
    
@app.get("/user/{user_id}")
def get_user(user_id:int):
    if user_id!=1:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    return{
        "id":1,
        "name":"misspai" 
    }
    
    