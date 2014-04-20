'''
Created on Apr 19, 2014

@author: Rishi Josan
'''
import  cPickle as pickle
from sklearn import svm
import SVM
import numpy as np

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

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'rb') as inp:
    idToPost = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags2Posts.pk', 'rb') as inp:
    tags2Posts = pickle.load(inp)
################################ End of Load #########################################################

topTags = set()

for item in tagsDesc[0:100]:
    topTags.add(item[0])
    
testSet = []

def getTopTestPosts():
 
    for i in range(100):
        topTags.remove(tagsDesc[i][0]) # Remove tag in question
        
        leftPosts = set(tags2Posts[tagsDesc[i][0]]) - set(posList[i]) #Remove posts with the tag in question
        
        finPosts = []
            
        for item in leftPosts:
            for tag in idToPost[item][3]:
                if tag in topTags:
                    finPosts.append(item)
                    continue
        
        topTags.add(tagsDesc[i][0])
        testSet.append(finPosts)
        
        with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/testSet.pk', 'wb') as output:
            pickle.dump(testSet, output, protocol=0)
        
        
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/testSet.pk', 'rb') as inp:
    testSet = pickle.load(inp)


posts = []

for item in testSet[99]:
    posts.append(idToPost[item][1])

vec = SVM.createFeatures(posts, classifiers[99][2])

featArr = np.array(vec)

classifier = classifiers[99][3]
labels = [1]*len(featArr)
scores = classifier.score(featArr,labels)
prob = classifier.decision_function(featArr)
