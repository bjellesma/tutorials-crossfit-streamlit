from fastapi import FastAPI, HTTPException
import traceback
import database

app = FastAPI()


@app.get('/api/athletes')
def get_athletes():
    try:
        return database.get_athletes()
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(500, detail=str(ex))
