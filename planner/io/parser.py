from planner.models.room_type import RoomType
from planner.models.view import View
from planner.models.room import Room
from planner.models.apartment import Apartment
from planner.models.floor import Floor
from jsonschema import validate
import json
import sys
import os

script_dir = os.path.dirname(__file__)
planner_path = os.path.join(script_dir, "../..")
sys.path.append(os.path.abspath(planner_path))


def parse_floor(path):
    # TODO Should include reference to global view constraints
    # TODO Should account for extra non-apartment spaces
    # TODO Should account for roomSpacings

    floor_json = load_json(path)
    validate_floor(floor_json)
    floor = json_to_floor(floor_json)
    return floor


def json_to_floor(floor_json):
    width = floor_json['dimensions']['width']
    length = floor_json['dimensions']['length']
    sides_views = tuple(map(parse_view,
                            tuple([floor_json['viewQuality'][key]
                                   for key in ['north', 'south', 'east', 'west']])
                            ))

    apartments_json = floor_json['apartments']
    apartments = [*map(parse_apartment, apartments_json)]
    return Floor(width, length, sides_views, apartments)


def parse_view(view_string):
    return View[view_string]


def parse_apartment(apartment_json):
    rooms_json = apartment_json['rooms']
    rooms = [*map(parse_room, rooms_json)]
    return Apartment(rooms)


def parse_room(room_json):
    room_type = parse_room_type(room_json['roomType'])
    min_area = room_json['minArea']

    preferred_width = None
    if 'width' in room_json:
        preferred_width = room_json['width']

    preferred_length = None
    if 'length' in room_json:
        preferred_length = room_json['length']

    adjacent_to = []
    if 'adjacentTo' in room_json:
        adjacent_to = room_json['adjacentTo']

    return Room(room_type, min_area, preferred_width, preferred_length, adjacent_to)


def parse_room_type(room_type_string):
    return RoomType[room_type_string]


def load_json(path, relative_to_source_file=False):
    """ Reads a JSON file from path

        Parameters
        ----------

            path : string
                Path of the JSON file (including the .json extension)
    """
    if relative_to_source_file:
        path = os.path.join(os.path.dirname(__file__), path)
    json_file = open(path)
    json_data = json.load(json_file)
    json_file.close()
    return json_data


def validate_floor(floor_json):
    """Check if a floor plan abides the schema"""
    schema = load_json('floor_schema.json', True)
    validate(instance=floor_json, schema=schema)
