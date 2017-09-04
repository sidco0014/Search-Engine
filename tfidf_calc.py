import os
import sys
import collections
import operator
import math


inv_index_dict = {}
terms_in_each_doc = {}
inverted_list = []
no_of_tokens = []
no_of_tokens_in_each_doc = {}
invindex_term_tfidf = {}
normalized_tf = {}
inverse_doc_freq = {}

def calculate_tfidf():


    #Retrieving the dictionary of inverted list of unigrams
    with open("F://IR//Project Files//inverted_index_unigrams.txt",'r',encoding='utf-8') as f:
        for val in f:
            inverted_list.append(eval(val))


    #storing the inverted index in a dictionary
    for row in inverted_list:       
        inv_index_dict[row[0]]=row[1]
        values=row[1]
        #maintainig a dictionary that keeps track of the terms that each document contains
        for v in values:
            if v[0] in terms_in_each_doc.keys():
                terms_in_each_doc[v[0]].append(row[0])
            else:
                terms_in_each_doc[v[0]] = [row[0]]

    f5 = open("F://IR//Project//terms_in_docs.txt",'w+',encoding='utf-8')
    for data in terms_in_each_doc.items():
        f5.write(str(data)+"\n")


    #retrieving the number of tokens in each document 
    with open("F://IR//Project Files//tokenscount.txt",'r',encoding='utf-8') as f2:
        for val in f2:
            no_of_tokens.append(eval(val))



    #creating a dictionary that stores the number of tokens in each document
    for token in no_of_tokens:
        no_of_tokens_in_each_doc[token[0]] = token[1]




    #calculating the normalised term frequency for every term
    for key in inv_index_dict.keys():
        values=inv_index_dict[key]
        
        for v in values:
            for totaltokens in no_of_tokens_in_each_doc.items():
                if v[0] == totaltokens[0]:
                    #print(key + " " +str(v[0])+" " +v[1])
                    if key in normalized_tf.keys():
                        normalized_tf[key].append([v[0],float(v[1]/totaltokens[1])])
                    else:
                        normalized_tf[key] = [[v[0],float(v[1]/totaltokens[1])]]

  
    #calculating the inverse document frequency for every term
    for key in inv_index_dict.keys():
        values=inv_index_dict[key]
        idf= 1 + math.log(len(no_of_tokens_in_each_doc)/len(values))
        inverse_doc_freq[key] = idf

    



    invindex_term_tfidf = collections.OrderedDict()
    
    #calculating tfidf value for documents which contain the query terms
    for term in inv_index_dict.keys():
        values=normalized_tf[term]
        for v in values:
            if term in invindex_term_tfidf.keys():
                invindex_term_tfidf[term].append([v[0],(float(v[1])*inverse_doc_freq[term])])
            else:
                invindex_term_tfidf[term] = [[v[0],(float(v[1])*inverse_doc_freq[term])]]
       
    

    f1 = open("F://IR//Project//tfidf_invindex.txt",'w+',encoding='utf-8')
    for data in invindex_term_tfidf.items():
        f1.write(str(data)+"\n")
        

                                    
            
        
     


    
    

calculate_tfidf()

    
