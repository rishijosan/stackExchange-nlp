from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import cPickle as pickle
import numpy as np
import nltk
from nltk.corpus import PlaintextCorpusReader
from sklearn import svm


with open('C:/Users/Abhinav/Desktop/Course work/NLP/Project/nlp/classifiersLat.pk', 'rb') as inp:
        classifirs = pickle.load(inp)
        
# for item in classifirs:
#     print item
 
print 'done'   
numtags = 100

cnt_pos = [] # to store number of positive correct
cnt_neg = [] # to store number of negative correct

acc_pos = [] # positive accuracy inside loop
acc_neg = []# negative accuracy inside loop

# neg_acc = [] # negative accuracy for each tag
# pos_acc = [] # positive accuracy for each tag

posTest_size = [] # test size of positive tags
negTest_size = [] # test size of negative tags

globl = []

for i in range(numtags):  
         
#        print "Starting " + str(i)
#        feats = createFeatures(negTestVect[i], classifiers[i][2])
        cnt_ps = 1 # 4 local variable to store temp count and size of positive and negative result
        cnt_ng = 1
        sm_pos = 0
        sm_neg = 0
        
        result_pos = classifirs[i][1] # positive result
        result_neg = classifirs[i][5] # negative result
        
        acc_pos.append(classifirs[i][0]) # positive accuracy
        acc_neg.append(classifirs[i][4]) # negative accuracy
        
        posTest_size.append(len(result_pos)) #positive test size
        negTest_size.append(len(result_neg)) #negative test size      
        
        for item in result_pos:
            if item == 1:
                cnt_ps += 1 
        cnt_pos.append(cnt_ps) # store number of positive correct
        
        
               
        for item in result_neg:     
            if item == 0:
                cnt_ng += 1
        cnt_neg.append(cnt_ng) #store number of negative correct

print 'Positive Test size of each tag'        
for item in posTest_size:
    print item
print 'Negative Test size of each tag'
for item in negTest_size:
    print item
    
for i in range(numtags):
    globl.append(float((cnt_pos[i] + cnt_neg[i])/(posTest_size[i] + negTest_size[i])))
    
  
    
# for item in acc_pos:
#         sm_pos += item
# pos_acc.append(sm_pos/len(acc_pos))        
# for item in acc_neg:
#         sm_neg += item
# neg_acc.append(sm_neg/len(acc_neg))
        
        

        #cnt_neg.index(i).append(cnt_ng)           
#         
# with open('C:/Users/Abhinav/Desktop/Course work/NLP/Project/nlp/posts.pk', 'rb') as inp:
#     posts = pickle.load(inp)
# 
# 
# tags = 'windows'
# 
# tags_lst = list()
# 
# #question list for success and fail cases for tags
# ques_yes = list()
# ques_no = list()
# 
# #count variable for keeping count 
# cnt_yes = 0
# cnt_no = 0
# 
# rows = len(posts)
# 
# # 
# for item in posts:
#         for tag in item[3]:
#             tags_lst = tag 
#             if tags_lst.__contains__(tags):
#                 if cnt_yes < 1500:
#                     ques_yes.append(item[1])
#                     cnt_yes += 1
#             elif cnt_no < 60 :
#                 ques_no.append(item[1])
#                 cnt_no += 1
#                  
#                  
#             
# for ques in ques_yes:
#     print ques
# 
# # 
# #for row in range(rows):
# # row = 1     
# # item = posts[row]
# # print item