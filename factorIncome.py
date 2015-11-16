__author__ = 'Rishikesh'

import json
import re
import csv
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from operator import itemgetter
import unicodedata
from sklearn.svm import LinearSVC, SVC, SVR, NuSVC,NuSVR

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier
from sklearn.cross_validation import train_test_split, StratifiedShuffleSplit
#import mlpy
#from mlpy import KFDA
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



def doAnalysis(city, state, category, k=10):
    with open('projectdata\\'+city + category + 'income.json','r') as r_file:
            data = json.load(r_file)
            keyset =set()
            unkeyset = set()
            unkvalueset  =set()
            newdata = []
            nbnewdata = []
            flabels = []
            fnewdata = []
            labels = []
            nblabels = []
            maxfeats = 0
            for dno,datum in enumerate(data):
                #if datum["stars"]>=3.0:
               newdatum = {}
               label = {}
               featcnt = 0
               for key in datum:
                   if key == "stars":
                       #labels.append(datum[key])
                       #label[key] = str(datum[key])
                       #labels.append(str(datum[key]))

                       ##jj
                       # if datum[key] <= 2.5:
                       # #if datum[key]==3.0: #and datum[key] <= 3.5:
                       #     labels.append("B")
                       #     #nblabels.append("na")
                       # # elif datum[key] >= 4.5:
                       # #     labels.append("G")
                       # #else:
                       # #elif datum[key] == 3.5:

                       if datum[key] > 2.5:
                           labels.append("NB")
                           if datum[key] >= 4.5:
                               nblabels.append("EG")
                           # elif datum[key] >= 3.5:
                           #     nblabels.append("G")
                           else:
                               nblabels.append("G")
                               if datum[key]==3.0:
                                   flabels.append("F")
                               else:
                                   flabels.append("AAvg")
                       # else:
                       #     labels.append("G")
                       else:
                           labels.append("PB")
                   elif key!="name" and key!="business_id" and key!="full_address" and key!="latitude" and key!="longitude" and key!="hours" and key[0]!=" " and key[0]!="$" and key!='review_count':
                       if isinstance(datum[key], int) or isinstance(datum[key], long) or isinstance(datum[key], float) \
                               or isinstance(datum[key], str) or isinstance(datum[key], bool):
                           newdatum[key] = datum[key]
                           keyset.add(key)
                           featcnt+=1
                       elif isinstance(datum[key],dict):
                           for subkey in datum[key]:
                               if isinstance(datum[key][subkey], int) or isinstance(datum[key][subkey], long) or \
                                       isinstance(datum[key][subkey], float) or isinstance(datum[key][subkey], str) or \
                                       isinstance(datum[key][subkey], bool):
                                   newdatum[key+" "+subkey] = datum[key][subkey]
                                   keyset.add(subkey)
                                   featcnt+=1
                               elif isinstance(datum[key][subkey], unicode):
                                   ascval = unicodedata.normalize('NFKD', datum[key][subkey]).encode('ascii','ignore')
                                   newdatum[key+" "+subkey] = ascval
                                   keyset.add(subkey)
                                   featcnt+=1
                               elif isinstance(datum[key][subkey],dict):
                                   for subsubkey in datum[key][subkey]:
                                       if isinstance(datum[key][subkey][subsubkey], int) or \
                                               isinstance(datum[key][subkey][subsubkey], long) or \
                                               isinstance(datum[key][subkey][subsubkey], float) or \
                                               isinstance(datum[key][subkey][subsubkey], str) or \
                                               isinstance(datum[key][subkey][subsubkey], bool):
                                           newdatum[key+" "+subkey+" "+subsubkey] = datum[key][subkey][subsubkey]
                                           keyset.add(subsubkey)
                                           featcnt+=1
                                       elif isinstance(datum[key][subkey][subsubkey], unicode):
                                           ascval = unicodedata.normalize('NFKD', datum[key][subkey][subsubkey]).encode('ascii','ignore')
                                           newdatum[key+" "+subkey+" "+subsubkey] = ascval
                                           keyset.add(subsubkey)
                                           featcnt+=1
                                       else:
                                           unkeyset.add(key+ " "+subsubkey)
                                           unkvalueset.add(type(datum[key][subkey][subsubkey]))

                               else:
                                   unkeyset.add(key+ " "+subkey)
                                   unkvalueset.add(type(datum[key][subkey]))
                       elif isinstance(datum[key],list):
                           for itnum, item in enumerate(datum[key]):
                               if isinstance(item, int) or isinstance(item, long) or isinstance(item, float) or \
                                       isinstance(item, str) or isinstance(item, bool):
                                   newdatum[key +" "+str(item)] = True
                                   keyset.add(key)
                                   featcnt+=1
                               elif isinstance(item, unicode):
                                   ascval = unicodedata.normalize('NFKD', item).encode('ascii','ignore')
                                   newdatum[key +" "+ascval] = True
                                   keyset.add(key)
                                   featcnt+=1
                               else:
                                   unkeyset.add(key)
                                   unkvalueset.add(type(item))
                       else:
                            if isinstance(datum[key], unicode):
                                ascval = unicodedata.normalize('NFKD', datum[key]).encode('ascii','ignore')
                                newdatum[key] = ascval
                                keyset.add(key)
                                featcnt+=1
                            else:
                                unkeyset.add(key)
                                unkvalueset.add(type(datum[key]))
               newdata.append(newdatum)
               if datum["stars"] > 2.5:
                    nbnewdata.append(newdatum)
                    if datum["stars"] < 4.5:
                        fnewdata.append(newdatum)
               if featcnt > maxfeats:
                   maxfeats = featcnt
               #labels.append(label)
            #print keyset
            print unkeyset
            print unkvalueset
            # for unk in unkeyset:
            #     if isinstance(unk, unicode):
            #         print "yeah"
            #     else:
            #         print "nah"
            dv = DictVectorizer(sparse=False)
            vectdata = dv.fit_transform(newdata)
            #print vectdata[0]


            nbdv = DictVectorizer(sparse=False)
            nbvectdata = nbdv.fit_transform(nbnewdata)
            #print nbvectdata[0]

            fdv = DictVectorizer(sparse=False)
            fvectdata = fdv.fit_transform(fnewdata)
            #print nbvectdata[0]
            print len(flabels), len(fnewdata), len(fvectdata)
            # split = (int)(round(len(vectdata)*0.7))
            # print split
            # traindata = vectdata[0:split]
            # trainlabels = labels[0:split]
            # testdata = vectdata[split:]
            # testlabels = labels[split:]

            #traindata, testdata, trainlabels, testlabels = train_test_split(vectdata, labels, test_size=0.33, random_state=42, stratify=)
            #nbtraindata, nbtestdata, nbtrainlabels, nbtestlabels = train_test_split(vectdata, nblabels, test_size=0.33, random_state=42)
            traindata = []
            trainlabels =[]
            testdata = []
            testlabels = []

            sssidxs = StratifiedShuffleSplit(labels, n_iter=1, test_size=0.7, random_state=0)
            #print len(sssidxs)
            for train_index, test_index in sssidxs:
                #print train_index#, test_index
                #print("TRAIN:", train_index, "TEST:", test_index)
                traindata, testdata = vectdata[train_index], vectdata[test_index]
                for tr_idx in train_index:
                    trainlabels.append(labels[tr_idx])
                for ts_idx in test_index:
                    testlabels.append(labels[ts_idx])

            #nbvectdata = []
            #nbpoplabels= []
            nbtraindata = []
            nbtrainlabels =[]
            nbtestdata = []
            nbtestlabels = []

            # for nbd, nbdatum in enumerate(vectdata):
            #     if nblabels[nbd] != "na":
            #         nbpoplabels.append(nblabels[nbd])
            #         nbvectdata.append(nbdatum)

            nbsssidxs = StratifiedShuffleSplit(nblabels, n_iter=1, test_size=0.7, random_state=0)
            for train_index, test_index in nbsssidxs:
                #print("TRAIN:", train_index, "TEST:", test_index)
                nbtraindata, nbtestdata = nbvectdata[train_index], nbvectdata[test_index]
                #nbtrainlabels, nbtestlabels = nblabels[train_index], nblabels[test_index]
                for tr_idx in train_index:
                    #nbtraindata.append(nbvectdata[tr_idx])
                    nbtrainlabels.append(nblabels[tr_idx])
                for ts_idx in test_index:
                    #nbtestdata.append(nbvectdata[ts_idx])
                    nbtestlabels.append(nblabels[ts_idx])


            ftraindata = []
            ftrainlabels =[]
            ftestdata = []
            ftestlabels = []

            # for nbd, nbdatum in enumerate(vectdata):
            #     if nblabels[nbd] != "na":
            #         nbpoplabels.append(nblabels[nbd])
            #         nbvectdata.append(nbdatum)

            fsssidxs = StratifiedShuffleSplit(flabels, n_iter=1, test_size=0.7, random_state=0)
            for train_index, test_index in fsssidxs:
                #print("TRAIN:", train_index, "TEST:", test_index)
                ftraindata, ftestdata = fvectdata[train_index], fvectdata[test_index]
                #nbtrainlabels, nbtestlabels = nblabels[train_index], nblabels[test_index]
                for tr_idx in train_index:
                    #nbtraindata.append(nbvectdata[tr_idx])
                    ftrainlabels.append(flabels[tr_idx])
                for ts_idx in test_index:
                    #nbtestdata.append(nbvectdata[ts_idx])
                    ftestlabels.append(flabels[ts_idx])





            # vectpca = PCA(n_components=4)
            # vectpca.fit(vectdata)

            # pcacorr = []
            # for var in vectdata:
            #     for comp in vectpca.components_:
            #         corr = pearsonr(var, comp)
            #         #print corr
            #         pcacorr.append(corr)


             # vectlabels = dv.fit_transform(labels)

            ##jj
            # print "LDA"
            # vectlda = LinearDiscriminantAnalysis(n_components=10)
            # ldacomps = vectlda.fit(traindata, trainlabels).transform(traindata)
            # print "==========================="
            # print maxfeats
            #


            #
            # for jdx, coef in enumerate(vectlda.coef_):
            #     print vectlda.classes_[jdx]
            #     for idx,(k,v) in enumerate(sorted(dv.vocabulary_.items(),key=itemgetter(1))):
            #         print k, coef[idx]
            #     print "==============="

            ##jj
            # ldaacc = vectlda.score(testdata,testlabels)
            # print "ldaacc ", ldaacc

            # ldacorr = []
            # for var in vectdata:
            #     for comp in ldacomps:
            #         corr = pearsonr(var, comp)
            #         #print corr
            #         ldacorr.append(corr)

             # vectlabels = dv.fit_transform(labels)

            # #jj
            # print "QDA"
            # vectqda = QuadraticDiscriminantAnalysis()
            # qdacomps = vectqda.fit(traindata, trainlabels)#.transform(vectdata)
            # print "==========================="
            # print maxfeats
            # qdaacc = vectqda.score(testdata, testlabels)
            # print "qdaacc ", qdaacc

            # for jdx, coef in enumerate(vectqda.coef_):
            #     print vectqda.classes_[jdx]
            #     for idx,(k,v) in enumerate(sorted(dv.vocabulary_.items(),key=itemgetter(1))):
            #         print k, coef[idx]
            #     print "==============="
            # ldacorr = []
            # for var in vectdata:
            #     for comp in ldacomps:
            #         corr = pearsonr(var, comp)
            #         #print corr
            #         ldacorr.append(corr)

            # rcf = RandomForestClassifier(n_estimators=200, warm_start=True,oob_score=True)
            # rcfcomps = rcf.fit(traindata,trainlabels).transform(traindata)
            #rcfacc = rcf
            #print "rcfacc ", rcfacc

            # #jj
            # adb = AdaBoostClassifier(n_estimators=200)
            # adcomps = adb.fit(traindata, trainlabels)#.transform(traindata)
            # adbacc = adb.score(testdata, testlabels)
            # print "adbacc ", adbacc
            # print adb.feature_importances_

            # gdb = GradientBoostingClassifier(n_estimators=200)
            # gdcomps = gdb.fit(traindata,trainlabels)#.transform(traindata)
            # gdbacc = gdb.score(testdata,testlabels)
            # print "gdbacc ", gdbacc
            # print gdb.feature_importances_


            ovs = OneVsRestClassifier(RandomForestClassifier(n_estimators=200, warm_start=True, oob_score=True))
            ovcomps = ovs.fit(traindata, trainlabels)
            ovsacc = ovs.score(testdata, testlabels)
            print "ovsacc ", ovsacc
            ovsestimators = ovs.estimators_
            ovsfeatimps = []
            for i,ovsest in enumerate(ovsestimators):
                print ovs.classes_[i], ovsest.feature_importances_
                ovsfeatimps = ovsest.feature_importances_
            #print len(dv.feature_names_)
            #print dv.feature_names_
            #print dv.vocabulary_[' $100000 to $124999']

            ovsfimps =  sorted(zip(dv.feature_names_,ovsfeatimps),key=itemgetter(1),reverse=True)[:k]
            #print sum(ovsfimps[:][2])
            print ovsfimps


            # #jj
            # ovs2 = OneVsRestClassifier(AdaBoostClassifier(n_estimators=200))
            # ovcomps2 = ovs2.fit(traindata, trainlabels)
            # ovsacc2 = ovs2.score(testdata, testlabels)
            # print "ovsacc2 ", ovsacc2
            #
            # ovo = OneVsOneClassifier(RandomForestClassifier(n_estimators=200, warm_start=True, oob_score=True))
            # ovocomps = ovo.fit(traindata, trainlabels)
            # ovoacc = ovo.score(testdata, testlabels)
            # print "ovoacc ", ovoacc
            #
            #
            # ovo2 = OneVsOneClassifier(AdaBoostClassifier(n_estimators=200))
            # ovocomps2 = ovo2.fit(traindata, trainlabels)
            # ovoacc2 = ovo2.score(testdata, testlabels)
            # print "ovoacc2 ", ovoacc2
            # #print ovs.coef_
            #
            # ovosvm  = OneVsOneClassifier(NuSVC(nu=0.1,kernel='poly',random_state=0))
            # ovosvm.fit(traindata, trainlabels)
            # ovosvmacc = ovosvm.score(testdata, testlabels)
            # print "ovosvmacc ", ovosvmacc


            # clf = NuSVR(kernel = 'rbf',C=1.0, nu=0.5)
            # clf.fit(traindata, trainlabels)
            # nusvacc = clf.score(testdata, testlabels)
            # print "nusvacc ", nusvacc


            print "===========================NB================================="


            # #jj
            # nbadb = AdaBoostClassifier(n_estimators=200)
            # nbadcomps = nbadb.fit(nbtraindata, nbtrainlabels)#.transform(traindata)
            # nbadbacc = nbadb.score(nbtestdata, nbtestlabels)
            # print "nbadbacc ", nbadbacc
            # print nbadb.feature_importances_

            # gdb = GradientBoostingClassifier(n_estimators=200)
            # gdcomps = gdb.fit(traindata,trainlabels)#.transform(traindata)
            # gdbacc = gdb.score(testdata,testlabels)
            # print "gdbacc ", gdbacc
            # print gdb.feature_importances_


            nbovs = OneVsRestClassifier(RandomForestClassifier(n_estimators=200, warm_start=True, oob_score=True))
            nbovcomps = nbovs.fit(nbtraindata, nbtrainlabels)
            nbovsacc = nbovs.score(nbtestdata, nbtestlabels)
            print "nbovsacc ", nbovsacc
            nbovsestimators = nbovs.estimators_
            nbovsfeatimps = []
            for i,nbovsest in enumerate(nbovsestimators):
                print nbovs.classes_[i], nbovsest.feature_importances_
                nbovsfeatimps = nbovsest.feature_importances_
            nbovsfimps =  sorted(zip(nbdv.feature_names_,nbovsfeatimps),key=itemgetter(1),reverse=True)[:k]
            print nbovsfimps


            # #jj
            # nbovs2 = OneVsRestClassifier(AdaBoostClassifier(n_estimators=200))
            # nbovcomps2 = nbovs2.fit(nbtraindata, nbtrainlabels)
            # nbovsacc2 = nbovs2.score(nbtestdata, nbtestlabels)
            # print "nbovsacc2 ", nbovsacc2
            #
            # nbovo = OneVsOneClassifier(RandomForestClassifier(n_estimators=200, warm_start=True, oob_score=True))
            # nbovocomps = nbovo.fit(nbtraindata, nbtrainlabels)
            # nbovoacc = nbovo.score(nbtestdata, nbtestlabels)
            # print "nbovoacc ", nbovoacc
            #
            # nbovo2 = OneVsOneClassifier(AdaBoostClassifier(n_estimators=200))
            # nbovocomps2 = nbovo2.fit(nbtraindata, nbtrainlabels)
            # nbovoacc2 = nbovo2.score(nbtestdata, nbtestlabels)
            # print "nbovoacc2 ", nbovoacc2
            # #print ovs.coef_
            #
            # nbovosvm  = OneVsOneClassifier(LinearSVC(random_state=0))
            # nbovosvm.fit(nbtraindata, nbtrainlabels)
            # nbovosvmacc = nbovosvm.score(nbtestdata, nbtestlabels)
            # print "nbovosvmacc ", nbovosvmacc

            print "===========================f================================="

            # #jj
            # fadb = AdaBoostClassifier(n_estimators=200)
            # fadcomps = fadb.fit(ftraindata, ftrainlabels)#.transform(traindata)
            # fadbacc = fadb.score(ftestdata, ftestlabels)
            # print "fadbacc ", fadbacc
            # print fadb.feature_importances_

            # gdb = GradientBoostingClassifier(n_estimators=200)
            # gdcomps = gdb.fit(traindata,trainlabels)#.transform(traindata)
            # gdbacc = gdb.score(testdata,testlabels)
            # print "gdbacc ", gdbacc
            # print gdb.feature_importances_


            fovs = OneVsRestClassifier(RandomForestClassifier(n_estimators=200, warm_start=True, oob_score=True))
            fovcomps = fovs.fit(ftraindata, ftrainlabels)
            fovsacc = fovs.score(ftestdata, ftestlabels)
            print "fovsacc ", fovsacc
            fovsestimators = fovs.estimators_
            fovsfeatimps = []
            for i,fovsest in enumerate(fovsestimators):
                print fovs.classes_[i], fovsest.feature_importances_
                fovsfeatimps = fovsest.feature_importances_
            fovsfimps =  sorted(zip(fdv.feature_names_,fovsfeatimps),key=itemgetter(1),reverse=True)[:k]
            print fovsfimps


            return ovsfimps, nbovsfimps, fovsfimps

            # #jj
            # fovs2 = OneVsRestClassifier(AdaBoostClassifier(n_estimators=200))
            # fovcomps2 = fovs2.fit(ftraindata, ftrainlabels)
            # fovsacc2 = fovs2.score(ftestdata, ftestlabels)
            # print "fovsacc2 ", fovsacc2
            #
            # fovo = OneVsOneClassifier(RandomForestClassifier(n_estimators=200, warm_start=True, oob_score=True))
            # fovocomps = fovo.fit(ftraindata, ftrainlabels)
            # fovoacc = fovo.score(ftestdata, ftestlabels)
            # print "fovoacc ", fovoacc
            #
            # fovo2 = OneVsOneClassifier(AdaBoostClassifier(n_estimators=200))
            # fovocomps2 = fovo2.fit(ftraindata, ftrainlabels)
            # fovoacc2 = fovo2.score(ftestdata, ftestlabels)
            # print "fovoacc2 ", fovoacc2
            # #print ovs.coef_
            #
            # fovosvm  = OneVsOneClassifier(NuSVC(nu=0.435,kernel='poly',random_state=0))
            # fovosvm.fit(ftraindata, ftrainlabels)
            # fovosvmacc = fovosvm.score(ftestdata, ftestlabels)
            # print "fovosvmacc ", fovosvmacc

#filename = 'DataVizProject\sample.txt'
filename = 'DataVizProject\yelp_business_id_block_id_lat_long_state.txt'
city = 'phoenix'
state = 'az'
category = 'restaurants'

#formatyelpjson(filename) # call only once!!
#getyelpjsonbyparams(filename,city,state,category)
#getyelpincomejson(city,state,category)
imps = []
nbimps, gimps, aavimps = doAnalysis(city, state, category,10)






