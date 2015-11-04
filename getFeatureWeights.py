__author__ = 'Rishikesh'

from numpy import random

#List of features from the Yelp + Census datasets
features = ['Drive-Thru', 'Alcohol', 'Open 24 Hours', 'Noise Level', 'Thursday', 'Sunday', 'Has TV', 'Attire',
            'Ambience', 'Payment Types', 'open', ' $75000 to $99999', 'Price Range', ' $200000 or more', 'city',
            'review_count', 'Caters', ' $150000 to $199999', 'Good for Kids', 'Friday', '$10000 to $24999',
            'Delivery', 'Dogs Allowed', 'state', ' $100000 to $124999', 'Smoking', 'Accepts Credit Cards', 'type',
            'BYOB/Corkage', 'Take-out', 'Ages Allowed', 'block_id', 'Good For Dancing', 'BYOB', 'Coat Check',
            'Wednesday', ' Less than $10000', 'Happy Hour','Monday', 'Wheelchair Accessible', 'Corkage',
            'Outdoor Seating', 'Takes Reservations', '$25000 to $49999', ' $125000 to $149999', 'Wi-Fi', 'categories',
            'Dietary Restrictions', 'name', 'neighborhoods', 'Tuesday', 'Saturday', 'By Appointment Only',
            'Waiter Service', 'Order at Counter', 'Good For', 'Parking', '$50000 to $74999', 'Music', 'Good For Kids',
            'Good For Groups']



#getTopFeatureWeights returns the top k features contributing to ratings on Yelp and their weights(contribution) filtered
# by a set of criteria.
def getTopFeatureWeights(filterdict,k):
    #featset = set(features)
    filtlist = list(set(features).difference(set(filterdict.keys())))
    rind = random.randint(0,len(filtlist)-k-1)
    weights = random.rand(k)
    wsum = sum(weights)
    if k < len(filtlist):
        weights = weights * 0.9 / wsum
    else:
        weights = weights / wsum
    #print zip(filtlist[rind:rind+k],weights)
    return zip(filtlist[rind:rind+k],weights)


#Usage: Build a dictionary of filter criteria. For example if you want all restaurants that are of 'category' mexican and
# 'Price Range' 2.0 and 'neighborhood' of downtown, create a dict by using  keys ('category', 'Price Range', 'neighborhood' etc.)
# from the featurelist defined at the top of this file and set them to the desired filter condition values.
# Choose k and pass both the dict and value of k, to get the top k features with their weights for the filter conditions defined by
# the dict. Example below:

fdict = dict()

# Filter conditions
fdict['Caters'] = True
fdict['Noise Level'] = 'Low'
fdict['categories'] = ['Mexican','Foodtruck']
fdict['Price Range'] = 3.0
fdict['Payment Types'] = ['Credit', 'Debit']
fdict['Open 24 Hours'] = True
fdict[' $75000 to $99999'] = 20
fdict['Alcohol'] = 'No'

# get Top 6 features
x = getTopFeatureWeights(fdict, k=6)
print x