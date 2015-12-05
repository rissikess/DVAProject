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
import pickle
from sklearn.externals import joblib
from scipy.sparse import csr_matrix
from numpy import savetxt, loadtxt, append, zeros
import numpy as np
from collections import Counter

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier
from sklearn.cross_validation import train_test_split, StratifiedShuffleSplit
#import mlpy
#from mlpy import KFDA
#import set

from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_selection import RFECV, RFE
from sklearn.preprocessing import Imputer




from django.conf import settings as djangoSettings


def inplace_change(filename, old_string, new_string):
    s=open(filename).read()
    if old_string in s:
            #print( 'Changing "{old_string}" to "{new_string}"'.format(**locals()))
            s=s.replace(old_string, new_string)
            f=open(filename, 'w')
            f.write(s)
            f.flush()
            f.close()
    else:
            pass
            #print( 'No occurances of "{old_string}" found.'.format(**locals()))

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
        #print ("totcount = ", totcount, " ", city, " count = ", citycount, " ",category," count = ", catcount)


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
    #print (invid)
    #print (errcount)
    #with open('maricopaincome\yelpincome.json','w') as wrincfile:
    #    wrincfile.write(json.dumps(newcatdata))


def evalFilter(datum, filterConditions):
    try:
      for filter in filterConditions:
          filtval = filterConditions[filter]

          if isinstance(filtval, int) or isinstance(filtval, int) or isinstance(filtval, float)\
                  or isinstance(filtval, str) or isinstance(filtval, bool):
              if datum[filter] != filtval:
                  return True
          if isinstance(filtval, list):
              filterCon = True
              for fval in filtval:
                  if fval in datum[filter]:
                      filterCon = False
                      break
              if filterCon:
                  return True
          if isinstance(filtval, dict):
              for fkey in filtval:
                  if isinstance(filtval[fkey], int) or isinstance(filtval[fkey], int) or isinstance(filtval[fkey], float)\
                  or isinstance(filtval[fkey], str) or isinstance(filtval[fkey], bool):
                      if datum[filter][fkey] != filtval[fkey]:
                          return True
                  if isinstance(filtval[fkey], dict):
                      for fsubkey in filtval[fkey]:
                          if isinstance(filtval[fkey][fsubkey], int) or isinstance(filtval[fkey][fsubkey], int) or isinstance(filtval[fkey][fsubkey], float)\
                          or isinstance(filtval[fkey][fsubkey], str) or isinstance(filtval[fkey][fsubkey], bool):
                              if datum[filter][fkey][fsubkey] != filtval[fkey][fsubkey]:
                                  return True
                  if isinstance(filtval[fkey], list):
                      filterCon = True
                      for fsubval in filtval[fkey]:
                          if fsubval in datum[filter][fkey]:
                              filterCon = False
                              break
                          if filterCon:
                              return True
    except KeyError as e:
      print(e)
      return True                

    return False






def doAnalysis(city, state, category, filterConditions, k=10):
    try:
      with open(djangoSettings.STATIC_ROOT + "/" +city + category + 'income.json','r') as r_file:
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
              filtercondition = True
              for dno,datum in enumerate(data):
                 #  #filter
                 # if 'Chinese' not in datum['categories'] and 'Pizza' not in datum['categories'] and 'Italian' not in datum['categories']:
                 #     continue
                 # if 'Wi-Fi' in datum['attributes'] and datum['attributes']['Wi-Fi'] == 'no':
                 #     continue
                 # #if 'Ambience' in datum['attributes'] and 'casual' in datum['Ambience'] and datum['Ambience']['casual'] == False:
                 # #    continue
                 # if 'Price Range' in datum['attributes'] and datum['attributes']['Price Range'] != 2:
                 #     continue
                 #if datum["stars"]>=3.0:
                 if evalFilter(datum, filterConditions):
                     continue
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
                     elif key!="name" and key!="business_id" and key!="full_address" and key!="latitude" and key!="longitude" and key!="hours" and key[0]!=" " and key[0]!="$" and key!='review_count' and key!='categories':
                         if isinstance(datum[key], int) or isinstance(datum[key], int) or isinstance(datum[key], float) \
                                 or isinstance(datum[key], str) or isinstance(datum[key], bool):
                             newdatum[key] = datum[key]
                             keyset.add(key)
                             featcnt+=1
                         elif isinstance(datum[key],dict):
                             for subkey in datum[key]:
                                 if isinstance(datum[key][subkey], int) or isinstance(datum[key][subkey], int) or \
                                         isinstance(datum[key][subkey], float) or isinstance(datum[key][subkey], str) or \
                                         isinstance(datum[key][subkey], bool):
                                     newdatum[key+" "+subkey] = datum[key][subkey]
                                     keyset.add(subkey)
                                     featcnt+=1
                                 elif isinstance(datum[key][subkey], str):
                                     ascval = unicodedata.normalize('NFKD', datum[key][subkey]).encode('ascii','ignore')
                                     newdatum[key+" "+subkey] = ascval
                                     keyset.add(subkey)
                                     featcnt+=1
                                 elif isinstance(datum[key][subkey],dict):
                                     for subsubkey in datum[key][subkey]:
                                         if isinstance(datum[key][subkey][subsubkey], int) or \
                                                 isinstance(datum[key][subkey][subsubkey], int) or \
                                                 isinstance(datum[key][subkey][subsubkey], float) or \
                                                 isinstance(datum[key][subkey][subsubkey], str) or \
                                                 isinstance(datum[key][subkey][subsubkey], bool):
                                             newdatum[key+" "+subkey+" "+subsubkey] = datum[key][subkey][subsubkey]
                                             keyset.add(subsubkey)
                                             featcnt+=1
                                         elif isinstance(datum[key][subkey][subsubkey], str):
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
                                 if isinstance(item, int) or isinstance(item, int) or isinstance(item, float) or \
                                         isinstance(item, str) or isinstance(item, bool):
                                     newdatum[key +" "+str(item)] = True
                                     keyset.add(key)
                                     featcnt+=1
                                 elif isinstance(item, str):
                                     ascval = unicodedata.normalize('NFKD', item).encode('ascii','ignore')
                                     newdatum[key +" "+ascval] = True
                                     keyset.add(key)
                                     featcnt+=1
                                 else:
                                     unkeyset.add(key)
                                     unkvalueset.add(type(item))
                         else:
                              if isinstance(datum[key], str):
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
              #print (unkeyset)
              #print (unkvalueset)
              # for unk in unkeyset:
              #     if isinstance(unk, unicode):
              #         print "yeah"
              #     else:
              #         print "nah"
              dv = DictVectorizer(sparse=False)
              vectdata = dv.fit_transform(newdata)
              #print vectdata[0]
              joblib.dump(dv, 'dv.pkl')
              savetxt('vectdata.txt',vectdata)


              nbdv = DictVectorizer(sparse=False)
              nbvectdata = nbdv.fit_transform(nbnewdata)
              #print nbvectdata[0]
              joblib.dump(nbdv, 'nbdv.pkl')
              savetxt('nbvectdata.txt',nbvectdata)

              fdv = DictVectorizer(sparse=False)
              fvectdata = fdv.fit_transform(fnewdata)
              #print nbvectdata[0]
              joblib.dump(fdv, 'fdv.pkl')
              savetxt('fvectdata.txt',fvectdata)


              #print (len(flabels), len(fnewdata), len(fvectdata))
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

              # #jj
              # print "LDA"
              # vectlda = LinearDiscriminantAnalysis(n_components=10)
              # ldacomps = vectlda.fit(traindata, trainlabels).transform(traindata)
              # print "==========================="
              # print maxfeats
              # #end jj



              #
              # for jdx, coef in enumerate(vectlda.coef_):
              #     print vectlda.classes_[jdx]
              #     for idx,(k,v) in enumerate(sorted(dv.vocabulary_.items(),key=itemgetter(1))):
              #         print k, coef[idx]
              #     print "==============="

              # #jj
              # ldaacc = vectlda.score(testdata,testlabels)
              # print "ldaacc ", ldaacc
              # #end jj

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
              # #end jj

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
              #
              # gdb = GradientBoostingClassifier(n_estimators=200)
              # gdcomps = gdb.fit(traindata,trainlabels)#.transform(traindata)
              # gdbacc = gdb.score(testdata,testlabels)
              # print "gdbacc ", gdbacc
              # print gdb.feature_importances_
              # #end jj


              ovs = OneVsRestClassifier(RandomForestClassifier(n_estimators=200, warm_start=True, oob_score=True))

              ovcomps = ovs.fit(traindata, trainlabels)
              ovsacc = ovs.score(testdata, testlabels)
              #print "ovsacc ", ovsacc
              ovsestimators = ovs.estimators_
              ovsfeatimps = []
              for i,ovsest in enumerate(ovsestimators):
                  #print ovs.classes_[i], ovsest.feature_importances_
                  ovsfeatimps = ovsest.feature_importances_
              #print len(dv.feature_names_)
              #print dv.feature_names_
              #print dv.vocabulary_[' $100000 to $124999']


              ovsfimps =  sorted(zip(dv.feature_names_,ovsfeatimps),key=itemgetter(1),reverse=True)[:k]
              #print sum(ovsfimps[:][2])
              #print (ovsfimps)


              # rfecv = RFECV(estimator=rfc, step=100, cv=StratifiedKFold(trainlabels, 2),
              #   scoring='accuracy')
              # rfecv.fit(traindata, trainlabels)
              #
              # print("Optimal number of features : %d" % rfecv.n_features_)
              #
              # # Plot number of features VS. cross-validation scores
              # plt.figure()
              # plt.xlabel("Number of features selected")
              # plt.ylabel("Cross validation score (nb of correct classifications)")
              # plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
              # plt.show()
              # print rfecv.ranking_
              rfc = RandomForestClassifier(n_estimators=200, warm_start=True, oob_score=True)
              rfe = RFE(estimator=rfc, n_features_to_select=k,step = 0.1)
              rfe.fit(traindata, trainlabels)
              #print rfe.n_features_
              #print len(rfe.ranking_)
              rfetestdata = [[each_list[i] for i, supp in enumerate(rfe.support_) if supp == True ] for each_list in testdata]
              #print "rfeacc ", rfe.estimator_.score(rfetestdata, testlabels)
              # plt.figure()
              # plt.xlabel("Number of features selected")
              # plt.ylabel("Cross validation score (nb of correct classifications)")
              # plt.plot(range(1, len(rfe.scores_) + 1), rfe.scores_)
              # plt.show()
              rfefeatimps = []
              rfefeatnames = [dv.feature_names_[i].replace("attributes ", "attributes_") for i, supp in enumerate(rfe.support_) if supp == True ]
              impsums = sum(rfe.estimator_.feature_importances_)
              rfeimps =  sorted(zip(rfefeatnames,rfe.estimator_.feature_importances_/impsums),key=itemgetter(1),reverse=True)
              #print (rfeimps)
              #print (sum([pair[1] for pair in rfeimps]))
              joblib.dump(ovs, 'rfc.pkl')



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
              # #end jj


              # clf = NuSVR(kernel = 'rbf',C=1.0, nu=0.5)
              # clf.fit(traindata, trainlabels)
              # nusvacc = clf.score(testdata, testlabels)
              # print "nusvacc ", nusvacc


              #print "===========================NB================================="


              # #jj
              # nbadb = AdaBoostClassifier(n_estimators=200)
              # nbadcomps = nbadb.fit(nbtraindata, nbtrainlabels)#.transform(traindata)
              # nbadbacc = nbadb.score(nbtestdata, nbtestlabels)
              # print "nbadbacc ", nbadbacc
              # print nbadb.feature_importances_
              #
              # gdb = GradientBoostingClassifier(n_estimators=200)
              # gdcomps = gdb.fit(nbtraindata,nbtrainlabels)#.transform(traindata)
              # gdbacc = gdb.score(nbtestdata,nbtestlabels)
              # print "gdbacc ", gdbacc
              # print gdb.feature_importances_
              # #end jj

              nbovs = OneVsRestClassifier(RandomForestClassifier(n_estimators=200, warm_start=True, oob_score=True))
              nbovcomps = nbovs.fit(nbtraindata, nbtrainlabels)
              nbovsacc = nbovs.score(nbtestdata, nbtestlabels)
              #print "nbovsacc ", nbovsacc
              nbovsestimators = nbovs.estimators_
              nbovsfeatimps = []
              for i,nbovsest in enumerate(nbovsestimators):
                 # print nbovs.classes_[i], nbovsest.feature_importances_
                  nbovsfeatimps = nbovsest.feature_importances_
              nbovsfimps =  sorted(zip(nbdv.feature_names_,nbovsfeatimps),key=itemgetter(1),reverse=True)[:k]
              #print nbovsfimps

              nbrfc = RandomForestClassifier(n_estimators=200, warm_start=True, oob_score=True)
              nbrfe = RFE(estimator=nbrfc, n_features_to_select=k,step = 0.1)
              nbrfe.fit(nbtraindata, nbtrainlabels)
              #print nbrfe.n_features_
              #print len(nbrfe.ranking_)
              nbrfetestdata = [[each_list[i] for i, supp in enumerate(nbrfe.support_) if supp == True ] for each_list in nbtestdata]
              #print "nbrfeacc ", nbrfe.estimator_.score(nbrfetestdata, nbtestlabels)

              nbrfefeatnames = [dv.feature_names_[i].replace("attributes ", "attributes_") for i, supp in enumerate(nbrfe.support_) if supp == True ]
              nbimpsums = sum(nbrfe.estimator_.feature_importances_)
              nbrfeimps =  sorted(zip(nbrfefeatnames,nbrfe.estimator_.feature_importances_/nbimpsums),key=itemgetter(1),reverse=True)
              #print nbrfeimps
              #print sum([pair[1] for pair in nbrfeimps])
              joblib.dump(nbovs, 'nbrfc.pkl')

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
              # #end jj

              #print "===========================f================================="

              # #jj
              # fadb = AdaBoostClassifier(n_estimators=200)
              # fadcomps = fadb.fit(ftraindata, ftrainlabels)#.transform(traindata)
              # fadbacc = fadb.score(ftestdata, ftestlabels)
              # print "fadbacc ", fadbacc
              # print fadb.feature_importances_
              #
              # gdb = GradientBoostingClassifier(n_estimators=200)
              # gdcomps = gdb.fit(ftraindata,ftrainlabels)#.transform(traindata)
              # gdbacc = gdb.score(ftestdata,ftestlabels)
              # print "gdbacc ", gdbacc
              # print gdb.feature_importances_
              # #end jj

              fovs = OneVsRestClassifier(RandomForestClassifier(n_estimators=200, warm_start=True, oob_score=True))
              fovcomps = fovs.fit(ftraindata, ftrainlabels)
              fovsacc = fovs.score(ftestdata, ftestlabels)
              #print "fovsacc ", fovsacc
              fovsestimators = fovs.estimators_
              fovsfeatimps = []
              for i,fovsest in enumerate(fovsestimators):
                  #print fovs.classes_[i], fovsest.feature_importances_
                  fovsfeatimps = fovsest.feature_importances_
              fovsfimps = sorted(zip(fdv.feature_names_,fovsfeatimps),key=itemgetter(1),reverse=True)[:k]
              #print fovsfimps

              owfile = 'output.json'
              with open(owfile,'w') as owrfile:
                  owrfile.write(json.dumps([dict(ovsfimps), dict(nbovsfimps), dict(fovsfimps)]))


              frfc = RandomForestClassifier(n_estimators=200, warm_start=True, oob_score=True)
              frfe = RFE(estimator=frfc, n_features_to_select=k,step = 0.1)
              frfe.fit(ftraindata, ftrainlabels)
              #print frfe.n_features_
              #print len(frfe.ranking_)
              frfetestdata = [[each_list[i] for i, supp in enumerate(frfe.support_) if supp == True ] for each_list in ftestdata]
              #print "frfeacc ", frfe.estimator_.score(frfetestdata, ftestlabels)

              frfefeatnames = [dv.feature_names_[i].replace("attributes ", "attributes_") for i, supp in enumerate(frfe.support_) if supp == True ]
              fimpsums = sum(frfe.estimator_.feature_importances_)
              frfeimps =  sorted(zip(frfefeatnames,frfe.estimator_.feature_importances_/fimpsums),key=itemgetter(1),reverse=True)
              #print frfeimps
              #print sum([pair[1] for pair in frfeimps])
              joblib.dump(fovs, 'frfc.pkl')

              #

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
              # #end jj

              #return ovsfimps, nbovsfimps, fovsfimps
              return rfeimps, nbrfeimps, frfeimps
    except Exception as e:
      return [],[],[]



def predictRating(factorDict):
    dv = joblib.load('dv.pkl')
    densevect = dv.transform(factorDict)
    sparsevect = csr_matrix(densevect)
    # imp = Imputer(missing_values=0.0, strategy='most_frequent', axis=0)
    # vectdata = loadtxt('vectdata.txt')
    # oldlen = len(vectdata[0])
    # impvect = imp.fit(vectdata)
    # tvect = impvect.transform(sparsevect)
    # newlen = len(tvect[0])
    # if newlen < oldlen:
    #     z = zeros((1,oldlen-newlen))
    #     testvect = append(tvect,z, axis=1)
    # else:
    #     testvect = tvect
    ovs = joblib.load('rfc.pkl')
    # result = ovs.predict(testvect)
    result = ovs.predict(densevect)
    return result


#filename = 'DataVizProject\sample.txt'
#filename = 'DataVizProject\yelp_business_id_block_id_lat_long_state.txt'
#city = 'phoenix'
#state = 'az'
#category = 'restaurants'

#formatyelpjson(filename) # call only once!!
#getyelpjsonbyparams(filename,city,state,category)
#getyelpincomejson(city,state,category)
#imps = []
#filterConditions = {}
#run experiments for different values of k
#nbimps, gimps, aavimps = doAnalysis(city, state, category, filterConditions, 20)
#print nbimps, gimps, aavimps






