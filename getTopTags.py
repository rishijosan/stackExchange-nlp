'''
Created on Apr 19, 2014

@author: Rishi Josan
'''
import  cPickle as pickle
from sklearn import svm
#import SVM
import numpy as np
from  nltk.probability import FreqDist
import nltk
import random

######################################### Load data files ################################################# 
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/classifiersLat.pk', 'rb') as inp:
    classifiers = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tagsDesc.pk', 'rb') as inp:
    tagsDesc = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/posListTop100.pk', 'rb') as inp:
    posList = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/negListTop100.pk', 'rb') as inp:
    negList = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/posTestTop100.pk', 'rb') as inp:
    posTestSet = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/negTestTop100.pk', 'rb') as inp:
    negTestSet = pickle.load(inp)

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPostSan.pk', 'rb') as inp:
    idToPost = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'rb') as inp:
    idToPostOrg = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags2Posts.pk', 'rb') as inp:
    tags2Posts = pickle.load(inp)
################################ End of Load #########################################################


numTags = 100


topTags = set()

for item in tagsDesc[0:100]:
    topTags.add(item[0])
    
testSet = []
trainSet = set()
    
#Create set of training posts
def createTrainSet():

    for item in posList:
        for post in item:
            trainSet.add(post)
            
    for item in negList:
        for post in item:
            trainSet.add(post)

#Create testSet with posts which have maltiple topTags and are not included in any training set
def getTopTestPosts():
 
    for i in range(numTags):
        topTags.remove(tagsDesc[i][0]) # Remove tag in question
        
        leftPosts = set(tags2Posts[tagsDesc[i][0]]) - set(posList[i]) #Remove train set posts with the tag in question
        
        #finPosts = []
            
        for item in leftPosts:
            if item not in trainSet:
                for tag in idToPost[item][3]:
                    if tag in topTags:
                        #finPosts.append(item)
                        testSet.append(item)
                        continue
        
        topTags.add(tagsDesc[i][0])
        #testSet.append(finPosts)
        
        with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/testSet.pk', 'wb') as output:
            pickle.dump(testSet, output, protocol=0)
        
#===============================================================================
# createTrainSet()
# getTopTestPosts()
#===============================================================================

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
 
        
        
       
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/testSet.pk', 'rb') as inp:
    testSet = pickle.load(inp)





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
            prob = classifier.decision_function(featArr)
            outPutSub.append(tagsDesc[i][0])
            outPutSub.append(prob[0])
            outPut.append(outPutSub)
            
    return outPut
     
print "Starting!"



postsToTest = random.sample(testSet, 1000)
finList = []

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
        
    with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/predictLabels.pk', 'wb') as output:
        pickle.dump(finList, output, protocol=0)
                
