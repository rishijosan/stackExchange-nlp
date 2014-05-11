'''
Created on May 11, 2014

@author: Rishi Josan
'''
import csv
import cPickle as pickle

with open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/finFormResSVM.pk', 'rb') as inp:
    resultSet = pickle.load(inp)

csvfile = open('/media/sf_G_DRIVE/nlp/Project/dataset/superuser/finRes.csv', 'wb')
csvwriter = csv.writer(csvfile)

for item in resultSet:
    csvwriter.writerow(item)
    
csvfile.close()

