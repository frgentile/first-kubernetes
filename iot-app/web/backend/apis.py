import os
from fastapi import FastAPI
from pymongo import MongoClient
from bson.json_util import dumps
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB configuration
client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://mongodb:27017/'))
db = client[os.getenv('MONGODB_DATABASE', 'iot_database')]

@app.get("/api/v1/devices")
async def get_devices():
    collections = db.list_collection_names()
    devices = []

    for collection_name in collections:
        collection = db[collection_name]
        last_document = collection.find().sort('_id', -1).limit(1)
        devices.append({
            'device': collection_name,
            'last_document': dumps(last_document)
        })

    return JSONResponse(content=devices)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)