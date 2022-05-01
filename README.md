# infiniversemaps
Examples for downloading and processing public infiniverse map data

This repo contains some samples and demos for accessing the Infiniverse map data for the Multiverse VR App (https://multiverseonline.io/)

The current early Beta api simply downloads static files that are regularly updated, which contain the following:
* a root map.json file that contains a list of all districts (and urls to download them)
* district data and geometry
* subdistrict data and geometry (inc terrain types)
* building data and geometry (inc names, street id, storefronts etc)
* purchased apartment/storefronts
* street+junctions

Combined, the full data released is enough to create maps of the whole Infinvierse, generate street/building directories, or probably another 100 things we've not thought of.

Current samples:
* download.py: downloads latest map data - run this before using other scripts
* draw.py: generates a jpeg with a map of an area of infiniverse

Enjoy!

Chris