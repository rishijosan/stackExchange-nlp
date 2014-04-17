'''
Created on Apr 16, 2014

@author: root
'''

import random 
import cPickle as pickle
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,stop_words='english')


with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tagsDesc.pk', 'rb') as inp:
    tagsDesc = pickle.load(inp)


#===============================================================================
# categories = [
#        'alt.atheism',
#        'talk.religion.misc',
#        'comp.graphics',
#        'sci.space',
#    ]
# 
# remove = ('headers', 'footers', 'quotes')
# 
# data_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42,remove=remove)
# 
# data_test = fetch_20newsgroups(subset='test', categories=categories, shuffle=True, random_state=42, remove=remove)
# 
# 
# X_train = vectorizer.transform(data_train.data)
# names = vectorizer.get_feature_names()
#===============================================================================


newSet = set()

for x in range(10):
    newSet.add(x)


otherSet = set()

for x in range(5):
    otherSet.add(x)

newDict = dict()


for i in range(20):
    newDict[i] = i
    
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags2Posts.pk', 'rb') as inp:
    tags2Posts = pickle.load(inp)
