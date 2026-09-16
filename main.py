from routers import news, users, favorite, history
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handlers import register_exception_handlers
from config import cache_config
import uvicorn

app = FastAPI(docs_static_url=None)
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)