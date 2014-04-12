'''
Created on Apr 11, 2014

@author: Rishi Josan
'''
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import cPickle as pickle
import numpy as np
import nltk
from nltk.corpus import PlaintextCorpusReader
from sklearn import svm

transformer = TfidfTransformer()
vectorizer = TfidfVectorizer()

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tagsDesc.pk', 'rb') as inp:
    tagsDesc = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags2Posts.pk', 'rb') as inp:
    tags2Posts = pickle.load(inp)
    
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'rb') as inp:
    idToPost = pickle.load(inp)
    

idToPost[tags2Posts['linux'][0]]

sublist = list()

#Create List with posts from top 4 tags. Add Post and tag to list
for i in range(4):
    for post in tags2Posts[tagsDesc[i][0]]:
        item = list()
        item.append(idToPost[post][1]) # Body of Post
        item.append(tagsDesc[i][0])
        sublist.append(item)
     
print 'before NumPY'   
#Convert list to numpy array
docsNP = np.array(sublist)
print 'NumPY'

#Column vector of posts
#docsNP[:,0]

#Create numPY matrix with features l
newVec = vectorizer.fit_transform(docsNP[:,0])

docClassifier = svm.LinearSVC()
docClassifier.fit(newVec, docsNP[:,1]) 