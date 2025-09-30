import logging
from fastapi import FastAPI
from app.routes import states, cases



logging.basicConfig(
    level=logging.DEBUG,  
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


app = FastAPI(title="Court Case Tracker API")

# Routes
app.include_router(states.router, prefix="/states", tags=["states"])
app.include_router(cases.router, prefix="/cases", tags=["cases"])

@app.get("/")
def root():
    return {"message": "API is running!"}
