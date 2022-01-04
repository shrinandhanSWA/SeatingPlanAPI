from pymongo import MongoClient
from main import get_module

client = MongoClient(
    "mongodb+srv://admin:ZpwHfTeZDM2ACkBM@cluster0.vqrib.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.myFirstDatabase

# get LT3
category = get_module('c1234-2', db)
students = category["students"]

new_hall = {"name": "LTUG"}

for student in students:
    if student["wildCard1"] == '' and student["wildCard2"] == '':
        student["wild"] = 'N'
    else:
        student["wild"] = 'Y'

category["students"] = students

this_db = db["categories"]
this_db.save(category)

"""

{
  "layout": [
    [
      [
        {
          "gender": "Male", 
          "group": "19S Group 9", 
          "name": "Laurel Buchanan", 
          "nationality": "Sweden", 
          "username": "zjf19", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 8", 
          "name": "Brianna Morrison", 
          "nationality": "United States", 
          "username": "nl1119", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 1", 
          "name": "Troy Moran", 
          "nationality": "Brazil", 
          "username": "dr1817", 
          "wild": "Y"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 7", 
          "name": "Tana Osborn", 
          "nationality": "United Kingdom", 
          "username": "ge19", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 10", 
          "name": "Clark Hale", 
          "nationality": "Netherlands", 
          "username": "ga5318", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 6", 
          "name": "Astra Reynolds", 
          "nationality": "South Korea", 
          "username": "pt719", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 7", 
          "name": "Tatiana Adams", 
          "nationality": "Mexico", 
          "username": "nd619", 
          "wild": "Y"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 10", 
          "name": "Irma Langley", 
          "nationality": "Belgium", 
          "username": "cc9718", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 2", 
          "name": "Philip Leblanc", 
          "nationality": "Peru", 
          "username": "am2219", 
          "wild": "N"
        }
      ], 
      [
        {
          "gender": "Female", 
          "group": "19S Group 8", 
          "name": "Jocelyn Mcpherson", 
          "nationality": "Austria", 
          "username": "smw19", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 2", 
          "name": "Cruz Wall", 
          "nationality": "Turkey", 
          "username": "rh1819", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 8", 
          "name": "Tyler Rosario", 
          "nationality": "Indonesia", 
          "username": "rgm19", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 4", 
          "name": "Gabriel Alston", 
          "nationality": "China", 
          "username": "mjk19", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 3", 
          "name": "Gil Sykes", 
          "nationality": "Colombia", 
          "username": "jr1519", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 2", 
          "name": "Bree Duke", 
          "nationality": "Vietnam", 
          "username": "bts19", 
          "wild": "Y"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 5", 
          "name": "Troy Anderson", 
          "nationality": "Nigeria", 
          "username": "ss7319", 
          "wild": "N"
        }
      ]
    ], 
    [
      [
        {
          "gender": "Male", 
          "group": "19S Group 1", 
          "name": "Aurora Rowland", 
          "nationality": "France", 
          "username": "oo1117", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 5", 
          "name": "Aquila Potter", 
          "nationality": "United States", 
          "username": "nj719", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 9", 
          "name": "Ulysses Bernard", 
          "nationality": "New Zealand", 
          "username": "nak19", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 3", 
          "name": "Alika Winters", 
          "nationality": "Sweden", 
          "username": "mha13", 
          "wild": "Y"
        }
      ]
    ], 
    [
      [
        {
          "gender": "Male", 
          "group": "19S Group 10", 
          "name": "Amery Hernandez", 
          "nationality": "India", 
          "username": "fcd18", 
          "wild": "Y"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 6", 
          "name": "Wade O'connor", 
          "nationality": "Netherlands", 
          "username": "etg19", 
          "wild": "Y"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 5", 
          "name": "Reagan Mathis", 
          "nationality": "Costa Rica", 
          "username": "co119", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 9", 
          "name": "Montana Young", 
          "nationality": "United Kingdom", 
          "username": "cbl19", 
          "wild": "Y"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 11", 
          "name": "Samson Heath", 
          "nationality": "Poland", 
          "username": "am16918", 
          "wild": "N"
        }, 
        {
          "gender": "", 
          "group": "", 
          "name": 26, 
          "nationality": "", 
          "username": ""
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 3", 
          "name": "Laurel Saunders", 
          "nationality": "South Korea", 
          "username": "yt2619", 
          "wild": "Y"
        }
      ]
    ], 
    [
      [
        {
          "gender": "Male", 
          "group": "19S Group 2", 
          "name": "Samantha Hernandez", 
          "nationality": "Mexico", 
          "username": "tv419", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 11", 
          "name": "Constance Madden", 
          "nationality": "Peru", 
          "username": "fong97", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 2", 
          "name": "Kirby Ball", 
          "nationality": "Belgium", 
          "username": "aao519", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 8", 
          "name": "Berk Caldwell", 
          "nationality": "Austria", 
          "username": "yz13219", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 7", 
          "name": "Neil Simon", 
          "nationality": "Netherlands", 
          "username": "wrn119", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 6", 
          "name": "Addison O'brien", 
          "nationality": "Chile", 
          "username": "vs1619", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 3", 
          "name": "Katelyn Mercado", 
          "nationality": "Brazil", 
          "username": "sl7319", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 8", 
          "name": "Quemby Anderson", 
          "nationality": "Italy", 
          "username": "sl5419", 
          "wild": "Y"
        }
      ]
    ], 
    [
      [
        {
          "gender": "Male", 
          "group": "19S Group 9", 
          "name": "Kenneth Waters", 
          "nationality": "Colombia", 
          "username": "sk2919", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 5", 
          "name": "Jacqueline Buck", 
          "nationality": "Indonesia", 
          "username": "sa3819", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 6", 
          "name": "Honorato Kelley", 
          "nationality": "United States", 
          "username": "mma919", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 11", 
          "name": "Maia Rodgers", 
          "nationality": "United Kingdom", 
          "username": "koshinye", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 5", 
          "name": "Knox Bass", 
          "nationality": "Canada", 
          "username": "jtn19", 
          "wild": "N"
        }
      ]
    ], 
    [
      [
        {
          "gender": "Male", 
          "group": "19S Group 5", 
          "name": "Dustin Humphrey", 
          "nationality": "China", 
          "username": "jkk19", 
          "wild": "Y"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 8", 
          "name": "Richard Gaines", 
          "nationality": "Germany", 
          "username": "hk1919", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 1", 
          "name": "Gisela Peters", 
          "nationality": "Sweden", 
          "username": "gm719", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 10", 
          "name": "Quinn Beach", 
          "nationality": "Turkey", 
          "username": "bpb10", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 7", 
          "name": "Levi Travis", 
          "nationality": "Russian Federation", 
          "username": "bo219", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 4", 
          "name": "Kamal Bell", 
          "nationality": "Vietnam", 
          "username": "ajc419", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 11", 
          "name": "Cara Dillard", 
          "nationality": "Pakistan", 
          "username": "acg07", 
          "wild": "Y"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 10", 
          "name": "Florence Bradley", 
          "nationality": "Spain", 
          "username": "aao1519", 
          "wild": "N"
        }
      ]
    ], 
    [
      [
        {
          "gender": "Female", 
          "group": "19S Group 10", 
          "name": "Cheyenne Holden", 
          "nationality": "Mexico", 
          "username": "nd1119", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 8", 
          "name": "Kieran Rodgers", 
          "nationality": "Peru", 
          "username": "nak119", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 7", 
          "name": "Sharon Duffy", 
          "nationality": "Belgium", 
          "username": "gg719", 
          "wild": "Y"
        }
      ]
    ], 
    [
      [
        {
          "gender": "", 
          "group": "", 
          "name": 52, 
          "nationality": "", 
          "username": ""
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 1", 
          "name": "Chiquita Pittman", 
          "nationality": "South Korea", 
          "username": "fk2818", 
          "wild": "Y"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 3", 
          "name": "Kennan Morin", 
          "nationality": "India", 
          "username": "tp519", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 2", 
          "name": "Arsenio Curry", 
          "nationality": "Sweden", 
          "username": "owa19", 
          "wild": "Y"
        }
      ]
    ], 
    [
      [
        {
          "gender": "Female", 
          "group": "19S Group 4", 
          "name": "Tiger Davis", 
          "nationality": "Poland", 
          "username": "orc19", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 6", 
          "name": "Dora Bryan", 
          "nationality": "United States", 
          "username": "nr1519", 
          "wild": "Y"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 11", 
          "name": "Flynn Knox", 
          "nationality": "New Zealand", 
          "username": "nae19", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 1", 
          "name": "Azalia Dunlap", 
          "nationality": "Netherlands", 
          "username": "mr1319", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 1", 
          "name": "Dennis Meadows", 
          "nationality": "Nigeria", 
          "username": "kkv19", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 9", 
          "name": "Wynne Abbott", 
          "nationality": "France", 
          "username": "hw2619", 
          "wild": "Y"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 6", 
          "name": "Simone Matthews", 
          "nationality": "United Kingdom", 
          "username": "he219", 
          "wild": "N"
        }
      ]
    ], 
    [
      [
        {
          "gender": "Female", 
          "group": "19S Group 1", 
          "name": "Adrienne Peters", 
          "nationality": "Costa Rica", 
          "username": "dh1818", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 9", 
          "name": "Ashton Sanders", 
          "nationality": "Vietnam", 
          "username": "pp319", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 4", 
          "name": "Omar Terrell", 
          "nationality": "Indonesia", 
          "username": "nft19", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 5", 
          "name": "Myles Little", 
          "nationality": "Turkey", 
          "username": "ks2419", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 11", 
          "name": "Zephania Patrick", 
          "nationality": "Austria", 
          "username": "hl2019", 
          "wild": "Y"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 11", 
          "name": "Griffin Orr", 
          "nationality": "Colombia", 
          "username": "er19", 
          "wild": "Y"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 3", 
          "name": "Gisela Eaton", 
          "nationality": "China", 
          "username": "awl2518", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 7", 
          "name": "Ian Price", 
          "nationality": "Belgium", 
          "username": "sf1419", 
          "wild": "N"
        }
      ]
    ], 
    [
      [
        {
          "gender": "Female", 
          "group": "19S Group 6", 
          "name": "Noelle Slater", 
          "nationality": "South Korea", 
          "username": "rme19", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 4", 
          "name": "Julie Lindsey", 
          "nationality": "Mexico", 
          "username": "pd219", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 9", 
          "name": "Teegan Valenzuela", 
          "nationality": "Peru", 
          "username": "jml219", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 10", 
          "name": "Inga Osborne", 
          "nationality": "Sweden", 
          "username": "sai19", 
          "wild": "N"
        }, 
        {
          "gender": "Female", 
          "group": "19S Group 7", 
          "name": "Petra Schroeder", 
          "nationality": "Netherlands", 
          "username": "ima00", 
          "wild": "Y"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 4", 
          "name": "Xanthus Young", 
          "nationality": "United Kingdom", 
          "username": "dd619", 
          "wild": "N"
        }, 
        {
          "gender": "Male", 
          "group": "19S Group 4", 
          "name": "Brendan Dalton", 
          "nationality": "United States", 
          "username": "aim109", 
          "wild": "Y"
        }
      ]
    ]
  ], 
  "status": "success"
}



"""
