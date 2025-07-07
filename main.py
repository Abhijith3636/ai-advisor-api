from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from ai_advisor import generate_advice
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI first
app = FastAPI()

# Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- Data Models -------------------
class User(BaseModel):
    name: str
    salary: float
    savings: float
    age: int
    expenses: float
    job_type: str = "salaried"
    dependents: int = 0

class Goal(BaseModel):
    name: str
    amount: float
    target_year: int
    saved_amount: float = 0

class Investment(BaseModel):
    instrument_name: str
    amount: float
    type: str = ""

class Insurance(BaseModel):
    type: str
    coverage: float
    amount:float

class AdvisorInput(BaseModel):
    user: User
    goals: List[Goal]
    investments: List[Investment]
    insurance: List[Insurance]

# ------------------- Route -------------------
@app.post("/advisor")
def get_advice(payload: AdvisorInput):
    try:
        result = generate_advice(
            user=payload.user.dict(),
            goals=[g.dict() for g in payload.goals],
            investments=[i.dict() for i in payload.investments],
            insurance=[ins.dict() for ins in payload.insurance]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
