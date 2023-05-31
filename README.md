# graphQL API with Strawberry and Neo4j
---

This repository contains a toy example of a graphQL API interface to the 'Movies' demo database provided by default in Neo4j.

The API is built using the Strawberry graphQL framework (https://strawberry.rocks/) and it's built in FastAPI integration. 

The goal of the project was to create an API frontend to the demo dataset, giving easy access to all node data within it, as well as entity relations. 

A nice overview of the library and reasons to use graphQL can be found here: (https://www.youtube.com/watch?v=J9AYhCmKMzo)

## Usage
---

This repo contains the API service, and the example neo4j test data. To start both services, simply run

```
docker-compose up
```

The neo4j web interface can be found on

```
 http://127.0.0.1:7474
```

Credentials are 'neo4j/terriblyinsecure'.

To access the graphQL API, navigate to 

```
http://127.0.0.1:8000/graphql
```

