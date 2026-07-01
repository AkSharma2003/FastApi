from fastapi import FastAPI,Depends,Header,HTTPException

app=FastAPI()

def verify_token(token:str=Header(None)):
    if token!="mySecrateToken":
        raise HTTPException (
            status_code=401,
            detail="Unothorized"
        )
    return{
        "user":"Authorized user"
    }

@app.get("/secure-data")
def secure_data(user=Depends(verify_token)):
    return{
        "message":"secure data accessed",
        "user":user
    }

def common_logic():
    return {
        "message":"common logic executed"
    }
    
    
@app.get("/home")
def home(data=Depends(common_logic)):
    return data