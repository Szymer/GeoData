import uvicorn
from fastapi import FastAPI


app = FastAPI()
print('dupa')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000,  reload=True)
