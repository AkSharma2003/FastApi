from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
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
    


class patientUPdate(BaseModel):
    id:Annotated[Optional[str],Field(default=None)]
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    gender:Annotated[Optional[Literal['male','female','other']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None)]
    weight:Annotated[Optional[float],Field(default=None)]
    
    
@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:patientUPdate):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='patient id is not abalvele in the data set')        
    existing_patient_info=data[patient_id]
    updated_patient_info=patient_update.model_dump(exclude_unset=True)
        
    for key,value in updated_patient_info.items():
        existing_patient_info[key]=value
        
    existing_patient_info['id']=patient_id # add id in the exiting data
    pateint_pydentic_object=patient(**existing_patient_info) # convert pydantic object
    existing_patient_info=pateint_pydentic_object.model_dump(exclude='id') # remove id from exiting data  & convert in to the dectionery
        
    data[patient_id]=existing_patient_info # update new data
        
    save_data(data) # save data
        
    return JSONResponse(status_code=200,content={'message':'data updated successfully'})    
    
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):
    data=load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='patient id is not abaiilble in the given data')
    
    del data[patient_id]
    save_data(data)
    
    return JSONResponse(status_code=200,content={'message':'data deleted successfully'})
             