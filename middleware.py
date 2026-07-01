from fastapi import FastAPI,Request
import time
app=FastAPI()

# @app.middleware("http")
# async def my_middleware(request:requests,call_next):
#     print("request recivied")
    
#     response= await call_next(request)
#     print("response sent")
    
#     return response 
    
    
@app.middleware("http")
async def log_middleware(request:Request,call_next):
    start_time=time.time()
    response=await call_next(request)
    
    process_time=time.time()-start_time
    
    print(f"path: {request.url.path} | time:{process_time}")
    
    return response
