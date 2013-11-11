# mapflip.py
# disguise GeoJSON shape by flipping or rotating clockwise

import sys, json

source = sys.argv[1]
flipHorizontal = False
flipVertical = False

nextRotate = False
rotateAmount = 0

for arg in sys.argv:
    if arg == "--flip-horizontal":
        flipHorizontal = True
    elif arg == "--flip-vertical":
        flipVertical = True
    elif arg == "--rotate":
        nextRotate = True
    elif nextRotate:
        nextRotate = False
        rotateAmount = int( arg )
if (rotateAmount != 90) and (rotateAmount != 180) and (rotateAmount != 270):
    rotateAmount = 0

gjfile = open(source,'r')
geojson = json.load(gjfile)
gjfile.close()

def changeCoordinate(arr):
    if(type(arr) == type([])):
        # recursive into array
        if(len(arr) > 0 and (type(arr[0]) == type(2) or type(arr[0]) == type(2.0))):
            # actual coordinate
            if(flipHorizontal):
                arr[0] = arr[0] * -1
            if(flipVertical):
                arr[1] = arr[1] * -1
            if(rotateAmount == 180):
                arr[0] = arr[0] * -1
                arr[1] = arr[1] * -1
            elif(rotateAmount == 270):
                # scale and rotate
                x = arr[0]
                y = arr[1]
                arr[0] = y * -0.5
                arr[1] = x * 0.5
            elif(rotateAmount == 90):
                # scale and rotate
                x = arr[0]
                y = arr[1]
                arr[0] = y * 0.5
                arr[1] = x * -0.5
                
        for item in arr:
            changeCoordinate(item)
    else:
        # recursive into object
        if(type(arr) == type({})):
            if arr.has_key('features'):
                changeCoordinate(arr['features'])
            if arr.has_key('geometry'):
                changeCoordinate(arr['geometry'])
            if arr.has_key('coordinates'):
                changeCoordinate(arr['coordinates'])

changeCoordinate(geojson)
outfile = open(source,'w')
outfile.write(json.dumps(geojson))
outfile.close()