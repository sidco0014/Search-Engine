import os
import sys
import math
import operator
import collections

# for lucene results obtained from normal corpus
#eval_write = open('eval_results_lucene.txt', 'w+', encoding='utf-8')
#p_at_k = open('eval_results_lucene_p_at_k.txt','w+',encoding='utf-8')

# for tfidf results obtained from normal corpus
#eval_write = open('eval_results_tfidf.txt', 'w+', encoding='utf-8')
#p_at_k = open('eval_results_tfidf_p_at_k.txt','w+',encoding='utf-8')

# for lucene results obtained from stopped corpus
#eval_write = open('eval_results_lucene_stopped.txt', 'w+', encoding='utf-8')
#p_at_k = open('eval_results_lucene_stopped_p_at_k.txt','w+',encoding='utf-8')

# for cosine results obtained from normal corpus
eval_write = open('eval_results_cosine.txt', 'w+', encoding='utf-8')
p_at_k = open('eval_results_cosine_p_at_k.txt','w+',encoding='utf-8')

def evaluation():

    # for lucene results normal
    #results = open("Lucene_Results.txt",'r',encoding='utf')

    # for lucene results stopped
    #results = open("Lucene_Results_Stopped.txt", 'r', encoding='utf')

    # for tfidf results normal
    #results = open("Lucene_Results_Stopped.txt", 'r', encoding='utf')

    # for tfidf results normal
    results = open("Cosine_Results.txt", 'r', encoding='utf')

    rel_judge = open("cacm.rel",'r',encoding='utf-8')
    judge=[]
    result = []
    #q = 1
    #for i in results.readlines():
    for j in rel_judge.readlines():
        l = j.split()
        judge.append(l)
    #print(judge)
    for i in results.readlines():
        l=i.split()
        result.append(l)
    #print(result)
    relevant_files = collections.OrderedDict()
    relevant_docs_query = collections.OrderedDict()

    i=1
    relevant_docs_query={}
    while (i<=64):
        if str(i) in [x[0] for x in judge]:
            for j in judge:
                if int(j[0])==i:
                    #print(j[0])
                    if j[0] not in relevant_docs_query:
                        relevant_docs_query[j[0]]=[j[2]]
                    else:
                        relevant_docs_query[j[0]].append(j[2])
                    if j[0] not in relevant_files.keys():
                        relevant_files[j[0]]=1
                    else:
                        relevant_files[j[0]]+=1
        else:
            if str(i) not in relevant_docs_query.keys():
                relevant_docs_query[str(i)]="null"
                relevant_files[str(i)]="null"
        i=i+1

    '''while(i<=64):
        if str(i) in relevant_docs_query.keys():
            continue
        else:
            relevant_docs_query[str(i)]="null"
        i=i+1
    #for i in result:
    qid=1
    print(relevant_docs_query[str(qid)])
    while (qid<=64):
        for i in result:
            if i[0]==str(qid):

                if i[2] in relevant_docs_query[str(qid)]:
                    result[qid].append('R')
                else:
                    result[qid].append('NR')
        qid=qid+1
    print(result)'''
    #print(relevant_docs_query['56'])
    for k in result:
        #print(len(k))
        if relevant_docs_query[k[0]]==str('null'):
                k.append('null')

        else:
            if k[2] in relevant_docs_query[k[0]]:
                k.append('R')
            else:
                k.append('NR')
    #print(len(relevant_docs_query))
    q = 1
    r = 0
    nr = 0
    retrieved = 0

    precision(result,relevant_docs_query,r,nr,retrieved,q)
    #mrr(result,relevant_docs_query)
    #print(result)


def precision(result,relevant_docs_query,r,nr,retrieved,q):

    prec = 0
    seen=[]
    c=1
    avgprec=0
    map=0
    mrr=0
    rr=0
    first='f'
    for i in result:
            if c==101:
                c = 1
                r = 0
                nr = 0
                retrieved = 0
                prec = 0
                avgprec=0
                first='f'
                rr=0
            if c==100:
                avgprec = prec/len(relevant_docs_query[str(i[0])])

                #print(str(i[0])+" : "+str(prec))
                map = map + avgprec
                mrr = rr + mrr

            if relevant_docs_query[i[0]]== str('null'):
                i.append(0)
                i.append(0)
            else:
                retrieved = retrieved + 1
                if i[5]=='R':
                    if first == 'f':
                        first = 't'
                        rr= 1/int(i[3])
                    r = r + 1
                    prec = (prec + (r/retrieved))
                    i.append(r/retrieved)
                    i.append(r/len(relevant_docs_query[str(i[0])]))
                else:

                    i.append(r/retrieved)
                    i.append(r/len(relevant_docs_query[str(i[0])]))
            if str(i[3]) == '5':
                p_at_k.write("Precision for query "+str(i[0]) + " @5 : "+str(i[6])+"   ")
                print(str(i[0]) + " : " + str(i[6]))
            if str(i[3]) == '20':
                p_at_k.write("Precision for query "+str(i[0]) + " @20 : " + str(i[6])+'\n')
                print(str(i[0]) + " : " + str(i[6]))

            c = c + 1
    print(map/52)
    print('\n')
    print(mrr/52)
    m = map/52
    mr = mrr/52

    for j in result:
        eval_write.write(
            '{:5} {:5} {:25} {:5} {:20} {:4} {:20} {:15}'.format("" + str(j[0]), "" + str(j[1]), "" + str(j[2]), "" + str(j[3]),
                            "" + str(j[4]),"" + str(j[5]),"" + str(j[6]),""+ str(j[7]))+'\n')
    eval_write.write("\n Mean Average Precision : "+ str(m) +"\n Mean Reciprocal Rank : "+ str(mr))
        #eval_write.write(str(j)+'\n')
    #print(result)
        #list = relevant_docs_query[k[0]]
        #print(str(k[0]) + " " +str(list))
        #print(list)
        #if k[2] in :
        #print('here')
    #print(len(result))
    #eval_write.write()
    #print(relevant_docs_query)
    #print(relevant_files)



evaluation()