import json
import ast

import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

input_file = open('phoenixrestaurantsage.json', 'r')
income_file = open('phoenixrestaurantsincome.json', 'r')
output_file = open('db_age.txt', 'w')

input_lines = input_file.read()
input_lines = json.loads(input_lines)

income_lines = income_file.read()
income_lines = json.loads(income_lines)

for line in input_lines:
    for income in income_lines:
        if(income['block_id'] == line['block_id']):
            for key in income:
                if(key not in line):
                    line[key] = income[key]
            break

keyvalues = set()
'''
for key in input_lines[0]:
    if(type(input_lines[0][key]) != dict):
        keyvalues += key + ","
    else:
        for inner_key in input_lines[0][key]:
            if(type(input_lines[0][key][inner_key]) != dict):
                keyvalues += inner_key
            else:
                for inner_inner_key in input_lines[0][key][inner_key]:
                    keyvalues += inner_key + "_" + inner_inner_key + ","

keyvalues = keyvalues[0:len(keyvalues)-1]
output_file.write(keyvalues + "\n")
'''

linevalues = dict()
lines = []

for line in input_lines:
    linevalues = dict()
    print(input_lines.index(line))
    for key in line:
        if(type(line[key]) != dict and type(line[key]) != list):
            linevalues[key] = line[key]
            keyvalues.add(key)
        elif(type(line[key]) == list):
            keyvalues.add(key)
            linevalues[key] = ",".join(line[key])
        else:
            for inner_key in line[key]:
                if(type(line[key][inner_key]) != dict):
                    keyvalues.add(inner_key)
                    linevalues[inner_key] = line[key][inner_key]
                else:
                    for inner_inner_key in line[key][inner_key]:
                        keyvalues.add(inner_key + "_" + inner_inner_key)
                        linevalues[inner_key + "_" + inner_inner_key] = line[key][inner_key][inner_inner_key]
    #print(linevalues)
    #linevalues = linevalues.encode('utf8')
    #linevalues = linevalues[0:len(linevalues) - 1]
    try:
        #output_file.write(str(linevalues) + "\n")
        lines.append(linevalues)
    except Exception as e:
        print(linevalues)

for obj in lines:
    for key in keyvalues:
        if(key not in obj):
            obj[key] = "null"
    output_file.write(str(obj) + "\n")

output_file.write(",".join(keyvalues))
output_file.close()
input_file.close()