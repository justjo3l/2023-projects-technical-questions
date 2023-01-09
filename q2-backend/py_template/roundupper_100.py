from dataclasses import dataclass
from enum import Enum
from typing import Union, NamedTuple, List
from flask import Flask, request
import math

# SpaceCowboy models a cowboy in our super amazing system
@dataclass
class SpaceCowboy:
    name: str
    lassoLength: int

# SpaceAnimal models a single animal in our amazing system
@dataclass
class SpaceAnimal:
    # SpaceAnimalType is an enum of all possible space animals we may encounter
    class SpaceAnimalType(Enum):
        PIG = "pig"
        COW = "cow"
        FLYING_BURGER = "flying_burger"

    type: SpaceAnimalType

# SpaceEntity models an entity in the super amazing (ROUND UPPER 100) system
@dataclass
class SpaceEntity:
    class Location(NamedTuple):
        x: int
        y: int

    metadata: Union[SpaceCowboy, SpaceAnimal]
    location: Location

# LassoedAnimal models a SpaceAnimal that has been lassoed
@dataclass
class LassoedAnimal:
    type: SpaceAnimal.SpaceAnimalType
    location: SpaceEntity.Location

# ==== HTTP Endpoint Stubs ====
app = Flask(__name__)
space_database: List[SpaceEntity] = []

# the POST /entity endpoint adds an entity to your global space database
@app.route('/entity', methods=['POST'])
def create_entity():
    # Gets JSON data from request
    json_data = request.json

    # Loops through entities
    for entity in json_data['entities']:
        # Checks if entity is a space cowboy or space animal or returns 400 if otherwise
        if entity['type'] == 'space_cowboy':
            # Creates new Space Cowboy entity with name and lassoLength
            new_entity = SpaceCowboy(entity['metadata']['name'], entity['metadata']['lassoLength'])
        elif entity['type'] == 'space_animal':
            # Creates new Space Animal entity with type
            new_entity = SpaceAnimal(entity['metadata']['type'])
        else:
            # Returns 400 status code
            return {'status': 'error'}, 400
        # Creates new entity location
        new_location = SpaceEntity.Location(entity['location']['x'], entity['location']['y'])

        # Adds Space Entity to Space Database
        space_database.append(SpaceEntity(new_entity, new_location))

    # Returns 200 status code
    return {}, 200

# lasooable returns all the space animals a space cowboy can lasso given their name
@app.route('/lassoable', methods=['GET'])
def lassoable():
    # Gets JSON data from request
    json_data = request.json

    # Defines empty cowboy
    cowboy = None

    # Loops through every entity in space_data
    cowboy = next(entity for entity in space_database if isinstance(entity.metadata, SpaceCowboy) and entity.metadata.name == json_data['cowboy_name'])

    # Returns 400 status code if cowboy is not found
    if (cowboy == None):
        return {'status':'error'}, 400
    
    # Creates list of lassoable animals
    lassoable_animals = []

    # Loops through every entity in space_data
    for entity in space_database:

        # Checks if entity is a space animal
        if isinstance(entity.metadata, SpaceAnimal):

            # Calculates pythagorean distance between cowboy and animal
            pythagorean = math.sqrt((entity.location.x - cowboy.location.x)**2 + (entity.location.y - cowboy.location.y)**2)

            # Adds animal to lassoable_animals if it is within the cowboy's lasso length
            if pythagorean <= cowboy.metadata.lassoLength:
                lassoable_animals.append(LassoedAnimal(entity.metadata.type, entity.location))

    # Returns 200 status code
    return { 'space_animals' : lassoable_animals }, 200


# DO NOT TOUCH ME, thanks :D
if __name__ == '__main__':
    app.run(debug=True, port=8080)