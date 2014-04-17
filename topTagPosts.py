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
for i in range(1):
    posList.append(random.sample(topList[i], 10000))
    
    
#Create TestSet
testList = list()
for i in range(1):
    testList.append(random.sample(topList[i], 5000))
    
finTestSet = set(testList[0]) - set(posList[0])
    
    
#Create list of sets for posts for top tags 
tagSetList = list()  
for i in range(numTags):
    tagSetList.append(set(tags2Posts[tagsDesc[i][0]]))
    
postSet = set(idToPost.keys())

# Create NegList 
for i in range(1):

    negPosts = random.sample(postSet-tagSetList[i], 10000) #All posts - posts corresponding to tag in question
    negList.append(negPosts)
    #print 'Tag' + str(i) + 'complete!'
    
    
#Originally PosList had 60 words and neglist had 15000 words

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/posList10k.pk', 'wb') as output:
    pickle.dump(posList, output, protocol=0)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/negList10k.pk', 'wb') as output:
    pickle.dump(negList, output, protocol=0)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/testSet.pk', 'wb') as output:
    pickle.dump(finTestSet, output, protocol=0)

    
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

