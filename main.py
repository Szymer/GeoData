import uvicorn
from fastapi import FastAPI

from utils import get_data, add_data, update_item


app = FastAPI()

@app.get("/")
def read_root():
    return {"Welcome in GeoAPI"}


@app.get("/item/{item_id}")
def read_item(item_id: str):
    data = get_data(item_id)
    return data


@app.post("/item/add/{item_id}")
def add_item(item_id: str):
    add_data(item_id)
    return 


@app.put("/item/update/{item_id}")
def update_item(item_id: str):
    update_data(item_id)
    return 
  










if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
