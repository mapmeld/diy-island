# rarelang.py
# replace GeoJSON properties with random Unicode letters

import sys, json, random

source = sys.argv[1]

languages = {
  'test': ['0400','0499'],
  'mongolian': [0x1800, 0x18AF],
  'tifinagh': [0x2D30, 0x2d7F]
}
language = 'test'
range = languages[language]
field = 'sample'

nextLang = False
nextField = False
nextRange = False
for arg in sys.argv:
    if arg == "--field":
        nextField = True
    elif nextField:
        nextField = False
        field = arg
    elif arg == "--language":
        nextLang = True
    elif nextLang:
        nextLang = False
        arg = arg.lower()
        if languages.has_key(arg):
            language = arg
            range = languages[arg]
    elif arg == "--range":
        nextRange = True
    elif nextRange:
        range = arg.split('-')

gjfile = open(source,'r')
geojson = json.load(gjfile)
gjfile.close()

def relang(feature):
    newLabel = ""
    for letter in feature["properties"][field]:
        if letter == " ":
            newLabel = newLabel + " "
            continue
        newChar = unichr(random.randint(int(range[0],16),int(range[1],16)))
        newLabel = newLabel + newChar
    feature["properties"][field] = newLabel.encode('utf-8')

if geojson.has_key("features"):
    for feature in geojson["features"]:
        relang(feature)
else:
    relang(geojson)

outfile = open(source,'w')
outfile.write(json.dumps(geojson))
outfile.close()