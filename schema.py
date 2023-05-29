import strawberry
import socket
from typing import Optional, List
from neo4j import GraphDatabase

neo4j_host = socket.gethostbyname('graphql-test-neo4j')
driver = GraphDatabase.driver(f"bolt://{neo4j_host}:7687", auth=("neo4j", "terriblyinsecure"))

# ---------------------------------------------------------------------------------------------------------------
#   Data Classes
# ---------------------------------------------------------------------------------------------------------------
# Define our dataclasses for Person and Movie nodes. All existing node properties are present as graphQL fields.
# Additional fields are lazily constructed when called, based on relationships present in the graph. 
# Relationships have only been utilised for Person nodes in this example to simplify things. 

@strawberry.type
class Movie:
    title: str
    released: Optional[int]
    tagline: Optional[str]

# ---------------------------------------------------------------------------------------------------

@strawberry.type
class Person:
    name: str
    born: Optional[int]    

    # Lazily evaluated fields and their resolvers
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    acted_in: List[Movie] = strawberry.field()
    @strawberry.field
    async def acted_in(self) -> List[Movie]:
        with driver.session() as session:
            query = """
            MATCH (m:Movie)<-[:ACTED_IN]-(p:Person)
            WHERE toLower(p.name) = toLower($name)
            RETURN m.released AS released, m.title AS title, m.tagline AS tagline
            """
            result = session.run(query, name=self.name)
            movies = [
                Movie(
                    title=record["title"],
                    released=record["released"],
                    tagline=record["tagline"]
                )
                for record in result
            ]
            return movies
        
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
    directed: List[Movie] = strawberry.field()
    @strawberry.field
    async def directed(self) -> List[Movie]:
        with driver.session() as session:
            query = """
            MATCH (m:Movie)<-[:DIRECTED]-(p:Person)
            WHERE toLower(p.name) = toLower($name)
            RETURN m.released AS released, m.title AS title, m.tagline AS tagline
            """
            result = session.run(query, name=self.name)
            movies = [
                Movie(
                    title=record["title"],
                    released=record["released"],
                    tagline=record["tagline"]
                )
                for record in result
            ]
            return movies
        
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    
    produced: List[Movie] = strawberry.field()
    @strawberry.field
    async def produced(self) -> List[Movie]:
        with driver.session() as session:
            query = """
            MATCH (m:Movie)<-[:PRODUCED]-(p:Person)
            WHERE toLower(p.name) = toLower($name)
            RETURN m.released AS released, m.title AS title, m.tagline AS tagline
            """
            result = session.run(query, name=self.name)
            movies = [
                Movie(
                    title=record["title"],
                    released=record["released"],
                    tagline=record["tagline"]
                )
                for record in result
            ]
            return movies
        
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    wrote: List[Movie] = strawberry.field()
    @strawberry.field
    async def wrote(self) -> List[Movie]:
        with driver.session() as session:
            query = """
            MATCH (m:Movie)<-[:WROTE]-(p:Person)
            WHERE toLower(p.name) = toLower($name)
            RETURN m.released AS released, m.title AS title, m.tagline AS tagline
            """
            result = session.run(query, name=self.name)
            movies = [
                Movie(
                    title=record["title"],
                    released=record["released"],
                    tagline=record["tagline"]
                )
                for record in result
            ]
            return movies
        
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    reviewed: List[Movie] = strawberry.field()
    @strawberry.field
    async def reviewed(self) -> List[Movie]:
        with driver.session() as session:
            query = """
            MATCH (m:Movie)<-[:REVIEWED]-(p:Person)
            WHERE toLower(p.name) = toLower($name)
            RETURN m.released AS released, m.title AS title, m.tagline AS tagline
            """
            result = session.run(query, name=self.name)
            movies = [
                Movie(
                    title=record["title"],
                    released=record["released"],
                    tagline=record["tagline"]
                )
                for record in result
            ]
            return movies
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
    follows: List['Person'] = strawberry.field()
    @strawberry.field
    async def follows(self) -> List['Person']:
        with driver.session() as session:
            query = """
            MATCH (p2:Person)<-[:FOLLOWS]-(p:Person)
            WHERE toLower(p.name) = toLower($name)
            RETURN p2.born AS born, p2.name AS name
            """
            result = session.run(query, name=self.name)
            people = [
                Person(
                    born=record["born"],
                    name=record["name"]
                )
                for record in result
            ]
            return people
        
# ---------------------------------------------------------------------------------------------------
#   QUERIES
# ---------------------------------------------------------------------------------------------------
# Queries available to user to return Person and Movie information

@strawberry.type
class Query:
    @strawberry.field
    def people(self, names: Optional[List[str]]) -> List[Person]:
        with driver.session() as session:
            # If a list of names was provided by the user, filter on them. If not, return all Person nodes. 
            if not names:
                query = """
                MATCH (p:Person)
                RETURN p.born AS born, p.name AS name
                """
                result = session.run(query)
            else:
                names = [x.lower() for x in names]
                query = """
                MATCH (p:Person)
                WHERE toLower(p.name) IN $names
                RETURN p.born AS born, p.name AS name
                """
                result = session.run(query, names=names)
            
            people = [
                Person(
                    born=record["born"],
                    name=record["name"]
                )
                for record in result
            ]
            return people

    @strawberry.field
    def movies(self, titles: Optional[List[str]]) -> List[Movie]:
        with driver.session() as session:
            # If a list of titles was provided by the user, filter on them. If not, return all Movie nodes. 
            if not titles:
                query = """
                MATCH (m:Movie)
                RETURN m.released AS released, m.title AS title, m.tagline AS tagline
                """
                result = session.run(query)
            else:
                titles = [x.lower() for x in titles]
                query = """
                MATCH (m:Movie)
                WHERE toLower(m.title) IN $titles
                RETURN m.released AS released, m.title AS title, m.tagline AS tagline
                """
                result = session.run(query, titles=titles)

                movies = [
                    Movie(
                        title=record["title"],
                        released=record["released"],
                        tagline=record["tagline"]
                    )
                    for record in result
                ]
                return movies


schema = strawberry.Schema(query=Query)
