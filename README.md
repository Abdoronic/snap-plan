# snap-plan

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
    "numberOfElevators": { "type": "number" },
    "numberOfStairs": { "type": "number" },
    "numberOfDucts": { "type": "number" }
  },

  "definitions": {
    "view": {
      "type": "string",
      "enum": ["NO_VIEW", "OPEN_AREA", "LANDSCAPE"]
    },
    "apartment": {
      "type": "object",
      "required": ["rooms"],
      "properties": {
        "rooms": {
          "type": "array",
          "items": { "$ref": "#/definitions/room" },
          "minItems": 1
        },
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
    }
  }
}
```

The following, explains what each attribute represents:

- `dimensions`: The dimensions of the floor in meters
- `viewQuality`: The view quality of each of the floor sides (e.g. north view and south view). Each floor side can have one of three values, which are No View, Open Area and Landscape, where Landscape is the best possible view.
- `apartments`: An array of the apartments that exist in the floor, for each apartment the following is needed:
  - `rooms`: An array of different rooms that exist in the apartment.
  - `roomSpacings`: An array of soft constraints on different rooms inside the apartment. Each constraint is encoded as 4-tuple of the following format (First room index, Second room index, lt or gt, some distance d), which means that the distance between the first room type and the second room type should be less than (or greater than) that distance d.
- `room`: The room object is used inside the apartment to hold all the needed info of a room. The following attributes are stored for each room:
  - `roomType`: The type of the room (e.g. Bedroom or Kitchen ).
  - `minArea`: The minimum area of the room in square meters.
  - `width`: Preferred width of the room in meters.
  - `length`: Preferred length of the room in meters.
  - `adjacentTo`: A list of indices of rooms, which this room must be adjacent to.
- `numberOfElevators`: The number of elevators in the floor, the default is one.
- `numberOfStairs`: The number of stairs in the floor, the default is one.
- `numberOfDucts`: The number of ducts in the floor, the default is one.

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

High Level Modules
Apartments / Stairs / Elevator / Ducts
