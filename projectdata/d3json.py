__author__ = 'Rishikesh'

import json
import re
from operator import itemgetter

def converttod3json(filename):
    with open(filename,'r') as r_file:
        data = json.load(r_file)
        keyset = set()
        for dno,datum in enumerate(data):
            for key in datum:
                d3key = key.replace('$','').strip().replace(' ','_')
                keyset.add(d3key)
                val = datum[key]
                del datum[key]
                datum[d3key] = val
            data[dno]=datum
    print keyset
    d3file = filename.replace('.json','')+"_d3.json"
    print d3file
    f=open(d3file, 'w')
    f.write(json.dumps(data,ensure_ascii=True, sort_keys=True))
    f.flush()
    f.close()
    return d3file

def inplace_change(filename, old_string, new_string):
    s=open(filename).read()
    begin = s[0:2]
    if old_string in s[2:]:
            print 'Changing "{old_string}" to "{new_string}"'.format(**locals())
            s=begin + s[2:].replace(old_string, new_string)
            f=open(filename, 'w')
            f.write(s)
            f.flush()
            f.close()
    else:
            print 'No occurances of "{old_string}" found.'.format(**locals())
    return filename


filename = 'phoenixrestaurantsincome.json'
newfile = inplace_change(converttod3json(filename),'{"100000_to_124999":','\n{"100000_to_124999":')
with open(newfile,'r') as r_file:
    data = json.load(r_file)
    print data[0]