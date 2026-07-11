from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Literal,Annotated
import pickle
import pandas as pd

# import AI modle
with open('model.pkl','rb') as f:
    model=pickle.load(f)
    
app=FastAPI()

# tear wise city name
tier_1_city = [
    "Ahmedabad",
    "Bengaluru",
    "Chennai",
    "Delhi",
    "Faridabad",
    "Ghaziabad",
    "Gurugram",
    "Hyderabad",
    "Kolkata",
    "Mumbai",
    "Navi Mumbai",
    "Noida",
    "Pune"
]
tier_2_city = [
    "Agra",
    "Ajmer",
    "Aligarh",
    "Allahabad",
    "Amritsar",
    "Aurangabad (Maharashtra)",
    "Bareilly",
    "Belagavi",
    "Bhilai",
    "Bhopal",
    "Bhubaneswar",
    "Chandigarh",
    "Coimbatore",
    "Cuttack",
    "Dehradun",
    "Dhanbad",
    "Durgapur",
    "Erode",
    "Goa (Panaji)",
    "Guntur",
    "Guwahati",
    "Gwalior",
    "Hubballi",
    "Indore",
    "Jabalpur",
    "Jaipur",
    "Jalandhar",
    "Jammu",
    "Jamshedpur",
    "Jodhpur",
    "Kanpur",
    "Kochi",
    "Kolhapur",
    "Kota",
    "Kozhikode",
    "Lucknow",
    "Ludhiana",
    "Madurai",
    "Mangaluru",
    "Mysuru",
    "Nagpur",
    "Nashik",
    "Patna",
    "Puducherry",
    "Raipur",
    "Rajkot",
    "Ranchi",
    "Salem",
    "Srinagar",
    "Surat",
    "Thiruvananthapuram",
    "Thrissur",
    "Tiruchirappalli",
    "Tiruppur",
    "Udaipur",
    "Vadodara",
    "Varanasi",
    "Vijayawada",
    "Visakhapatnam",
    "Warangal"
]
tier_3_city = [
    "Anantapur",
    "Anand",
    "Arrah",
    "Asansol",
    "Aurangabad (Bihar)",
    "Begusarai",
    "Bhagalpur",
    "Bikaner",
    "Bilaspur",
    "Bokaro",
    "Darbhanga",
    "Davanagere",
    "Dibrugarh",
    "Gaya",
    "Gorakhpur",
    "Haldwani",
    "Hisar",
    "Jhansi",
    "Kakinada",
    "Karimnagar",
    "Karnal",
    "Khammam",
    "Kurnool",
    "Mathura",
    "Meerut",
    "Moradabad",
    "Muzaffarpur",
    "Nanded",
    "Nellore",
    "Patiala",
    "Prayagraj",
    "Rohtak",
    "Rourkela",
    "Sagar",
    "Saharanpur",
    "Sambalpur",
    "Shimla",
    "Sikar",
    "Siliguri",
    "Solapur",
    "Sonipat",
    "Thoothukudi",
    "Ujjain",
    "Vellore"
]

# pydantic modle to vailidate incoming data
class userInput(BaseModel):
    age:Annotated[int,Field(...,gt=0,lt=120,description='Age of the user')]
    weight:Annotated[float,Field(...,gt=0,description='Weight of the user')]
    height:Annotated[float,Field(...,gt=0,lt=2.5,description='Height of the user')]
    income_lpa:Annotated[int,Field(...,gt=0,lt=120,description='yearly income of the user')]
    smoker:Annotated[bool,Field(...,description='It is smoker or not')]
    city:Annotated[str,Field(...,description='the city taht user belongs to')]
    ocupation:Annotated[Literal['retaireed','freelancer','student','goverment_job','business_owner','unemployeed','private_job'],
                        Field(...,description='occupation of the user')]
    
    
    @computed_field
    @property
    def bmi(self)->float:
        return self.weight/(self.height**2)
    
    
    @computed_field
    @property
    def lifestyle_risk(self)->str:
        if self.smoker and self.bmi>30 : return "high"
        elif self.smoker and self.bmi>27: return "medium"
        else : return "low"
        
    @computed_field
    @property
    def age_group(self)->str:
        if self.age<25: return "young"
        elif self.age<45 : return "adult"
        elif self.age<60: return "middle_age"
        else : return "senior"
        
    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_city: return 1
        elif self.city in tier_2_city: return 2
        else : return 3
    
@app.post('/predict')
def predict_premium(data:userInput):
    
    
    input_df=pd.DataFrame([
        {
            'bmi':data.bmi,
            'age_group':data.age_group,
            'lifestyle_risk':data.lifestyle_risk,
            'city_tier':data.city_tier,
            'income_lpa':data.income_lpa,
            'occupation':data.ocupation
        }
    ])
    
    prediction=model.predict(input_df)[0]
    return JSONResponse(status_code=200,content={'predect_cotegry':prediction})
    