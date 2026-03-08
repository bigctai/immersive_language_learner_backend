from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import create_all_tables
from routes import user, translate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers=["*"],
)

create_all_tables()

app.include_router(user.router)
app.include_router(translate.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)