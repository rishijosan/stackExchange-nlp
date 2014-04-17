'''
Created on Apr 17, 2014

@author: Rishi Josan
'''

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import cPickle as pickle
import numpy as np
import nltk
from nltk.corpus import PlaintextCorpusReader
from sklearn import svm

#transformer = TfidfTransformer()
vectorizer = TfidfVectorizer()
countVec = CountVectorizer(stop_words='english')


    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'rb') as inp:
    idToPost = pickle.load(inp)

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tagsDesc.pk', 'rb') as inp:
    tagsDesc = pickle.load(inp)
   
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags2Posts.pk', 'rb') as inp:
    tags2Posts = pickle.load(inp)
       
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'rb') as inp:
    idToPost = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/posList10k.pk', 'rb') as inp:
    posList = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/negList10k.pk', 'rb') as inp:
    negList = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/testSet.pk', 'rb') as inp:
    testSet = pickle.load(inp)
 
 
 
  
#Create Vector of Posts
subList = list()
#Create Vector of Labels
labels = list()

for item in posList[0]:
    subList.append(idToPost[item][1])
    labels.append(1)
    
for item in negList[0]:
    subList.append(idToPost[item][1])
    labels.append(1)
    
    
