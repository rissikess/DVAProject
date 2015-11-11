#http://data.fcc.gov/api/block/2010/find?latitude=40.0&longitude=-85&format=jso
import json
import ast
import time

inputfile = open('phoenixrestaurants.json', 'r')
datafile = open('age_block_group.csv', 'r')
outputfile = open('phoenixrestaurantsage.json', 'w')

input_lines = inputfile.read()
data_lines = datafile.readlines()
header = [i.split(";")[1] for i in data_lines[0].split(",")[1:]]
block_group_data = {i.split(",")[0].strip():i.split(",")[1:] for i in data_lines[1:]}
input_lines = json.loads(input_lines)
print(len(input_lines))

for line in input_lines:
    print(input_lines.index(line))
    obj = line
    block_group_id = line['block_id']
    if(block_group_id[1:len(block_group_id)-3] in block_group_data):
        for field in range(0,len(header), 2):
            fieldname = header[field].split("-")[0].strip() + header[field].split("-")[1].strip().split("to")[0].strip() + " to " + header[field + 1].split("-")[1].strip().split("to")[1].strip()
            obj[fieldname] = int(block_group_data[block_group_id[1:len(block_group_id)-3]][field]) + int(block_group_data[block_group_id[1:len(block_group_id)-3]][field + 1])
    input_lines[input_lines.index(line)] = obj
        
for item in input_lines:    
    outputfile.write(json.dumps(item) + ",\n")

outputfile.close()
inputfile.close()
datafile.close()
