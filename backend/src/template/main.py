from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from template.middleware.auth import AuthMiddleware

app = FastAPI()

# Middleware order matters. If you add a middleware first, it will be executed last.
app.add_middleware(AuthMiddleware)
# allow CORS for all origins on all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return "You are at the index"
