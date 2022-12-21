import json

json_data = {
    'position1': '516, 440',
    'position2': '971, 443',
    'position3': '1186, 439',
    'position4': '1402, 441',
    'position5': '1630, 449',
    'position6': '299, 681',
    'position7': '518, 684',
    'position8': '736, 691',
    'position9': '739, 431'
}

data = json.dumps(json_data)
print(data)

f = open("file.json", "w")
f.write(data)
f.close()