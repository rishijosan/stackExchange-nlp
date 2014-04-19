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
from collections import OrderedDict
from  nltk.probability import FreqDist
from nltk.corpus import stopwords


useSantized = True


#transformer = TfidfTransformer()
vectorizer = TfidfVectorizer()
#countVec = CountVectorizer(stop_words='english')
countVec = CountVectorizer()



    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'rb') as inp:
    idToPost = pickle.load(inp)

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tagsDesc.pk', 'rb') as inp:
    tagsDesc = pickle.load(inp)
   
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags2Posts.pk', 'rb') as inp:
    tags2Posts = pickle.load(inp)
       
if useSantized:
    #Using Sanitized Posts now
    with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPostSan.pk', 'rb') as inp:
        idToPost = pickle.load(inp)  
else:
    with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'rb') as inp:
        idToPost = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/posListTop100.pk', 'rb') as inp:
    posList = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/negListTop100.pk', 'rb') as inp:
    negList = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/testSetTop100.pk', 'rb') as inp:
    testSet = pickle.load(inp)
 

key = 20
  
#Create Vector of Posts
trainList1 = list()
testList1 = list()
#Create Vector of Labels
labels1 = list()

for item in posList[key]:
    
    if useSantized:
        trainList1.append(" ".join(idToPost[item][1]))
    else:
        trainList1.append(idToPost[item][1])
        
    labels1.append(1)
    
for item in negList[key]:
    
    if useSantized:
        trainList1.append(" ".join(idToPost[item][1]))
    else:
        trainList1.append(idToPost[item][1])
        
    labels1.append(0)
    
for item in testSet[key]:
    
    if useSantized:
        testList1.append(" ".join(idToPost[item][1]))
    else:
        testList1.append(idToPost[item][1])
    
    
def countVectorizerSVM(trainList, labels, testList):
    
    trainCountVector = countVec.fit_transform(trainList)
    docClassifier = svm.LinearSVC()
    docClassifier.fit(trainCountVector, labels) 
    
    testCountVector = countVec.transform(testList)
    results = docClassifier.predict(testCountVector)
    return results



    
#Own implementation of word frequency
def wordFrequencySVM(trainList, labels, testList):    
    trainWordList = list()
    
    for post in trainList:
        for word in nltk.word_tokenize(post):
            trainWordList.append(word)
            
    trainFreq = nltk.FreqDist(trainWordList)
    noFeat = len(trainFreq)
    trainKeys = trainFreq.keys()
    
    ordFeat = OrderedDict()
    for key in trainFreq.keys():
        ordFeat.update( {key: trainFreq.freq(key)} )
        
        
    def featureList(corpus):
        featList = []
        for post in corpus:
            listItem = [0]*noFeat
            fileFreqDist = FreqDist()
            fileFreqDist = nltk.FreqDist(nltk.word_tokenize(post))
            
            i =0
            for key in trainKeys:
                if fileFreqDist.has_key(key):
                    listItem[i] = fileFreqDist.get(key)
                i=i+1
                
            featList.append(listItem)
            
        return featList
    
    
    print 'Here!'
    
    featList = featureList(trainList)
    
    #Create numpy Array for word frequencies : Feature Vector
    trainFreqArr = np.array(featList)
    trainLabels = np.array(labels)
    
    docClassifier = svm.LinearSVC()
    docClassifier.fit(trainFreqArr, trainLabels) 
    
    testFeatList = featureList(testList)   
    testFeatArr = np.array(testFeatList)
    
    results = docClassifier.predict(testFeatArr)
    return results
    
    
res = wordFrequencySVM(trainList1, labels1, testList1)
acc = float(sum(res))/len(res)




#===============================================================================
# trainCountVector = countVec.fit_transform(trainList1)
# docClassifier = svm.LinearSVC()
# docClassifier.fit(trainCountVector, labels1) 
# 
# testCountVector = countVec.transform(testList1)
# results = docClassifier.predict(testCountVector)
#===============================================================================

