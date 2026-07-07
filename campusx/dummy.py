from fastapi import FastAPI,Path,HTTPException,Query
import json

app=FastAPI()

@app.get("/")
def hello():
    return{
        "message":"hello world"
    } 

def loadDaata():
    with open("test.json","r") as f:
        data=json.load(f)
    return data

@app.get('/view')
def view():
    data=loadDaata()
    return data

@app.get('/patationt/{pationt_id}')
def view_pataint(pationt_id:str = Path(..., description='ID of the pataint in the DB',example='p001')):
    data=loadDaata()
    if pationt_id in data:
        return data[pationt_id]
    raise HTTPException(status_code=404,detail="data not found")
    

@app.get('/sort')
def sort_pationt(sort_by:str=Query(...,description='sort on the basis of hoedgt,weight or bmi'),
                order:str=Query('asc',description='sort in ascending and descending order')):
    
    vaild_field=['height','weight','bni']
    if sort_by not in vaild_field:
        raise HTTPException(status_code=400,detail=f'Invailid field from {vaild_field}')
        
    if order not in ['asc','des']:
        raise HTTPException (status_code=400,detail=f'Invailid field from {vaild_field}')
    
    data=loadDaata()
    sort_order=True if order=='des' else False
    sorted_data= sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=sort_order
    )
    
    return sorted_data