from fastapi import FastAPI
from app.modules.sessions.router import router as sessions_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title = 'Voice-Cart',
    description="Real time voice agent withe e-commerce connectors"
)

app.include_router(sessions_router,prefix ='/api/v1')

@app.get('/hearh',tags= ['meta'])
async def health_check():
    'Simple liveness probe verification'
    return {'status' : 'ok', 'service': 'voice-cat -backend', 'env' : 'dev'}


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)