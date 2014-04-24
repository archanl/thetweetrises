allCoordinates = open("oneState.txt",'r')
allLines = allCoordinates.readlines()
outputLines = open("convertedState.txt", 'w')

# We want to convert <point lat="71.2249" lng="-159.6313"/>
# to new google.maps.LatLng(38.4385, -82.3425),

# We extract the name of the state
stateName = allLines[0].split("=")[1].split("\"")[1]
# We print our JS variable 
outputLines.writelines("var " + stateName + "\n \n")
# We print our JS outline
outputLines.writelines("var " + stateName + "Outline = [ \n")
for coordinate in allLines[1:-2]:
    lat = float(coordinate.split("=")[1].split("\"")[1])
    lng = float(coordinate.split("=")[2].split("\"")[1])
    outputLines.writelines("  new google.maps.LatLng(" + str(lat) + ", " + str(lng) + "),\n")

lastLat = float(allLines[-2].split("=")[1].split("\"")[1])
lastLng = float(allLines[-2].split("=")[2].split("\"")[1])
outputLines.writelines("  new google.maps.LatLng(" + str(lastLat) + ", " + str(lastLng) + ")\n")
outputLines.writelines("]; \n \n")

# We construct our polygon
outputLines.writelines(stateName + " = new google.maps.Polygon({ \n")
outputLines.writelines("  paths: " + stateName + "Outline, \n")
outputLines.writelines("  strokeColor: '#000000', \n")
outputLines.writelines("  strokeOpacity: 0.9, \n")
outputLines.writelines("  strokeWeight: 2, \n")
outputLines.writelines("  fillColor: '#000000', \n")
outputLines.writelines("  fillOpacity: 0.50 \n")
outputLines.writelines("}); \n \n")

outputLines.close()
