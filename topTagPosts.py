'''
Created on Apr 16, 2014

@author: Rishi Josan
'''

import cPickle as pickle
import random

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tagsDesc.pk', 'rb') as inp:
    tagsDesc = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags2Posts.pk', 'rb') as inp:
    tags2Posts = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'rb') as inp:
    idToPost = pickle.load(inp)
    
    
numTags = 100
    
topList = list() #List of posts for top tags
postsAdded = set() # Set for posts already added. To prevent duplicate posts in SVM train set
        #=======================================================================
        # if post not in postsAdded:
        #    postsAdded.add(post)
        #=======================================================================

#Create List with posts from top numTags tags. Add Post and tag to list
for i in range(numTags):
    subList = list() # Unique posts for a single tag
    for post in tags2Posts[tagsDesc[i][0]]:
        #item = list()
        #item.append(post)
        #item.append(tagsDesc[i][0]) #Tag
        #item.append(idToPost[post][0]) # Title of Post
        #item.append(idToPost[post][1]) # Body of Post
        #subList.append(item)
        subList.append(post)
    topList.append(subList)
    
  
 
    
# For each top tag, collect 60 positive and 1500 negative posts(Originally)
posList = list() 
negList = list()

    
# Create Pos List
for i in range(numTags):
    numPosts = 4*len(topList[i])/5
    if numPosts > 1000:
        numPosts = 1000
    posList.append(random.sample(topList[i], numPosts))
   
    
    
#Create TestSet
posTestList = list()
for i in range(numTags):
    posSet = set(posList[i])
    totSet = set(topList[i])
    testSet = totSet - posSet
    numTest = len(testSet)
    if numTest > 1000:
        numTest = 1000
    posTestList.append(random.sample(testSet, numTest))
    
#finTestSet = list(set(posTestList[0]) - set(posList[0]))
    
    
#Create list of sets for posts for top tags 

tagSetList = list()  
for i in range(numTags):
    tagSetList.append(set(tags2Posts[tagsDesc[i][0]]))
    
postSet = set(idToPost.keys())




# Create NegList 
for i in range(numTags):

    negPosts = random.sample(postSet-tagSetList[i], 1000) #All posts - posts corresponding to tag in question
    negList.append(negPosts)
    #print 'Tag' + str(i) + 'complete!'
    


negTestList = []
 
#Create NegTestSet
for i in range(numTags):
    negTrainSet = set(negList[i])
    
    negTestSet = random.sample(postSet-negTrainSet-tagSetList[i], 1000) # All posts - neg train set - posts corresponding to tag
    negTestList.append(negTestSet)
    
    



    
#Originally PosList had 60 words and neglist had 15000 words

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/posListTop100.pk', 'wb') as output:
    pickle.dump(posList, output, protocol=0)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/negListTop100.pk', 'wb') as output:
    pickle.dump(negList, output, protocol=0)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/posTestTop100.pk', 'wb') as output:
    pickle.dump(posTestList, output, protocol=0)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/negTestTop100.pk', 'wb') as output:
    pickle.dump(negTestList, output, protocol=0)


    
#Find min no. of posts    
#===============================================================================
# 
# minP = len(topList[0])
# 
# for x in range(numTags):
#    if len(topList[x]) < minP:
#        minP = len(topList[x])
#===============================================================================
       
#===============================================================================
#       
# for i in range(numTags):
#    numPosts = 0
#    negSubList = list()
#    while(numPosts < 1500):
#        post = random.choice(idToPost.keys()) 
#        #if post not in tags2Posts[tagsDesc[i][0]]: #Post does not correspond to this tag
#        if post not in tagSetList[i]:
#            negSubList.append(post)
#            numPosts += 1
#    negList.append(negSubList)
#===============================================================================

