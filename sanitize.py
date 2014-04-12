'''
Created on Apr 11, 2014

@author: root
'''

import cPickle as pickle
import nltk
from nltk.corpus import stopwords



   
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'rb') as inp:
    idToPost = pickle.load(inp)
    
#===============================================================================
#    
# with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/posts.pk', 'rb') as inp:
#    posts = pickle.load(inp)
#   
# with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags.pk', 'rb') as inp:
#    tags = pickle.load(inp)
#   
# with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags2Posts.pk', 'rb') as inp:
#    tags2Posts = pickle.load(inp)
#===============================================================================


#Should've used set not list for stop words. Runtime ~1hr
def remStopWords (str):
    filtered_words = [w for w in nltk.word_tokenize(str) if not w in nltk.corpus.stopwords.words('english')] 
    return filtered_words

#Sanitized posts and saved to file
def sanitizePosts():
    for key,post in idToPost.iteritems():
        post[0] = remStopWords(post[0].lower()) #Remove StopWords and convert to lower
        post[1] = remStopWords(post[1].lower()) #Remove StopWords and convert to lower
        idToPost[key] = post
        
    with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPostSan.pk', 'wb') as output:
        pickle.dump(idToPost, output, protocol=0)
        
    
