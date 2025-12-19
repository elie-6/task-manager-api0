import uvicorn
from fastapi import FastAPI,HTTPException
from app.config.settings import settings
from app.controllers import include_routers
from app.data.database import task_collection

app = FastAPI(title="Task Manager API")

@app.get("/")
def home():
    
    context = {
        "MONGODB_URL": settings.MONGODB_URL,
        "MONGODB_DATABASE": settings.MONGODB_DATABASE
    }
    return context

@app.get("/test-db")
async def test_db():
  
    try:
        doc = await task_collection.find_one()
        return {"detail": "Connected to Atlas!", "example_doc": doc}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


include_routers(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
