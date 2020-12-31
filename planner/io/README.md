# IO Specs

## Input Format

### Floor Schema ([jsonschema](https://python-jsonschema.readthedocs.io/en/stable/))

```json
{
  "type": "object",
  "required": ["dimensions", "viewQuality", "apartments"],
  "properties": {
    "dimensions": {
      "type": "object",
      "required": ["width", "length"],
      "properties": {
        "width": { "type": "number" },
        "length": { "type": "number" }
      }
    },
    "viewQuality": {
      "type": "object",
      "required": ["north", "west", "south", "east"],
      "properties": {
        "north": { "$ref": "#/definitions/view" },
        "west": { "$ref": "#/definitions/view" },
        "south": { "$ref": "#/definitions/view" },
        "east": { "$ref": "#/definitions/view" }
      }
    },
    "apartments": {
      "type": "array",
      "items": { "$ref": "#/definitions/apartment" },
      "minItems": 1
    },
    "elevator": { 
      "type": "object",
      "required": ["width", "length"],
      "properties": {
        "width": { "type": "number" },
        "length": { "type": "number" }
      }
    },
    "stairs": { 
      "type": "object",
      "required": ["width", "length"],
      "properties": {
        "width": { "type": "number" },
        "length": { "type": "number" }
      }
    },
    "numberOfCorridors": { "type": "number" },
    "optionalConstraints": { "$ref": "#/definitions/optionalConstraints" }
  },

  "definitions": {
    "view": {
      "type": "string",
      "enum": ["NO_VIEW", "OPEN_AREA", "LANDSCAPE"]
    },
    "apartment": {
      "type": "object",
      "required": ["count", "rooms", "numberOfHallways"],
      "properties": {
        "count": { "type": "number" },
        "rooms": {
          "type": "array",
          "items": { "$ref": "#/definitions/room" },
          "minItems": 1
        },
        "numberOfHallways": { "type": "number" },
        "roomSpacings": {
          "type": "array",
          "items": {
            "type": "array",
            "items": [
              { "type": "number" },
              { "type": "number" },
              {
                "type": "string",
                "enum": ["lt", "gt"]
              },
              { "type": "number" }
            ]
          },
          "minItems": 1
        }
      }
    },
    "room": {
      "type": "object",
      "required": ["roomType", "minArea"],
      "properties": {
        "roomType": {
          "type": "string",
          "enum": [
            "BEDROOM",
            "DRESSING_ROOM",
            "MASTER_BATHROOM",
            "BATHROOM",
            "KITCHEN",
            "DINING_ROOM",
            "LIVING_ROOM",
            "SUN_ROOM"
          ]
        },
        "minArea": { "type": "number" },
        "width": { "type": "number" },
        "length": { "type": "number" },
        "adjacentTo": { 
          "type": "array",
          "items": { "type": "number" }
        }
      }
    },
    "optionalConstraints": {
      "type": "object",
      "properties": {
        "allLandscape": { "type": "boolean" },
        "allNearElevator": { "type": "boolean" },
        "symmetry": { "type": "boolean" },
        "goldenRatio": { "type": "boolean" }
      }
    }
  }
}
```

The following, explains what each attribute represents:

- `dimensions`: The dimensions of the floor in meters
- `viewQuality`: The view quality of each of the floor sides (e.g. north view and south view). Each floor side can have one of three values, which are No View, Open Area and Landscape, where Landscape is the best possible view.
- `apartments`: An array of the apartment types that exist in the floor, for each apartment type the following is needed:
  - `count`: The number of apartments of this type.
  - `rooms`: An array of different rooms that exist in the apartment.
  - `numberOfHallways`: The max number of hallways in this apartment (e.g. L-shaped hallways are considered two hallways, while U-shaped hallways are considered three hallways).
  - `roomSpacings`: An array of soft constraints on different rooms inside the apartment. Each constraint is encoded as 4-tuple of the following format (First room index, Second room index, lt or gt, some distance d), which means that the distance between the first room type and the second room type should be less than (or greater than) that distance d.
- `room`: The room object is used inside the apartment to hold all the needed info of a room. The following attributes are stored for each room:
  - `roomType`: The type of the room (e.g. Bedroom or Kitchen ).
  - `minArea`: The minimum area of the room in square meters.
  - `width`: Preferred width of the room in meters.
  - `length`: Preferred length of the room in meters.
  - `adjacentTo`: A list of indices of rooms, which this room must be adjacent to.
- `elevator`: The dimensions of the elevator in meters, the default is 1x1.
- `stairs`: The dimensions of the stairs in meters, the default is 2x2.
- `numberOfCorridors`: The number of corridors in the floor, the default is the number of apartments + 1.
- `optionalConstraints`: Multiple optional hard constraints on the floor, each flag means the following:
  - `allLandscape`: All apartments should have look on landscape view.
  - `allNearElevator`: All apartments should be have an equal distance to the elevator unit.
  - `symmetry`: Symmetry Constraints over floor or over same type apartments.
  - `goldenRatio`: Allocate spaces with ratios following the divine proportion.

### Example Input

```json
{
  "floor": {
    "width": 8,
    "length": 10
  },
  "viewQuality": {
    "north": "OPEN_AREA",
    "west": "NO_VIEW",
    "south": "OPEN_AREA",
    "east": "LANDSCAPE"
  },
  "apartments": [
    {
      "rooms": [
        {
          "roomType": "BEDROOM",
          "minArea": 20
        },
        {
          "roomType": "BATHROOM",
          "minArea": 10
        }
      ]
    }
  ]
}
```
