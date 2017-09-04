import os
import sys
import math
import operator
import collections 

N = 3204
k1 = 1.2
k2 = 100
b= 0.75
doc_length = collections.OrderedDict()
inverted_index_dict = {}
term_freq_in_each_doc = {}
doc_token_info= {}

inverted_list = []
tokens_in_each_doc = []
visited_terms = []
cacm_rel = []
total_avg_prec = 0
total_reciprocal_rank = 0
mean_reciprocal_rank = 0


def bm25_intermediate_fn(query,avdl,inverted_index_dict,count,R,rel_docs,doc_token_info,f5):
    global total_avg_prec
    global mean_avg_precision
    global total_reciprocal_rank
    global mean_reciprocal_rank
    
    bm25_score= {}
    bm25_ranked_list = []
    query=query.split()
    visited_terms = []
    for term in query:
        r = 0
        #checking whether the score is already calculated for that term
        if term not in visited_terms:
            visited_terms.append(term)
            #checking whether query term is in the inverted index
            if term in inverted_index_dict.keys():
                values=inverted_index_dict[term]
                n=len(values)
                for item in values:
                    #storing the frequency of the term for that doc
                    frequency = item[1]
                    #checking whether the document is in the list of relevant documents for that query
                    if item[0] in rel_docs:
                        if term in doc_token_info[item[0]]:
                            r+=1
                    dl=doc_length[item[0]]
                    #calculating the frequency of the term in the query
                    query_freq = query.count(term)
                    #calculating the BM25 score
                    s = calculate_BM25(frequency,dl,query_freq,n,avdl,R,r)
                    doc=item[0]
                    if doc in bm25_score.keys():
                        bm25_score[doc]+=s
                    else:
                        bm25_score[doc] = s


    bm25_ranked_list =sorted(bm25_score.items(), key=operator.itemgetter(1), reverse=True)

    documents = [x[0] for x in bm25_ranked_list]

    precision = {}
    recall = {}
    total_retrieved_docs = 0
    rel = 0
    avg_precision = 0
    sum_precision = 0
    #calculating precision and recall
    for doc in documents:
        total_retrieved_docs+=1
        if doc in rel_docs:
            rel+=1
            if rel ==1 :
                total_reciprocal_rank+=(float(1/total_retrieved_docs))
            precision[doc] = float(rel/total_retrieved_docs)
            sum_precision = sum_precision+float(precision[doc])
            if R == 0:
                recall[doc] = 0.0
            else:
                recall[doc] = float(rel/R)
        else:
            precision[doc] = float(rel/total_retrieved_docs)
            if R==0:
                recall[doc] =0.0
            else:
                recall[doc] = float(rel/R)

    if R!=0:
        avg_precision = float(sum_precision/R)
        total_avg_prec = float(total_avg_prec+avg_precision)

    #Put count==7 for stemming and 64 for stopping
    if count ==64:
        
        #For stemming divide by 7, for stooping divide by 52
        mean_avg_prec = float(total_avg_prec/52)

        mean_reciprocal_rank = float(total_reciprocal_rank/52)

    f6 = open("F://IR//Project Files//Precision_at_K_BM25_general.txt",'a+',encoding='utf-8')

    #For stemming uncomment this
    #f6 = open("F://IR//Project Files//Task3Stemmed//Precision_at_K_BM25_stemmed.txt",'a+',encoding='utf-8')
    
    #For stopping uncomment this
    #f6 = open("F://IR//Project Files//Task3Stopped//Precision_at_K_BM25_stopped.txt",'a+',encoding='utf-8')

    if len(bm25_ranked_list)<100:
        x=len(bm25_ranked_list)
    else:
        x=100
    
    for i in range(x):
        document = str(bm25_ranked_list[i][0])
        if document in rel_docs:
            relevance = "R"
        else:
            relevance = "NR"
        f5.write('{:10} {:2} {:40} {:5} {:30} {:10} {:40} {:20}'.format("" + str(count), "Q0", "" + document, "" + str(i+1), "" + str(bm25_ranked_list[i][1]),
                                               relevance, "" + str(precision[document]), "" + str(recall[document])) + '\n')
        if ((i+1)==5 or (i+1)==20):
            f6.write("Precision @ K= "+str(i+1)+" for query number : "+str(count)+" is : "+str(precision[document])+"\n")


    # Put count==7 for stemming and 64 for stopping
    if count ==64:
        f5.write("Mean Average Precision (MAP) : "+str(mean_avg_prec)+"\n")
        f5.write("Mean Reciprocal Rank (MRR) : "+str(mean_reciprocal_rank))

    f4=open("F://IR//Project Files//Relevant_Docs_for_each_query.txt",'a+',encoding='utf-8')
    
    #For stopping uncomment this
    #f4=open("F://IR//Project Files//Task3Stopped//Relevant_Docs_for_each_stopped_query.txt",'a+',encoding='utf-8')
    
    #For stemming uncomment this
    #f4=open("F://IR//Project Files//Task3Stemmed//Relevant_Docs_for_each_stemmed_query.txt",'a+',encoding='utf-8')
    
    f4.write(str(count)+" ")
    for j in range(10):
        f4.write(bm25_ranked_list[j][0]+" ")
    f4.write("\n")
        


def calculate_BM25(freq,doclen,qf,n,avdl,R,r):
    x = float(doclen/avdl)
    x = (b*x)
    z = (1-b)
    K = (k1*(z+x))
    p1 = float((r+0.5)/(R-r+0.5))
    p2 = float((n-r+0.5)/(N-n-R+r+0.5))
    temp=(p1/p2)
    p3 = math.log(temp if temp>0 else 1)
    p4 = float(((k1+1)*freq)/(K+freq))
    p5 = float(((k2+1)*qf)/(k2+qf))
    score = (p3*p4*p5)

    return score
    


def main():
    

    f5=open("F://IR//Project Files//bm25_general_corpus_results.txt",'a+',encoding='utf-8')
    
    #For stopping uncomment this
    #f5=open("F://IR//Project Files//Task3Stopped//bm25_stopped_corpus_results.txt",'a+',encoding='utf-8')
    
    #For stemming uncomment this
    #f5=open("F://IR//Project Files//Task3Stemmed//bm25_stemmed_corpus_results.txt",'a+',encoding='utf-8')
    
    count = 0
    path = "F://IR//Project Files//CACMCORPUS//"
    sum_doc_length = 0
    #calculating the document length for every document
    for filename in os.listdir(path):
       temp = str(filename)
       temp=temp.rstrip('.txt')
       fi=  open(path+filename,'r',encoding="utf-8").readlines()
       dl=len(fi)
       doc_length[temp]=dl
       sum_doc_length+=dl
       
    #calculating avdl 
    avdl = float(sum_doc_length/N)

    #Retrieving the dictionary of inverted list of unigrams
    
    #For stemming uncomment this
    #with open("F://IR//Project Files//Stopped and Stemmed Files_Task3//inverted_index_stemmed_unigrams.txt",'r',encoding='utf-8') as f:

    #For stopping uncomment this
    #with open("F://IR//Project Files//Stopped and Stemmed Files_Task3//inverted_index_stopped_unigrams.txt",'r',encoding='utf-8') as f:    
    with open("F://IR//Project Files//inverted_index_unigrams.txt",'r',encoding='utf-8') as f:
        for val in f:
            inverted_list.append(eval(val))

    #storing the inverted index in a dictionary
    for row in inverted_list:        
        inverted_index_dict[row[0]]=row[1]

    #retrieving the dictionary of tokens in each doc
    #with open ("F://IR//Project Files//Stopped and Stemmed Files_Task3//terms_in_docs_stopped.txt",'r',encoding='utf-8') as f2:
        
    #For stemming uncomment this    
    #with open ("F://IR//Project Files//Stopped and Stemmed Files_Task3//terms_in_docs_stemmed.txt",'r',encoding='utf-8') as f2:    
    with open ("F://IR//Project Files//terms_in_docs.txt",'r',encoding='utf-8') as f2:
        for val in f2:
            tokens_in_each_doc.append(eval(val))

    for row in tokens_in_each_doc:
        doc_token_info[row[0]] = row[1]


    with open ("F://IR//Project Files//cacm_rel.txt",'r',encoding='utf-8') as f3:
        for line in f3.readlines():
            l=line.split()
            cacm_rel.append(l)


    f5.write('{:10} {:2} {:40} {:5} {:30} {:10} {:40} {:20}'.format("QueryId", "Q0", "DocumentName", "Rank", "    Score",
                                                      "Relevance", "   Precision", "   Recall") + '\n\n')

    #For stopping uncomment this
    #with open("F://IR//Project Files//Stopped and Stemmed Files_Task3//query_stopped.txt",'r',encoding="utf-8") as fi :
    
    #For stemming uncomment this
    #with open("F://IR//Project Files//Stopped and Stemmed Files_Task3//query_stemmed.txt",'r',encoding="utf-8") as fi :
    with open("F://IR//Project Files//query.txt",'r',encoding="utf-8") as fi :    
        for query in fi:
            count = count + 1
            R = 0
            rel_docs = []
            for row in cacm_rel:
                if count ==int(row[0]):
                    R += 1
                    rel_docs.append(row[2])

            bm25_intermediate_fn(query,avdl,inverted_index_dict,count,R,rel_docs,doc_token_info,f5)
    
           
  


   

   
       
main()
    
