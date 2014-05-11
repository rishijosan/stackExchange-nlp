'''
Created on Apr 17, 2014

@author: Rishi Josan
'''
import nltk
from  nltk.probability import FreqDist
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import cPickle as pickle
import numpy as np
from collections import OrderedDict

# Use sanitized text
useSantized = True


vectorizer = TfidfVectorizer()
#countVec = CountVectorizer(stop_words='english')
countVec = CountVectorizer()

print 'In SVM'

######################################### Load data files #################################################   
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
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/posTestTop100.pk', 'rb') as inp:
    posTestSet = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/negTestTop100.pk', 'rb') as inp:
    negTestSet = pickle.load(inp)
################################ End of Load #########################################################

trainVect = list()
posTestVect = list()
labelVect = list()
negTestVect = list()

numtags = 100


# Create Vectors of posts from ids
def prepPostLists():
  
    for key in range(numtags):
        
        #Create Vectors 
        trainList1 = list()
        testList1 = list()
        labels1 = list()
        negTestList1 = list()
        
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
            
        for item in posTestSet[key]:
            
            if useSantized:
                testList1.append(" ".join(idToPost[item][1]))
            else:
                testList1.append(idToPost[item][1])
                
                
                
        for item in negTestSet[key]:
            
            if useSantized:
                negTestList1.append(" ".join(idToPost[item][1]))
            else:
                negTestList1.append(idToPost[item][1])
                
            
                
        trainVect.append(trainList1)
        posTestVect.append(testList1)
        labelVect.append(labels1)
        negTestVect.append(negTestList1)
    
    
    print "Posts done!"
    
    
    
    
# Create Feature Vector from Count Vectorizer and Fit SVM : Accuracy not good    
def countVectorizerSVM(trainList, labels, testList):
    
    trainCountVector = countVec.fit_transform(trainList)
    docClassifier = svm.LinearSVC()
    docClassifier.fit(trainCountVector, labels) 
    
    testCountVector = countVec.transform(testList)
    results = docClassifier.predict(testCountVector)
    return results



    
#Own implementation of word frequency; Also creating classifiers and predicting here: Split into methods
def wordFrequencySVM(trainList, labels, testList):    
    trainWordList = list()
    
    for post in trainList:
        for word in nltk.word_tokenize(post):
            trainWordList.append(word)
            
    trainFreq = nltk.FreqDist(trainWordList)
    noFeat = len(trainFreq)
    trainKeys = trainFreq.keys()
    
    #===========================================================================
    # ordFeat = OrderedDict()
    # for key in trainFreq.keys():
    #    ordFeat.update( {key: trainFreq.freq(key)} )
    #===========================================================================
        
        
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
    return results, trainKeys, docClassifier
    
    

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
    

# Train classifiers for top tags, compute accuracy and save to disk  
def createClassifiers():
    
    prepPostLists()    
    results = list()
    
    for i in range(numtags):
        resList = list()
        res, keys, classifier = wordFrequencySVM(trainVect[i], labelVect[i], posTestVect[i])
        acc = float(sum(res))/len(res)
        resList.append(acc) # Pos Test Accuracy
        resList.append(res) # Pos Test Results
        resList.append(keys) # To maintain order of features
        resList.append(classifier) #Actual classifier : Use to predict
        results.append(resList)  
        print str(i) + " done!"
        
    with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/classifiersLat.pk', 'wb') as output:
        pickle.dump(results, output, protocol=0)


# Append accuracy and results for negative test cases
def appendNegTests():
    
    prepPostLists()
    with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/classifiersLat.pk', 'rb') as inp:
        classifiers = pickle.load(inp)
     
     
    for i in range(numtags):  
         
        print "Starting " + str(i)
        feats = createFeatures(negTestVect[i], classifiers[i][2])
        
        classifier = classifiers[i][3]
        res = classifier.predict(np.array(feats))
        
        acc = float(len(res) - sum(res))/len(res)
        
        classifiers[i].append(acc)
        classifiers[i].append(res)
        print str(i) + " Done!"
        
    
    with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/classifiersLat.pk', 'wb') as output:
        pickle.dump(classifiers, output, protocol=0)
        


#createClassifiers()
#appendNegTests()


#===============================================================================
# with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/classifiers100.pk', 'rb') as inp:
#    classifiers = pickle.load(inp)
# 
# 
# for i in range(numtags):  
#     
#    print "Starting " + str(i)
#    feats = createFeatures(negTestVect[i], classifiers[i][2])
#    
#    classifier = classifiers[i][3]
#    res = classifier.predict(np.array(feats))
#    
#    acc = float(len(res) - sum(res))/len(res)
# 
#    classifiers[i].append(acc)
#    classifiers[i].append(res)
#    print str(i) + " Done!"
#    
#    
#    
# 
# with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/classifiersFin.pk', 'wb') as output:
#    pickle.dump(classifiers, output, protocol=0)
#===============================================================================


#===============================================================================
# trainCountVector = countVec.fit_transform(trainList1)
# docClassifier = svm.LinearSVC()
# docClassifier.fit(trainCountVector, labels1) 
# 
# testCountVector = countVec.transform(testList1)
# results = docClassifier.predict(testCountVector)
#===============================================================================

