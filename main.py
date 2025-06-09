import csv
import os
import math
import json

from termcolor import colored, cprint

def indexed_color(index):
    colors = [
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
        "light_grey",
        "light_red",
        "light_green",
        "light_yellow",
        "light_blue",
        "light_magenta",
        "light_cyan"
    ]
    return colors[index % (len(colors) -1)]



try:
    columns, lines = os.get_terminal_size()
    print(f"Columns: {columns}, Lines: {lines}")
except OSError:
    print("Could not get the terminal size.")

data = []
with open('Data/data.json', 'r') as file:
    data = json.load(file)


def get_pokemon_by_id(id):
    return data["species"][id]

def get_pokemon_id_by_name(name):
    pokemon = data["species"]
    for p in pokemon:
        if(pokemon[p]["name"] == name or pokemon[p]["key"] == name):
            return str(pokemon[p]['ID'])

maxlen = 0
routes = {}
with open("Data/flat_encounters.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        location_name = row['Location']

        if len(location_name) > maxlen:
            maxlen = len(location_name)

        if(routes.get(location_name) == None):
            routes[location_name] = []
        routes[location_name].append([row['Pokemon'], row['Method'], row['Time']])

keys = ["wild-day", "wild-night", "wild-surf", "wild-oldRod", "wild-goodRod", "wild-superRod", "fixed-trade", "raid1", "raid2", "raid3", "raid4", "raid5" ,"raid6", "fixed-gift"]
game_corner_name = "Celadon City Game Corner Exchange"
subscriptable_keys = ["fixed-trade", "fixed-gift"]
routes = {}
for r in data["areas"]:
    name = r["name"]
    if len(name) > maxlen:
        maxlen = len(name)
    has_pokemon = False
    for k in r.keys():
        if k in keys:
            has_pokemon = True
            break
    if not has_pokemon:
        continue
    routes[name] = []
    def add_pokemon_to_route(name, key, method, time):
        #print("KEYS : " + str(r.keys()))
        if not key in r.keys():
            print(key + "    " + name + " Skipping " + key)
            return
        id = 0
        for n in r[key].keys(): # not sure what this number is used for
            def append_pokemon(id):
                id = id
                if id == 0:
                    return
                pokemon = get_pokemon_by_id(str(id))
                m = method
                if (key == "fixed-gift" and name == game_corner_name):
                    m = "Game Corner"
                routes[name].append({
                    "method" : m,
                    "time" : time,
                    "id" : str(id),
                    "pokemon_data" : pokemon,
                    "name" : pokemon["name"]
                })
            if key in subscriptable_keys:
                #print(key + "    " + name + " & " + key + "\n\t" + str(p) + "\n\t" + str(n) + "\n\t" + str(r[key]))
                for pokemon_id in r[key][n]:
                    append_pokemon(pokemon_id)
            else:        
                for p in r[key][n]:
                    append_pokemon(p[0])



    add_pokemon_to_route(name, "wild-day", "Wild", "Day")
    add_pokemon_to_route(name, "wild-night", "Wild", "Night")
    add_pokemon_to_route(name, "wild-surf", "Surf", "All")
    add_pokemon_to_route(name, "wild-oldRod", "Old Rod", "All")
    add_pokemon_to_route(name, "wild-goodRod", "Good Rod", "All")
    add_pokemon_to_route(name, "wild-superRod", "Super Rod", "All")
    add_pokemon_to_route(name, "fixed-trade", "Trade", "All")
    add_pokemon_to_route(name, "fixed-gift", "Gift", "All")
    add_pokemon_to_route(name, "raid1", "Raid", "All")
    add_pokemon_to_route(name, "raid2", "Raid", "All")
    add_pokemon_to_route(name, "raid3", "Raid", "All")
    add_pokemon_to_route(name, "raid4", "Raid", "All")
    add_pokemon_to_route(name, "raid5", "Raid", "All")
    add_pokemon_to_route(name, "raid6", "Raid", "All")






column_size = maxlen + 12
printable_columns = math.floor(columns / column_size)
print("P COLUMNS : " + str(printable_columns))
def route_select():
    print("Routes and Locations : ")
    index = 1
    for k in routes.keys():
        prntstr = "\t("+str(index)+") " + k
        extra_space = " " * (column_size - len(prntstr))

        cprint(prntstr + extra_space, indexed_color(index),end="")
        if(index % printable_columns == 0 and index != 0):
            print()
        index += 1
    print()
    handle_input()



def handle_input():
    selection = input("Enter Route Index : ")
    if(not selection.isdigit()):
        print("Incorrect input, must be an index.")
        handle_input()
    elif(int(selection) > len(routes.keys()) or int(selection) <= 0):
        print("Index is out of range.")
        handle_input()
    else:
        display_pokemon_on_route(int(selection) -1 )

def display_pokemon_on_route(route_index):
    keys = list(routes.keys())
    route = routes[keys[route_index]]
    for pokemon in route:
        display_pokemon(pokemon)

method_color = {
    'Wild' : 'light_green',
    'Surf' : 'blue',
    'Game Corner' : 'magenta',
    'Old Rod' : 'cyan',
    'Good Rod' : 'cyan',
    'Super Rod' : 'cyan',
    'Raid' : 'light_red',
    "Gift" : "light_magenta",
    "Trade" : "yellow"
}

time_color = {
    'Day' : 'light_yellow',
    'Night' : 'blue',
    'All' : 'white'
}

def display_pokemon(pokemon):
    cprint(pokemon["name"], attrs=["bold"])
    cprint("\t"+pokemon["method"], method_color[pokemon["method"]])
    cprint("\t"+pokemon["time"], time_color[pokemon["time"]])


route_select()

import base64
from term_image.image import from_file

def display_image():
    img_data = b'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'
    img_data = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAAXNSR0IArs4c6QAAAtJJREFUeF7tmsuRwjAMhs2NMiiBY8rgmBJzpIwcKYEyuMGYwTNGSPYvvzbreI+L7Oj/9PAjOZid/x12rt8MACMDGhJY1/V5v9/NPM/sU5dlMafTyUzT1CwzmzxoWZanJFrib2HM81zdv6oPSBFOgdQGUQVACeGtQBQHgIh3te6LDPUGZ1cjG0oDeIZq+nK5QC33er2KjfIzQTG/i01kjGHF26ihwimdCIgivheZRBL/eDygiMeMjsejZJLtf/YEUs2HxN9uN1bQ+XwWWXAQSvSELABa8VY4shGSQNSAkAWAS30p8oE0ZqOunCdZR/JALvqc01IjW9fVuEjbzJim6QeE1EApzJxSSAZAo885y4n3hVPFHAh0XmPSTrZJANDo00ihqwIyrlQWJAFAok8dpJH3ox36zWUJhSeUllqPeoA90tJ6pc5xqUxtYlGOAbRgOBvtUVoNAEl/Ljq5ALheUKIM1ABi6S919FwANuK0VEqUQTYApH6p89RxGl0JIvgslSaV8achfR16QKfeQ20WUPHcsihtmsBnqTSpjHMB0HWfWxZDO8auAIDL2hezTQJA6zcWfeSssIkmmLoMcnd87qIEuAEym1kGUzdCsUuP2O9Is7Q21TdCXCNEokMFIqdBfwzYM9RNXT3AOoWUAbdVdYK4aEprv1s+KcASu0A7ZxIANAuQuwAnTHMnUGIH6J6bDADNAgSCRjyXWX91IWJ9+bkKV15lib1POU9yIJMHSr1Aqln7/x4vRdmGGILgQHCh/3fX4p4I9q0QegUW2wNs+sVIDMJeXo05Drt+OfqGsPfX4zCEWN1zh6can8xkLYMxEUg2AHNU/VaoKgAnLgVEzu4uBtX/vQkA7xC0z8/kNBFpbds0A1qLQ543ACCUerYZGdBzdBFtIwMQSj3bjAzoObqItpEBCKWebUYG9BxdRNvIAIRSzzYjA3qOLqJtZABCqWebF5RwLF+j0HPvAAAAAElFTkSuQmCC'
    import base64
    with open("imageToSave.png", "wb") as fh:
        fh.write(base64.decodebytes(img_data))

    image = from_file("imageToSave.png")
    image.set_size(width = 50, height = 25)
    image.draw(h_align="left", v_align="top", pad_height = 25, pad_width=50, check_size = False)
    image.close()

display_image()