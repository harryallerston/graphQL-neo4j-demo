import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import uvicorn

# Import our graphQL schema definition
from schema import schema

# Create a router for fastapi using the integration included in strawberry
graphql_app = GraphQLRouter(schema)

# Create our FastAPI app
app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

# Initialise API server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
