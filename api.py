from fastapi import FastAPI

app = FastAPI() # run using uvicorn api:app --reload

@app.get("/")
async def root():
    return {"message": "Hello, world!"}

    
