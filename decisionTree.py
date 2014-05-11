'''
Created on May 10, 2014

@author: Rishi Josan
Use decision tree classifiers for predicting tags and their probabilities 

'''

import nltk
from  nltk.probability import FreqDist
from sklearn import svm
from sklearn.tree import DecisionTreeRegressor
import cPickle as pickle
import numpy as np
import random

#2 are featureKeys, 3 are classifiers
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/classifiersLatDecisionTree10.pk', 'rb') as inp:
    classifiers = pickle.load(inp)
    
######################################### Load data files ################################################# 

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tagsDesc.pk', 'rb') as inp:
    tagsDesc = pickle.load(inp)
       
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/testSetAll.pk', 'rb') as inp:
    testSet = pickle.load(inp)

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPostSan.pk', 'rb') as inp:
    idToPost = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'rb') as inp:
    idToPostOrg = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags2Posts.pk', 'rb') as inp:
    tags2Posts = pickle.load(inp)
################################ End of Load #########################################################



numTags = 10


topTags = set()

for item in tagsDesc[0:100]:
    topTags.add(item[0])
    

trainSet = set()
  

# Create feature vector given vector of posts and ordered list of features
def createFeatures(sentVect, ordList):
    
    noFeat = len(ordList)
    
    featList = []
    for post in sentVect:
        listItem = [0]*noFeat
        fileFreqDist = FreqDist()
        fileFreqDist = nltk.FreqDist(nltk.word_tokenize(post))
            
        i =0
        for key in ordList:
            if fileFreqDist.has_key(key):
                listItem[i] = fileFreqDist.get(key)
            i=i+1
                
        featList.append(listItem)
            
    return featList
 


#For a post, run all classifiers and sort
def getTopLabels(post):
    outPut = []
    for i in range(numTags):
        
        outPutSub = []
        
        vec = createFeatures([post], classifiers[i][2])
        featArr = np.array(vec[0])
        classifier = classifiers[i][3]
        res = classifier.predict(featArr)
        
        if res[0] == 1:
            prob = classifier.predict_log_proba(featArr)
            print 'LogProb'
            print prob
            prob1 = classifier.predict_proba(featArr)
            print prob1
            outPutSub.append(tagsDesc[i][0])
            outPutSub.append(prob)
            outPutSub.append(prob1)
            outPut.append(outPutSub)
            
    return outPut
     

def predictLabels():
    postNo = 0
    for item in postsToTest:
        
        subList=[]
        
       
        postTest = " ".join(idToPost[item][1])
        out = getTopLabels(postTest)
        
        subList.append(item) #Post No.
        subList.append(idToPostOrg[item][1]) #Post
        subList.append(idToPostOrg[item][3]) #List of original Tags
        subList.append(out) #List of predicted tags
        
        topCount = 0
        topPres = list()
        for tag in idToPostOrg[item][3]:
            if tag in topTags:
                topCount +=1
                topPres.append(tag)
         
          
        predCount = 0
        predList = list()       
        for tag in out:
            if tag[0] in topTags:
                predCount +=1
                predList.append(tag)
                
        subList.append(topPres) # Top tags present in post
        subList.append(topCount) # No. of top tags present in post
        subList.append(predList) # Top tags present in prediction
        subList.append(predCount) #No of Top tags present in prediction
        
        
        finList.append(subList)
        print str(postNo) + " Complete!"
        postNo+=1
        
    with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/predictLabelsDT.pk', 'wb') as output:
        pickle.dump(finList, output, protocol=0)
        


postsToTest = random.sample(testSet, 1000)
finList = []
predictLabels()
                