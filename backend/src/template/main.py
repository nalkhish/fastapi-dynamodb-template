from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return "You are at the index"
