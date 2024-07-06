from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
 

app = FastAPI()


@app.get('/')
async def root():
    return {"message": "Hello World"}


@app.post('/createpost')
def create_post(payload: dict = Body()):
    return {"title": f"Title: {payload['title']} Content: {payload['content']}"}
