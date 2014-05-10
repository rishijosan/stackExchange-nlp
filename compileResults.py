'''
Created on May 9, 2014

@author: Rishi Josan
'''
import cPickle as pickle

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/predictLabels.pk', 'rb') as inp:
    bodyTags = pickle.load(inp)

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/testSet.pk', 'rb') as inp:
    testSet = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/predictLabelsTitleTS.pk', 'rb') as inp:
    titleTags = pickle.load(inp)
    

titleTagDict = dict()
for item in titleTags:
    titleTagDict.update({item[0] : item[1]})
    
    
resultSet = []
for item in bodyTags:
    resRow = []
    resRow.append(item[0]) # Post No
    resRow.append(item[2]) # Original Tags
    
    titleTag = titleTagDict[item[0]]
    resRow.append(titleTag.keys()) #Predicted Title Tags
    
    if len(titleTag.keys()) != 0:
        count = 0
        for ky in titleTag.keys():
            if ky in item[2]:
                count += 1
        prec = float(count)/len(titleTag.keys())
    else:
        prec = 0
    
    resRow.append(prec) #Precision of Title Tags
    
    resRow.append(item[3]) #Predicted Body Tags
    
    
    count = 0
    for ky in item[3]:
        if ky[0] in item[2]:
            count += 1
    prec = float(count)/len(item[3])
    resRow.append(prec) #Precision of Body Tags
    resRow.append(float(count)/len(item[2])) #Recall of body tags
    
    resultSet.append(resRow)
    
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/finResults.pk', 'wb') as output:
    pickle.dump(resultSet, output, protocol=0)
    