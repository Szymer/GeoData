import uvicorn
from fastapi import FastAPI
from database import engine, Base
from routes import router

app = FastAPI()

        
def init_db():
    Base.metadata.create_all(bind=engine)

init_db()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
