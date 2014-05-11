'''
Created on May 9, 2014

@author: Rishi Josan
Final Compilation of results 
'''


import cPickle as pickle

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/predictLabels.pk', 'rb') as inp:
    bodyTags = pickle.load(inp)

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/testSet.pk', 'rb') as inp:
    testSet = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/predictLabelsTitleTS.pk', 'rb') as inp:
    titleTags = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'rb') as inp:
    idToPost = pickle.load(inp)
    
    
#Compile results, Compute precision and recall, save to disk
def compileResults():
    titleTagDict = dict()
    for item in titleTags:
        titleTagDict.update({item[0] : item[1]})
        
        
    resultSet = []
    for item in bodyTags:
        resRow = []
        resRow.append(item[0]) # Post No
        resRow.append(idToPost[item[0]][0]) # Title
        resRow.append(idToPost[item[0]][1]) #Post
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
        
        
        allPredTags = set()
        orgTags = set(resRow[3])
        
        #Add predicted title tags
        for predTag in resRow[4]:
            allPredTags.add(predTag)
            
            
        #Add predicted body tags
        for predTag in resRow[6]:
            allPredTags.add(predTag[0])
            
        corrPredTags = orgTags.intersection(allPredTags)
        
        #Global precision
        prec = float(len(corrPredTags))/len(allPredTags)
        
        #Global Recall
        recall = float(len(corrPredTags))/len(orgTags)
            
        resRow.append(allPredTags)#All predicted Tags
        resRow.append(prec) #Global Precision
        resRow.append(recall) #Global Recall
        resRow.append(corrPredTags) #Tags predicted correctly
        
        resultSet.append(resRow)
        
        
    with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/finResultsSVM.pk', 'wb') as output:
        pickle.dump(resultSet, output, protocol=0)
    
    
    

#Now convert all iterables into string for export to excel
def saveFormRes():
    with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/finResultsSVM.pk', 'rb') as inp:
        resultSet = pickle.load(inp)
    
    formRes = []
      
    for res in resultSet:
        res[3] = ", ".join(res[3])
        res[4] = ", ".join(res[4])
        bodTags = []
        for tag in res[6]:
            bodTags.append(tag[0])
        res[6] = ", ".join(bodTags)
        res[9] = ", ".join(res[9])
        res[12] = ", ".join(res[12])
        formRes.append(res)
        
    with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/finFormResSVM.pk', 'wb') as output:
        pickle.dump(formRes, output, protocol=0)


saveFormRes()
    