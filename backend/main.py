# Import necessary libraries and modules
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.sql import insert
import pandas as pd
from io import StringIO
from typing import List
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

print(DB_NAME)
# Define SQLAlchemy database URL and create engine
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#DATABASE_URL = "postgresql://${username:@localhost:5432/dbname"
engine = create_engine(DATABASE_URL)

# Load metadata
metadata = MetaData()

# Define FastAPI app and allow all CORS
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define SQLAlchemy table
stock = Table("stock", metadata, autoload_with=engine)

# Define Pydantic model for StockItem
class StockItem(BaseModel):
    datetime: datetime
    close: float
    high: float
    low: float
    open: float
    volume: int
    instrument: str

    # Method to convert database tuple to StockItem instance
    @classmethod
    def from_tuple(cls, data):
        return cls(
        datetime=data[0],
        close=data[1],
        high=data[2],
        low=data[3],
        open=data[4],
        volume=data[5],
        instrument=data[6])

# Endpoint to upload data
@app.post("/upload-data/")
async def upload_data(file: UploadFile = File(...)):
    # Read the uploaded file
    contents = await file.read()

    # Convert the file contents to a DataFrame
    df = pd.read_csv(StringIO(contents.decode("utf-8")))

    # Convert the DataFrame to a list of dictionary items
    data_list = df.to_dict(orient="records")

    # Create an insert query
    query = insert(stock).values(data_list)

    # Execute the query
    with engine.connect() as connection:
        result = connection.execute(query)
        connection.commit()

        # Check result and return appropriate response
        if result:
            return {"message": "Data inserted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Insert failed")

# Endpoint to get data
@app.get("/get-data/", response_model=List[StockItem])
async def get_data():
    # Create a select query
    query = select('*').select_from(stock)

    # Execute the query
    with engine.connect() as connection:
        result = connection.execute(query)

        # Convert result to list of StockItem instances
        return [StockItem.from_tuple(i) for i in result]
