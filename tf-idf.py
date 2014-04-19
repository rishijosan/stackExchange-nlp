'''
Created on Apr 11, 2014

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


with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/posList.pk', 'rb') as inp:
    posList = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/negList.pk', 'rb') as inp:
    negList = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'rb') as inp:
    idToPost = pickle.load(inp)

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tagsDesc.pk', 'rb') as inp:
    tagsDesc = pickle.load(inp)
   
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags2Posts.pk', 'rb') as inp:
    tags2Posts = pickle.load(inp)
       
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'rb') as inp:
    idToPost = pickle.load(inp)
 
#Create Vector of Posts
subList = list()

for item in posList[0]:
    subList.append(idToPost[item][1])
    
for item in negList[0]:
    subList.append(idToPost[item][1])
    
#Create Label Vector
labels = list()
for i in range(60):
    labels.append(1)
for i in range(1500):
    labels.append(0)  

 
#Convert lists to numpy arrays
docsNP = np.array(subList)
labelsNP = np.array(labels)


#Create numPY matrix with features

#tfifdVector = countVec.fit_transform(subList)
tfifdVector = vectorizer.fit_transform(subList)

docClassifier = svm.LinearSVC()
docClassifier.fit(tfifdVector, labelsNP) 



#######################Testing################################

testList = list()

for id in tags2Posts[tagsDesc[0][0]]:
    testList.append(idToPost[id][1])
    
testListNP = np.array(testList)


#tfifdVectorTest = countVec.transform(testList[1000:2000])
tfifdVectorTest = vectorizer.transform(testList[1000:2000])

#tfifdVectorTest = vectorizer.transform(subList)
print 'Vectorized!'
results = np.array(docClassifier.predict(tfifdVectorTest)).tolist()


















#Column vector of posts
#docsNP[:,0]

#===============================================================================
# with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tagsDesc.pk', 'rb') as inp:
#    tagsDesc = pickle.load(inp)
#    
# with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags2Posts.pk', 'rb') as inp:
#    tags2Posts = pickle.load(inp)
#    
# with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'rb') as inp:
#    idToPost = pickle.load(inp)
#===============================================================================

#===============================================================================
# idToPost[tags2Posts['linux'][0]]
# 
# sublist = list()
# 
# #Create List with posts from top 4 tags. Add Post and tag to list
# for i in range(100):
#    for post in tags2Posts[tagsDesc[i][0]]:
#        item = list()
#        item.append(idToPost[post][1]) # Body of Post
#        item.append(tagsDesc[i][0])
#        sublist.append(item)
#===============================================================================