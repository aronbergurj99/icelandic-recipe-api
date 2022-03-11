import uvicorn
from fastapi import FastAPI
import endpoints.recipes as recipes
import endpoints.users as users
from infrastructure.container import Container

import endpoints.recipes as recipes
def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[recipes, users])

    app = FastAPI()
    app.include_router(recipes.router)
    app.include_router(users.router)
    return app

app = create_app()

if __name__ == '__main__':
    uvicorn.run('server:app', host='localhost', port=8000, reload=True)