'''
Created on Apr 8, 2014
@author: Rishi Josan
Natural Language Processing : Project
'''

import lxml.html
import cPickle as pickle
import sqlite3

res = list()
idToPost = dict()
tags = set()
tags2Posts = dict()

#Dump required fields(posts) from Database to Python List
def dumpDB():
    conn = sqlite3.connect('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/so-dump.db')
    
    cur = conn.cursor()
    cur.execute('SELECT Title, Body, OwnerUserID, Tags, Id FROM posts where Tags is not null')
    
    for item in cur:
        record = list(item)
        page = lxml.html.document_fromstring(record[1])
        record[0] = str(record[0])
        record[1] = str(page.text_content()) # Stripping HTML Tags
        record[3] = str(record[3])[1:-1].split('><') # Converting Tags to Array
        res.append(record)
     
    with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/posts.pk', 'wb') as output:
        pickle.dump(res, output, protocol=0)
    

#Create Python Dictionary for ID->Post
def dumpId2Post():
    for item in res:
        idToPost[item[4]] = item[0:4]
       
    with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'wb') as output:
        pickle.dump(idToPost, output, protocol=0)

#Dump Set of Tags to Disk
def dumpTags():
    for entry in res:
        for item in entry[3]:
            tags.add(item)
           
    with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags.pk', 'wb') as output:
        pickle.dump(tags, output, protocol=0)
        

# Create Dictionary of Tags with Values as List of Posts with the tag
def dumpTags2Posts():
    for item in res:
        for tag in item[3]:
            if tags2Posts.has_key(tag):
                tags2Posts[tag].append(item[4])
        else:
            tags2Posts[tag] = [item[4]]
           
       
    with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags2Posts.pk', 'wb') as output:
        pickle.dump(tags2Posts, output, protocol=0)



with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/posts.pk', 'rb') as inp:
    res = pickle.load(inp)
   
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/idToPost.pk', 'rb') as inp:
    idToPost = pickle.load(inp)
   
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags.pk', 'rb') as inp:
    tags = pickle.load(inp)
   
with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/tags2Posts.pk', 'rb') as inp:
    tags2Posts = pickle.load(inp)



