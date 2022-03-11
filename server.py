import uvicorn
from fastapi import FastAPI
import endpoints.recipes as recipes

import endpoints.recipes as recipes
def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(recipes.router)
    return app

app = create_app()

if __name__ == '__main__':
    uvicorn.run('server:app', host='localhost', port=8000, reload=True)