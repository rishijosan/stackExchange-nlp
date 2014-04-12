'''
Created on 11-Apr-2014

@author: Abhinav
'''

import cPickle as pickle

with open('C:/Users/Abhinav/Desktop/Course work/NLP/Project/nlp/tags2Posts.pk', 'rb') as inp:
    tags2Posts = pickle.load(inp)

ordTags = dict()

# Generating ordered list based on the descending order of number of time tags has been used

for key, val in tags2Posts.iteritems():
    ordTags[key] = len(tags2Posts.get(key))
    

with open('C:/Users/Abhinav/Desktop/Course work/NLP/Project/nlp/tagsDesc.pk', 'wb') as output:
        pickle.dump(sorted(ordTags.items(), key=lambda x:x[1], reverse = True), output, protocol=0)

#sorted(ordTags.items(), key=lambda x:x[1], reverse = True)
