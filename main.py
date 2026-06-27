from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
    return {"massege":"Welcom to my home"}

@app.get("/users")
def users():
    return {
        "user":["mohit","rohit"]
    }
        