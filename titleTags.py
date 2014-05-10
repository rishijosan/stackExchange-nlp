'''
Created on May 9, 2014

@author: Rishi Josan
'''
import cPickle as pickle
import nltk
from nltk.probability import FreqDist
import random
import operator


with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'rb') as inp:
    idToPostOrg = pickle.load(inp)

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPostSan.pk', 'rb') as inp:
        idToPost = pickle.load(inp)
        
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tagsDesc.pk', 'rb') as inp:
    tagsDesc = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/posListTop100.pk', 'rb') as inp:
    posList = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/negListTop100.pk', 'rb') as inp:
    negList = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/posTestTop100.pk', 'rb') as inp:
    posTestList = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/negTestTop100.pk', 'rb') as inp:
    negTestList = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags2Posts.pk', 'rb') as inp:
    tags2Posts = pickle.load(inp)
    
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/testSet.pk', 'rb') as inp:
    testSet = pickle.load(inp)
    
    
numTags = 100

#Create list of tagsDescwith only tags
orderedTags = []
for item in tagsDesc:
    orderedTags.append(item[0])

common = dict()
total = dict()
usefulness = dict()

def createUsefulness():

    for tag in range(numTags):
        for post in posList[tag]:
            tags = idToPost[post][3]
            for word in idToPost[post][0]:
                if total.has_key(word):
                    total[word] += 1
                else:
                    total[word] = 1
                
                if word in tags:
                    if common.has_key(word):
                        common[word] += 1
                    else:
                        common[word] = 1
                    
        for post1 in negList[tag]:
            tags1 = idToPost[post1][3]
            for word in idToPost[post1][0]:
                if total.has_key(word):
                    total[word] += 1
                else:
                    total[word] = 1
                
                if word in tags1:
                    if common.has_key(word):
                        common[word] += 1
                    else:
                        common[word] = 1
    
    for word in total:
        if common.has_key(word):
            usefulness[word] = float(common[word]) / total[word]
        else:
            usefulness[word] = 0



createUsefulness()

#There are about 2000 words with usefulness > 0.4
#===============================================================================
# usefulSort = sorted(usefulness.iteritems(), key=operator.itemgetter(1))
# usefulSort.reverse()
#===============================================================================

predTags = []
def predictTags():
    
    #testList = posTestList + negTestList
    testList = [testSet]
    
    for postList in testList:
        for post in postList:
            predRow= []
            predRow.append(post)
            
            tagsForPost = dict()
            for word in idToPost[post][0]:
                if usefulness.has_key(word):
                    score = usefulness.get(word)
                    if score >= 0.4:
                        tagsForPost.update({word:score})
                    
                        
                        
            predRow.append(tagsForPost)
            
            predTags.append(predRow)
            
            
    with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/predictLabelsTitleTS.pk', 'wb') as output:
        pickle.dump(predTags, output, protocol=0)
            
        




predictTags()





 
#Compute no.oftagscovered by the training set = 4934/5108
def tagsCovered():
    tagSet = set()
     
    for tag in range(numTags):
        for post in posList[tag]:
            tags = idToPost[post][3]
            for tt in tags:
                tagSet.add(tt)
                
    for tag in range(numTags):
        for post in negList[tag]:
            tags = idToPost[post][3]
            for tt in tags:
                tagSet.add(tt)
     

posFreqDist = []
negFreqDist = []
totFreqDist = []

 
 
def createFreqDist(posFreqDist=posFreqDist, negFreqDist=negFreqDist, totFreqDist=totFreqDist ):
    
    # Create Freq Dist for Pos Cases
    for tag in range(numTags):
        tagPosFreqDist = FreqDist()
        for post in posList[tag]:
            for word in idToPost[post][0]:
                tagPosFreqDist.inc(word)
        posFreqDist.append(tagPosFreqDist)
        
        
    # Create Freq Dist for Neg Cases, select only the no. of posts as in the PosList
    for tag in range(numTags):
        tagNegFreqDist = FreqDist()
        
        if len(posList[tag]) != 1000:
            newList = random.sample(negList[tag],len(posList[tag]))
            print 'Not 100, Tag: ' + str(tag)
        else:
            newList = negList[tag]
            
        for post in newList:
            for word in idToPost[post][0]:
                tagNegFreqDist.inc(word)
        negFreqDist.append(tagNegFreqDist)
        
        
    #Create Total Freq Dist
    for i in range(numTags):
        tagFreqDist = posFreqDist[i] + negFreqDist[i]
        totFreqDist.append(tagFreqDist)
        
#===============================================================================
# testScores = []       
#        
# for i in range(numTags):
#    tagScore =[]       
#    for post in posTestSet[i]:
#        score = 0
#        for word in idToPost[post][0]:
#            if word in posFreqDist[i]:
#                score += posFreqDist[i].freq(word)
#        tagScore.append(score)
#        
#===============================================================================
            
