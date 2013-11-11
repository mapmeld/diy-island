# linemeet.py
# turn coastline of multiple LineStrings into island Polygons

import sys, json

source = sys.argv[1]
gjfile = open(source,'r')
geojson = json.load(gjfile)
gjfile.close()

for feature in geojson["features"]:
    if feature["geometry"]["type"] == "LineString":
        closeMatch = 0.00008
        closestMatch = None
        closeEnd = "start"
        for matchline in geojson["features"]:
            if matchline == feature or (matchline.has_key("null") and matchline["null"] == "null"):
                continue
            myPt = feature["geometry"]["coordinates"][0]
            pPt = matchline["geometry"]["coordinates"][0]
            distance = ((myPt[0] - pPt[0])**2 + (myPt[1] - pPt[1])**2)**0.5
            if distance < closeMatch:
                closestMatch = matchline
                closeMatch = distance
                closeEnd = "start"
            pPt = matchline["geometry"]["coordinates"][len(matchline["geometry"]["coordinates"])-1]
            distance = ((myPt[0] - pPt[0])**2 + (myPt[1] - pPt[1])**2)**0.5
            if distance < closeMatch:
                closestMatch = matchline
                closeMatch = distance
                closeEnd = "end"
            
        if closestMatch is not None:
            # join up
            feature["null"] = "null"
            if closeEnd == "start":
                feature["geometry"]["coordinates"].reverse()
                closestMatch["geometry"]["coordinates"] = feature["geometry"]["coordinates"] + closestMatch["geometry"]["coordinates"]
            else:
                closestMatch["geometry"]["coordinates"] = closestMatch["geometry"]["coordinates"] + feature["geometry"]["coordinates"]

polygons = [ ]
for polygon in geojson["features"]:
    if polygon.has_key("null") and polygon["null"] == "null":
        continue
    polygons.append(polygon)
    polygon["geometry"]["type"] = "Polygon"
    polygon["geometry"]["coordinates"] = [polygon["geometry"]["coordinates"]]
    polygon["geometry"]["coordinates"][0].append(polygon["geometry"]["coordinates"][0][0])
geojson["features"] = polygons

outfile = open(source,'w')
outfile.write(json.dumps(geojson))
outfile.close()