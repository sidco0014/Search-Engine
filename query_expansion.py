import os
import sys
import collections
import operator
import math

common = open('common_words.txt', 'r', encoding='utf-8')
stop_words = common.read().splitlines()

inv_index_dict = {}
term_doc_info = []
terms_in_each_doc = {}
inverted_list = []
relevant_docs_tf = {}
non_rel_docs_tf = {}
no_of_tokens = []
no_of_tokens_in_each_doc = {}
rel_docs_for_each_query = collections.OrderedDict()

invindex_term_tfidf = {}
tfidf = []
query_vector = {}
expanded_file = open('expanded_query.txt','a+',encoding='utf-8')
#retrieving the number of tokens in each document
with open("tokenscount.txt",'r',encoding='utf-8') as f2:
        for val in f2:
            no_of_tokens.append(eval(val))

    #creating a dictionary that stores the number of tokens in each document
for token in no_of_tokens:
        no_of_tokens_in_each_doc[token[0]] = token[1]


    #retrieving the tfidf score of all terms
with open("tfidf_invindex.txt",'r',encoding='utf-8') as f1:
        for val in f1:
            tfidf.append(eval(val))

    #creating a dictionary that stores the tfidf of every term in the inverted index
for score in tfidf:
        invindex_term_tfidf[score[0]] = score[1]

    #retrieving terms in each doc
with open("terms_in_docs.txt",'r',encoding='utf-8') as f3:
        for val in f3:
            term_doc_info.append(eval(val))

    #creating a dictionary that stores the information about terms in each doc
for i in term_doc_info:
        terms_in_each_doc[i[0]] = i[1]

def rocchio(query,rel_docs_for_each_query,count):
    global rel_docs,query_vector,rel_doc_vec,non_rel_vector
    rel_docs = []
    rel_doc_vec={}
    non_rel_vector={}
    query_vector={}

    query = query.split()
    #print(query)

    #creating the query vector
    #considering idf as 1 in case of query
    for term in query:
        if term in query_vector.keys():
            continue
        else:
            query_vector[term] = query.count(term)

    for term in invindex_term_tfidf.keys():
        if term in query:
            if term in query_vector.keys():
                query_vector[term]+=1
            else:
                query_vector[term]=1
        else:
            query_vector[term]=0

    rel_docs = rel_docs_for_each_query[str(count)]

    rel_doc_vec = {}
    non_rel_docs = []
    non_rel_vector = {}

    '''for doc in rel_docs:
        terms = terms_in_each_doc[doc]
        for t in terms:
            val = [x[1] for x in invindex_term_tfidf[t] if x[0] == doc]
            if doc not in rel_doc_vec.keys():
                rel_doc_vec[doc] = [[term,val]]
            else:
                rel_doc_vec[doc].append([term,val])'''
    #print(rel_docs)
    rel_vec={}
    for term in invindex_term_tfidf.keys():
        values = invindex_term_tfidf[term]
        for doc in values:
            if doc[0] in rel_docs:
                if term in rel_vec:
                    rel_vec[term]+=float(doc[1])
                else:
                    if term == 'sorting':
                        print('once '+ str(doc[1]))
                    rel_vec[term] = float(doc[1])
            else:
                if term in rel_vec:
                    continue
                else:
                    rel_vec[term]=0

    for doc in no_of_tokens_in_each_doc.keys():
        if doc not in rel_docs:
            non_rel_docs.append(doc)

    for term in invindex_term_tfidf.keys():
        values = invindex_term_tfidf[term]
        for doc in values:
            if doc[0] in non_rel_docs:
                if term in non_rel_vector.keys():
                    non_rel_vector[term]+=doc[1]
                else:
                    non_rel_vector[term]=doc[1]
            else:
                if term in non_rel_vector:
                    continue
                else:
                    non_rel_vector[term]=0
    alpha=8
    beta=16
    gamma=4
    b=float(beta/len(rel_docs))
    g=float(gamma/len(non_rel_docs))
    #print(non_rel_vector)
    #print(query_vector)
    #print(rel_vec)
    for term in invindex_term_tfidf.keys():
        non_rel_vector[term]=g*non_rel_vector[term]
        rel_vec[term]=b*rel_vec[term]
        query_vector[term]=alpha*query_vector[term]
    list_of_query_vec={}
    for term in invindex_term_tfidf.keys():
        if term not in list_of_query_vec:
            list_of_query_vec[term] = query_vector[term] + rel_vec[term] - non_rel_vector[term]
    #print(list_of_query_vec)
    roc=open("rocchio.txt","w+",encoding="utf-8")
    global sorted_index
    sorted_index=[]

    sorted_index = sorted(list_of_query_vec.items(), key=operator.itemgetter(1), reverse=True)

    # get the new query by expanding it with elements
    si = []
    #print(sorted_index[:5])
    global expanded_terms
    expanded_terms=[]
 #   resultwords = [word for word in querywords if word not in stop_words]
    lst = []
    for i in sorted_index:
        lst.append(i[0])

    s = [word for word in lst if word not in stop_words]

    for k in s:
        if k in query:
            #print(k[0])
            continue
        else:
           si.append(k)
    #s = [word for word in sorted_index if word not in stop_words]

    print(si[:15])
    l= len(query)
    #print(l)
    #expanded_terms = query + [x[0] for x in sorted_index[l:l+5]]
    #print(si[:5])
    #print(sorted_index[:5])
    l = len(query)
    expanded_terms = query + si[:15]

    #print(str(sorted_index[l:l+5]))
    print('\n')
    #print(expanded_terms)
    e = ' '.join(expanded_terms)
    print(expanded_terms)
    print(e)
    #print(str(e))
    expanded_file.writelines(e)
    expanded_file.write('\n')

    #for i in sorted_index:
    #    roc.write(str(i) + '\n')


    #print(len(query_vector))
    #print(rel_doc_vec)
    #print(len(non_rel_vector))

    
def main():
    count = 1
    fi = open("Relevant_Docs_for_each_query.txt",'r',encoding='utf-8')
    for val in fi.readlines():
        x=val.split()
        rel_docs_for_each_query[x[0]] = x[1:]
    query = open('query.txt','r',encoding='utf-8')
    for q in query:

        #q =  "algorithms"
        #print(q)
        #q="i am interested in articles written either by prieve or udo pooch prieve b pooch u"
        rocchio(q,rel_docs_for_each_query,count)
        count=count+1

main()
    

    
