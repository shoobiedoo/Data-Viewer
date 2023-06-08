# Data-Viewer
Uploads and fetches data on a react app (Assignment for invsto)
Have used postgres as DB and storing data in a table named stock inside the data_viewer_db.

Commands to download DB : 

psql -U shubhankitsingh -d data_viewer_db

query used for creating the database : "CREATE TABLE stock (
    datetime timestamp NOT NULL,
    close real NOT NULL,
    high real NOT NULL,
    low real NOT NULL,
    open real NOT NULL,
    volume integer NOT NULL,
    instrument text NOT NULL
);"




# Execution
python3 -m pip install virtualenv
virtualenv env --python=python3
. env/bin/activate
pip install -r requirements.txt
cd backend
uvicorn backend.main:app --reload

cd frontend
npm install 
npm start