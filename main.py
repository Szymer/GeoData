import uvicorn
from fastapi import FastAPI
from database import engine, Base
from routes import router

app = FastAPI()

        
def init_db():
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception as e:
        raise SystemExit(e)

        

  

init_db()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
