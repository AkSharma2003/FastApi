from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
import json
from fastapi.responses import JSONResponse

app=FastAPI()

def load_data():
    with open('test.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('test.json','w') as f:
        json.dump(data,f)

class patient(BaseModel):
    id:Annotated[str,Field(...,description='ID of the patient',examples=['P001'])]
    name:Annotated[str,Field(...,description='name of the patient')]
    city:Annotated[str,Field(...,description='name of city living patient')]
    gender:Annotated[Literal['male','female','other'],Field(description='gender of patient')]
    height:Annotated[float,Field(...,gt=0,lt=100,description='height of patient')]
    weight:Annotated[float,Field(...,gt=0,lt=100,description='height of patient')]
        
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    
    def verdict(self)->str:
        if self.bmi<18.5:
            return "underweight"
        elif self.bmi<30:
            return "normal"
        else :
            return "obese"

@app.post("/create")
def create_patient(patient:patient):
    # load existing data
    data=load_data()
        
    # cheak if the patient allready exit or not
    if patient.id in data:
        raise HTTPException(status_code=400,detail='patient allready exit')
        
    # new patient added in the database
    data[patient.id]=patient.model_dump(exclude=['id'])
        
    save_data(data)
        
    return JSONResponse(status_code=200,content={"message":"data added successfully"})
    

