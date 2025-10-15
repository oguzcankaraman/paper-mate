from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Paper Mate API",
    description="Unified API for Paper Mate conversion services",
    version="0.1.0"
)

#TODO: KISITLAMA GETİRMEYİ UNUTMA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.include_router(script_routes.router, prefix="/api/ad gireriz", tags=["hallederiz"])
@app.get("/")
async def root():
    return {"message": "Welcome to T2V API!"}