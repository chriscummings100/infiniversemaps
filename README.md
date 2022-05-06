# infiniversemaps
Examples for downloading and processing public infiniverse map data

This repo contains some samples and demos for accessing the Infiniverse map data for the Multiverse VR App (https://multiverseonline.io/)

# Setup
* get python installed (written with 3.8 though doesn't use any fancy features)
* download/clone the repo
* run "pip install -r requirements.txt" in the folder to install python requirements
* optionally run download.py to download latest Infiniverse data (this is done automatically run running sample scripts)

The current early Beta api simply downloads static files that are regularly updated, which contain the following:
* a root map.json file that contains a list of all districts (and urls to download them)
* district data and geometry
* subdistrict data and geometry (inc terrain types)
* building data and geometry (inc names, street id, storefronts etc)
* purchased apartment/storefronts
* street+junctions

Combined, the full data released is enough to create maps of the whole Infinvierse, generate street/building directories, or probably another 100 things we've not thought of.

# Current samples:
* settings.py: shared settings
* download.py: downloads latest map data - run this before using other scripts
* draw.py: generates a jpeg with a map of an area of infiniverse
* drawsvg.py generates an svg instead
* storefronts.py: dump out a csv and tabsv file with list of store fronts in Infiniverse

# Json Format

## map.json
This file is automatically loaded by settings:

### ROOT
* districts: [ MapDistrictRecord ]

### MapDistrictRecord
* cellx: x id of cell
* celly: y id of cell
* centrex: x position of district cell centre
* centrey: y position of district cell centre
* code: zip code of district (based on x and y id)
* url: download url of district info

## district file
Each district has an associated json file whose url is found in map.json

### ROOT
* district: District
* subdistricts: [ SubDistrict ]
* buildings: [ Building ]
* slots: [ Slot ]
* streets: [ Street ]
* junctions: [ Junction ]

### Common properties to district/subdistrict/building/slot
* cellx: x id of containing cell
* celly: y id of containing cell
* centre: Vector2, centre of node
* code: zip code

### District
* boundingpoly: Polygon, outer polygon covered by district

### Subdistrict
* subdistrictid: numeric id of subdistrict inside district
* innerfloor: FloorType, interior floor type
* outerfloor: FloorType, exterior floor type
* innerpoly: Polygon, interior floor polygon
* outerpoly: Polygon, exterior floor polygon
* curbpoly: Polygon, curb polygon

### Building
* subdistrictid: numeric id of containing subdistrict
* buildingid: numeric id of building inside subdistrict
* buildingstyle: BuildingType, type of building
* name: human readable building name
* doorcentre: Vector2, centre of door 
* doordir: Vector2, direction door faces
* storefront: Boolean, does building have storefront
* street: Street zip code
* street_number: Number of building on street
* boundingpoly: Polygon, Boundary of building structure

### Slot
* subdistrictid: numeric id of containing subdistrict
* buildingid: numeric id of containing building
* slot: slot index (0 = penthouse, 65538 = storefront)
* owner: Owner name
* location: Target location name
* domain: Target location metaverse name
* destination: Target location url

### Street
* code: zip code
* name: street name
* junctions: [ junction zip code ]

### Junction
* code: zip code
* pos: Vector2

### Polygon
* [ Vector2 ]

### Vector2
* [ x coord, y coord]

### FloorType (enum)
* [ Concrete | Grass | Water ]


Enjoy!

Chris