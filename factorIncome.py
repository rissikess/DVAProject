__author__ = 'Rishikesh'

import json
import re
import csv
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
#import set


def inplace_change(filename, old_string, new_string):
    s=open(filename).read()
    if old_string in s:
            print 'Changing "{old_string}" to "{new_string}"'.format(**locals())
            s=s.replace(old_string, new_string)
            f=open(filename, 'w')
            f.write(s)
            f.flush()
            f.close()
    else:
            print 'No occurances of "{old_string}" found.'.format(**locals())

def formatyelpjson(filename):
    inplace_change(filename,'{"business_id":',',\n{"business_id":')

    #sample = '"block_id": 999999754011003}'
    #output = re.sub(r'"block_id": ([0-9]*)}', r'"block_id": "\1"}', sample)
    #print output
    s=open(filename).read()
    s = s.replace(',\n','',1)
    s = s.replace('","intersection":[','')
    s=re.sub(r'"block_id": (.*)}', r'"block_id": "\1"}', s)
    s = '['+s+']'
    f=open(filename, 'w')
    f.write(s)
    f.flush()
    f.close()


def getyelpjsonbyparams(filename, city, state, category):
    wfile = 'projectdata\\'+city + category +'.json'
    with open(wfile,'w') as wrfile:
        wrfile.write('[')
        with open(filename) as data_file:
           data = json.load(data_file)
           #print data[0]
           totcount = 0
           citycount = 0
           catcount = 0
           for datum in data:
               totcount+=1
               if datum['city'].lower()==city and datum['state'].lower()==state:
                   citycount+=1
                   if 'restaurants' in [x.lower() for x in datum['categories']]:
                       catcount+=1
                       if catcount>1:
                           wrfile.write(',\n')
                       wrfile.write(json.dumps(datum))
        wrfile.write(']')
        print "totcount = ", totcount, " ", city, " count = ", citycount, " ",category," count = ", catcount


def getyelpincomejson(city, state, category):
    wfile = 'projectdata\\'+ city + category +'.json'
    with open(wfile,'r') as r_file:
        catdata = json.load(r_file)
        newcatdata = []
        ncnt = 0
        #print data[0]
        with open('projectdata\\'+city + category + 'income.json','w') as wrincfile:
            wrincfile.write('[')
            with open('maricopaincome\income breakdown.csv','r') as incfile:
                incomereader = csv.DictReader(incfile)
                incomedict = {row['Id2']: row for row in incomereader}
                #print inc
                invid = 0
                errcount = 0
                for datum in catdata:
                    key = datum['block_id'][1:-3]
                    if not re.match(r'[0-9]{11}', key):
                        invid+=1
                        continue
                    breakdown = incomedict[key]
                    #print breakdown
                    total = 0
                    for inclevel in breakdown:
                        if 'MoE' not in inclevel and inclevel!='Id' and inclevel!='Id2' and inclevel!='Geography':
                            incparts = inclevel.strip().replace(',','').replace('$','').split(' to ')
                            if len(incparts)>1 and (int)(incparts[1]) <=24999:
                                newkey = '$10000 to $24999'
                                datum[newkey] = datum.get(newkey,0)+(int)(breakdown[inclevel])
                                total = total + (int)(breakdown[inclevel])
                                #print newkey,inclevel,breakdown[inclevel],' ',total
                            elif len(incparts)>1 and (int)(incparts[1]) <=49999:
                                newkey =  '$25000 to $49999'
                                datum[newkey] = datum.get(newkey,0)+(int)(breakdown[inclevel])
                                total = total + (int)(breakdown[inclevel])
                                #print newkey,inclevel,breakdown[inclevel],' ',total
                            elif len(incparts)>1 and (int)(incparts[1]) <=74999:
                                newkey =  '$50000 to $74999'
                                datum[newkey] = datum.get(newkey,0)+(int)(breakdown[inclevel])
                                total = total + (int)(breakdown[inclevel])
                                #print newkey,inclevel,breakdown[inclevel],' ',total
                            elif 'Total' not in inclevel:
                                newkey = inclevel.replace(',','')
                                datum[newkey] = (int)(breakdown[inclevel])
                                total = total + (int)(breakdown[inclevel])
                                #print newkey,inclevel,breakdown[inclevel],' ',total
                            else:
                                brktotal = (int)(breakdown[inclevel])
                                #print 'Total',inclevel,breakdown[inclevel],' ',total
                    if total - brktotal != 0:
                        #print total, " ", brktotal, " ","total error!!"
                        errcount+=1
                    newcatdata.append(datum)
                    ncnt+=1
                    if ncnt>1:
                           wrincfile.write(',\n')
                    wrincfile.write(json.dumps(datum))
            wrincfile.write(']')
                    #print newcatdata
                    #break
    print invid
    print errcount
    #with open('maricopaincome\yelpincome.json','w') as wrincfile:
    #    wrincfile.write(json.dumps(newcatdata))



def doPCA(city, state, category):
    with open('projectdata\\'+city + category + 'income.json','r') as r_file:
            data = json.load(r_file)
            keyset =set()
            newdata = []
            for datum in data:
               newdatum = {}
               for key in datum:
                   if isinstance(datum[key], int) or isinstance(datum[key], long) or isinstance(datum[key], float) \
                           or isinstance(datum[key], str) or isinstance(datum[key], bool):
                       newdatum[key] = datum[key]
                       keyset.add(key)
                   elif isinstance(datum[key],dict):
                       for subkey in datum[key]:
                           keyset.add(subkey)
                   else:
                       keyset.add(key)
               newdata.append(newdatum)
            #print keyset
            dv = DictVectorizer(sparse=False)
            vectdata = dv.fit_transform(newdatum)
            print vectdata[0]
            vectpca = PCA(n_components=4)
            vectpca.fit(vectdata)

            correlation = []
            for var in vectdata:
                for comp in vectpca.components_:
                    corr = pearsonr(var, comp)
                    print corr
                    correlation.append(corr)

            for i in range(len(correlation)):
                print correlation[i]

            print correlation[0]
            #print correlation[1]



#filename = 'DataVizProject\sample.txt'
filename = 'DataVizProject\yelp_business_id_block_id_lat_long_state.txt'
city = 'phoenix'
state = 'az'
category = 'restaurants'

#formatyelpjson(filename) # call only once!!
getyelpjsonbyparams(filename,city,state,category)
getyelpincomejson(city,state,category)
doPCA(city,state,category)






