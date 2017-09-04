import os
import re
import nltk
import operator
import math
import collections
from bs4 import BeautifulSoup
path = 'cacm/'

#corpus_folder = "CACMCORPUS-STOPPED"
corpus_folder = "CACMCORPUS"
new_folder_path = os.getcwd()
if not os.path.exists(corpus_folder):
    create_folder = os.makedirs(os.path.join(new_folder_path, corpus_folder))
#print(len(os.listdir(path)))
common = open('common_words.txt', 'r', encoding='utf-8')
stop_words = common.read().splitlines()


def tokenize():
    for filename in os.listdir(path):
    #for i in range(0,1):
        #print(filename)
        filen= os.path.join(os.getcwd(),'cacm',filename) #'CACM-0001.html')
        #print(filename.rstrip('.html'))
        f = open(filen,'r',encoding='utf-8').read()
        soup = BeautifulSoup(f,'lxml')
        for data in soup.find_all('pre'):
            #print('here'+filename)
            rx = re.compile('\[\d+\]|\(|\)|\{|\}|,|/|;|:').sub(' ', data.text).strip()
            rx = re.sub(r'[""]|\*|\+', "", rx)
            rx = re.sub(r'\?',"",rx)
            rx = re.sub(r'(?<!\d)\.|\.(?!\d)', "", rx)
            rx = re.sub(r'(?<!\d)\,|\,(?!\d)', "", rx)
            rx = rx.lower()
            rx = rx.split()
            #print(rx)
        #print('here'+filename)
            for j in rx:
                #print(rx.index(j))
                if(j.__contains__('-')):
                    words = j.split('-')
                    #rx.remove(j)
                    rx[rx.index(j):rx.index(j)+len(words)] = words
                    continue
                if (j.__contains__("\'")):
                        # print(str(j))
                        temp = j
                        j = j.replace("\'", '')
                        # words = j.split()

                        # rx.remove(j)
                        rx[rx.index(temp)] = j

                    #print(rx)
        #print('here'+filename)
        create_file = os.path.join(new_folder_path, corpus_folder, filename.rstrip('.html') + ".txt")
        w = open(create_file, "w+", encoding='utf-8')
        # for normal tokenized corpus

        for j in rx:
                w.write(str(j)+'\n')
            #print(j)
        w.close()

        '''for j in rx:
            if j not in stop_words:
                w.write(str(j) + '\n')
                # print(j)
        w.close()''' # for stop words removal

    #print(str(j)+'\n')

def indexer_unigrams():
    global corpus_folder
    global terms_in_document
    # global tf, df, map_doc_id_name, indexfile,mapper
    # global map_doc_id_name, id_doc, doc_freq, numberoftokens
    # global filen, termfreqfile, docfreqfile
    tf = {}
    df = []
    map_doc_id_name = {}
    doc_freq = {}
    terms_in_document = {}
    #mapper = open("task2-mapper-doc-id-name.txt", "w+", encoding="utf-8")
    #filen = "inverted_index_unigrams.txt"
    #filen = "inverted_index_stemmed_unigrams.txt"
    filen = "inverted_index_stopped_unigrams.txt"

    numberoftokens = {}
    filename = []
    invertedindex_for_ngrams = {}
    #f_number = open("tokenscount.txt", 'w+', encoding="utf-8")
    #f_number = open("tokenscount_stemmed.txt", 'w+', encoding="utf-8")
    f_number = open("tokenscount_stopped.txt", 'w+', encoding="utf-8")

    id_doc = 1
    stemmed_folder = "Stemmed-Corpus"
    path_stemmed = 'Stemmed-Corpus/'
    stopped_folder = 'CACMCORPUS-STOPPED'
    path_stopped = 'CACMCORPUS-STOPPED/'
    # replace by path
    for filename in os.listdir(path_stopped):
        document_number = filename.rstrip('.txt')
        #document_number = filename.rstrip('.html')
        # replace this by commented part
        #fileopen = os.path.join(os.getcwd(), corpus_folder, filename.rstrip('.html') + ".txt")
        fileopen = os.path.join(os.getcwd(), stopped_folder, filename)

        f1 = open(fileopen, "r", encoding="utf-8").read().split()

        f2 = open(fileopen, 'r', encoding='utf-8').read()
        # this the number of tokens within each of the documents
        numberoftokens[document_number] = len(f1)
        # print("the number of tokens: " + str(numberoftokens[document_number]))

        # terms within a document
        # terms_in_document[document_number] = f2.splitlines()

        terms = nltk.ngrams(f1, 1)  # 1 for unigrams
        count_of_bi_grams = nltk.FreqDist(terms)
        # this loop gives inverted index for specified n for ngrams
        for key, val in count_of_bi_grams.items():
            if key[0] in invertedindex_for_ngrams.keys():
                # if docid not in [x[0] for x in invertedindex_for_bigrams.get(key)]:
                invertedindex_for_ngrams[key[0]].append([document_number, val])
            else:
                # print(key[0])
                invertedindex_for_ngrams[key[0]] = [[document_number, val]]
        id_doc = id_doc + 1

    # write inverted index to file
    indexfile = open(filen, "w+", encoding="utf-8")
    for p in invertedindex_for_ngrams.items():
        indexfile.write(str(p) + "\n")
    indexfile.close()

    # number of tokens per document
    for j in numberoftokens.items():
        f_number.write(str(j) + '\n')
    f_number.close()

def query_processing():
    f = open('cacm.query', 'r', encoding='utf-8').read()
    soup = BeautifulSoup(f, 'lxml')

    # without stopped words
    query_write = open("query.txt",'w+',encoding='utf-8')

    # stopped words query file
    #query_write = open("query_stopped.txt", 'w+', encoding='utf-8')

    for data in soup.find_all(['doc']):
        un=data.find('docno')
        un.extract()
        #print(data.text)
        # print('here'+filename)
        rx = re.compile('\[\d+\]|\(|\)|\{|\}|,|/|;|:').sub(' ', data.text).strip()
        rx = re.sub(r'[""]|\*|\+',"",rx)
        rx = re.sub(r'\?',"",rx)
        rx = re.sub(r'(?<!\d)\.|\.(?!\d)', "", rx)
        rx = re.sub(r'(?<!\d)\,|\,(?!\d)', "", rx)
        rx = rx.lower()
        rx = rx.split()
        # print(rx)
        # print('here'+filename)
        for j in rx:
            # print(rx.index(j))
            t = j
            if (j.__contains__('-')):
                words = j.split('-')
                # rx.remove(j)
                rx[rx.index(j):rx.index(j) + len(words)] = words
            if (j.__contains__("\'")):
                #print(str(j))
                temp = j
                j=j.replace("\'",'')
                #words = j.split()

                # rx.remove(j)
                rx[rx.index(temp)] = j
        for j in rx:
            rx[rx.index(j)]= j + " "
                #print(rx)
        #print(rx)

        # for stopped words query processing
        querywords = []
        for word in rx:
            #print(stop_words)
            word = re.sub(r'\s','',word)
            querywords.append(word)
            if word in stop_words:
                print(word)
        resultwords = [word for word in querywords if word not in stop_words]
        result = ' '.join(resultwords)
        #query_write.writelines(result)
        #query_write.write('\n')

        # without stopped words
        query_write.writelines(rx)
        query_write.write('\n')
    query_write.close()
    pass

#####################################################################################

### terms count within each document
invindex={}
indexfile = open('inverted_index_unigrams.txt','r',encoding="utf-8")

tokens=open('tokenscount.txt','r',encoding='utf-8')
dicts_from_file = []

for line in indexfile.readlines():
    dicts_from_file.append(eval(line))
for l in dicts_from_file:
    invindex[l[0]]=l[1]

def get_total_tokens():
    token_count=[]
    total_tokens_doc={}
    for k in tokens:
        token_count.append(eval(k))
    for p in token_count:
        total_tokens_doc[p[0]]=p[1]
    return total_tokens_doc
    #print(total_tokens_doc)

# dicts_from_file now contains the dictionaries created from the text fileprint(dict_from_file)

### get inverted list matchng the query terms
def get_query_match(query_list):
    new_list_matched_terms={}
    t = query_list
    for i in t:
        if i in invindex.keys():
            new_list_matched_terms[i]=invindex[i]

    return new_list_matched_terms

def cosine_similarity_se():
    global q, list
    list = {}
    dict_doc_term = {}
    qid = 1
    query_file = open("query.txt", 'r', encoding='utf-8')
    # to take query from console uncomment this code
    '''while q != "":
        q = input("enter  the query to be searched (!!press enter to exit):")'''

    # to take query from a file one by one
    tot_tokens = get_total_tokens()

    for i in query_file.readlines():
        # print(get_query(q))
        # print(i)
        list = get_query_match(get_query(i))
        len_of_query = len(list)
        # for k in list.items():
        # print(str(k))
        tf = get_normalized_tf(list, tot_tokens)
        idf = get_idf(list)
        tfidf = get_tf_idf(tf, idf)
        # print(tot_tokens)
        dict_doc_term = get_vector_term(tfidf, tot_tokens)
        dict_query_term = get_query_vector(len_of_query, idf)
        cosine_similarity_score(dict_doc_term, dict_query_term, qid, tot_tokens, list)
        # get_document_magnitude(list,tot_tokens)
        qid = qid + 1
    exit()

# get the query terms
def get_query(q):
    lst = []
    terms_in_query=[]
    query_dict={}
    lst.append(q)
    for i in lst:
        terms_in_query= i.split()
    return terms_in_query
        #get_inverted_list(terms_in_query)

        #get_inverted_list(terms_in_query)

'''def get_inverted_list(tiq):
    for j in indexfile.readlines():
        pass
    pass'''

# normalize the tf

def get_normalized_tf(query_dict,tot_tokens):
    global doc_normalized_tf
    doc_normalized_tf={}
    temp={}

    for j in query_dict.keys():
        #print(j)
        for i in query_dict[j]:
            #print(tot_tokens[i[0]])

            docs = tot_tokens.get(i[0])
            #print(docs)
            #doc_normalized_tf[j]=[[i[0],(i[1]/docs)]]
            #a = i[0]
            #b= i[1]
            #print(i[0])
            if j in doc_normalized_tf.keys():
                doc_normalized_tf[j].append([i[0],i[1]/docs])
            else:
                doc_normalized_tf[j]=[[i[0],i[1]/docs]]
    #print(doc_normalized_tf)
    return doc_normalized_tf

### calculate idf

def get_idf(list):
    idf={}
    total_docs=3204
    idf_formula=0
    for i in list.keys():
        num_of_doc=len(list.get(i))
        #print(num_of_doc)
        idf_formula = 1 + math.log(total_docs / num_of_doc)
        if i in idf.keys():
            idf[i].append(idf_formula)
        else:
            idf[i]=idf_formula
    #print(idf)
    return idf

### calculate tf*idf for the documents matching the query terms

def get_tf_idf(tf,idf):
    tf_idf={}
    for i in tf.keys():
        for j in tf[i]:
            #print(j)
            tfidf = float(j[1] * idf[i])
            if i in tf_idf.keys():

                tf_idf[i].append([j[0],tfidf])
            else:
                tf_idf[i]=[[j[0],tfidf]]
            #print(j[1])
    #print(tf_idf)
    return tf_idf

### get the term - document vector

def get_vector_term(tfidf,tot_tokens):
    vector={}

    #print(len(tot_tokens.items()))
    for j in tfidf.keys():
        for i in tot_tokens.keys():
            '''for k in tfidf.get(j):
                print(k[0])'''
            if i not in [x[0] for x in tfidf[j]]:
                #print(tfidf[j][0])
                tfidf[j].append([i, 0])
            else:
                continue
    #print(tfidf)
    return tfidf

            #print(tfidf[j])
            #vector[i].append()

### get the query vector

def get_query_vector(length,idf):
    #print(length)
    query_vector={}
    for i in idf.keys():
        tfidf_query= idf[i]*(1/length)
        if i in query_vector.keys():
            query_vector[i].append(tfidf_query)
        else:
            query_vector[i]=tfidf_query
    #print(query_vector)
    return query_vector

### sorting helper function for natural sorting

def sorted_nicely(l, key):
    #sorting the docs
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda item: [ convert(c) for c in re.split('([0-9]+)', key(item)) ]
    return sorted(l, key = alphanum_key)

### sorting the dictionary's values based on the document ids

def get_sorted_doc_term(doc):
    new_doc={}

    for i in doc.keys():
        doc[i] = sorted_nicely(doc[i],operator.itemgetter(0))
        #doc[i]=sorted(doc[i],key=operator.itemgetter(0))

    #print(doc)
    return doc

### sorting results

def get_sorted_doc_term_v2(doc):
    #
    # print(doc)

    doc = collections.OrderedDict(sorted_nicely(doc,operator.itemgetter(0)))
        #doc[i]=sorted(doc[i],key=operator.itemgetter(0))

    #print(doc)
    return doc

### calculate the document magnitude for documents matching the query terms

def get_document_magnitude(list,tot_tokens):
    #print(list)
    doc_magni={}
    t_in_docs=[]
    tinDocs={}
    idf={}
    normalized_tf=get_normalized_tf(invindex,tot_tokens)

    '''f = open('terms_in_document.txt','r',encoding='utf-8')
    for i in f.readlines():
        t_in_docs.append(eval(i))'''
    '''for l in t_in_docs:
        tinDocs[l[0]]=l[1]'''
    for i in invindex.keys():
        for j in invindex[i]:
            if j[0] in tinDocs.keys():
                tinDocs.get(j[0]).append(i)
            else:
                tinDocs[j[0]]=[i]

    for j in invindex.keys():
        idf[j] = 1 + math.log(3204 / len(invindex[j]))
    tf_term=1
    for i in list.keys():
        for k in list[i]:
                    terms = tinDocs[k[0]]
                    for l in terms:
                        #print(str(l)+" : "+str(idf[l])+'\n')
                        idf_term=idf[l]
                        #print(k[0])

                        '''if k[0] in [j[0] for j in invindex[l]]:
                                 print(str(k[0] + "\n"))
                                 print(str(j[0])+" : "+str(j[1]))
                                 tf_term = j[1]/tot_tokens[k[0]]'''
                        term=normalized_tf[l]
                        for o in term:
                            if k[0]==o[0]:
                                tf_term=o[1]
                        #print(tf_term)
                        if k[0] in doc_magni.keys():
                                doc_magni[k[0]]=doc_magni[k[0]]+ math.pow(tf_term*idf_term,2)
                        else:
                                #print(k[0])
                                doc_magni[k[0]]=math.pow(tf_term * idf_term,2)
    doc_magni=get_vector_v2(doc_magni,tot_tokens)
    #doc_magni=get_sorted_doc_term_v2(doc_magni)
    #print(doc_magni)
    return doc_magni

def get_vector_v2(doc_magni,tot_tokens):
    for i in tot_tokens.keys():
        if i not in doc_magni.keys():
            doc_magni[i]=0
    return doc_magni

### Calculating cosine similarity scores for the documents

def cosine_similarity_score(doc,query,qid,tot_tokens,list):
    cosine_sim=collections.OrderedDict()
    tfidf={}
    q_doc_mag=collections.OrderedDict()
    doc_magnitude=collections.OrderedDict()
    tfidf=get_sorted_doc_term(doc)
    '''for j in query.items():
        print(j)'''

    for i in tfidf.keys():
        for j in tfidf[i]:
            #print(i)
            for k in query.keys():
                if k==i:
                    if j[0] in cosine_sim.keys():
                        cosine_sim[j[0]]=float(cosine_sim[j[0]]+j[1]*query[k])#/math.pow(query[k],2)
                    else:
                        cosine_sim[j[0]]=float(j[1]*query[k])
                    '''if j[0] in doc_magnitude.keys():
                        doc_magnitude[j[0]] = doc_magnitude[j[0]] + (math.pow(j[1],2))
                    else:
                        doc_magnitude[j[0]] = float(math.pow(j[1],2))'''
    #print(cosine_sim)
    #tf_idf_se(cosine_sim)
    doc_magnitude=get_document_magnitude(list,tot_tokens)
    #print(doc_magnitude)
    query_magnitude = 0
    for k in query.keys():
        query_magnitude=query_magnitude+ float(math.pow(query[k],2))
    query_magnitude=math.sqrt(query_magnitude)
    #print(query_magnitude)
    print("Top 100 Search Results :" +'\n')
    for i in doc_magnitude.keys():
        if i not in q_doc_mag.keys():
            q_doc_mag[i]=math.sqrt(doc_magnitude[i]) * query_magnitude
        else:
            q_doc_mag[i]= math.sqrt(doc_magnitude[i]) * query_magnitude
    #print(q_doc_mag)
    for k in cosine_sim.keys():
        #print(k)
        if q_doc_mag[k]==0:
            cosine_sim[k]=0
        else:
            cosine_sim[k]=float(cosine_sim[k]/q_doc_mag[k])

    top_100_documents=sorted(cosine_sim.items(),key=operator.itemgetter(1),reverse=True)
    print(top_100_documents)
    new_folder_path = os.getcwd()

    if not os.path.exists("CosineSimilarity"):
        create_folder = os.makedirs(os.path.join(new_folder_path, "CosineSimilarity"))

    fname="cosine_sim_SE"+"_Query"+str(qid)+".txt"
    create_file = os.path.join(new_folder_path, "CosineSimilarity", fname + ".txt")

    file = open("Cosine_Results.txt",'a+',encoding='utf-8')
    c=1
    #file.write('{:10} {:2} {:40} {:5} {:30} {:10}'.format("QueryId","Q0","DocumentName","Rank","    Score","SystemName")+'\n\n')
    for i in top_100_documents[0:100]:
        #if i in [x[0] for x in map]:
        #for j in map:
            #if i[0]==j[0]:
        file.write(
            '{:10} {:3} {:40} {:5} {:30}'.format("" + str(qid), "" + "Q0", "" + str(i[0]), "" + str(c), "" + str(i[1]),
                                                 ) + '\n')

        #file.write('{:10} {:2} {:40} {:5} {:30} {:10}'.format(""+str(qid),"Q0",""+str(i[0]),""+str(c),""+str(i[1]),"Shantanu-SYS-001")+'\n')
                #file.write('Q0'+"\t"+str(j[1]+'\t          '+str(i[1]))+'\t              '+"Shantanu"+'\n')
                #print(str(j[1])+'\t'+str(i[1]))

            #else:
            #    continue
        c = c + 1

def tf_idf_main():
    global q, list
    list = {}
    dict_doc_term = {}
    qid = 1
    query_file = open("query.txt", 'r', encoding='utf-8')
    # to take query from console uncomment this code
    '''while q != "":
        q = input("enter  the query to be searched (!!press enter to exit):")'''

    # to take query from a file one by one
    tot_tokens = get_total_tokens()

    new_folder_path = os.getcwd()
    if not os.path.exists("TDIDF-Latest"):
        create_folder = os.makedirs(os.path.join(new_folder_path, "TDIDF-Latest"))

    fname = "tf_idf_ranking"
    create_file = os.path.join(new_folder_path, "TDIDF-Latest", fname + ".txt")

    file = open("TFIDF_Results.txt", 'a+', encoding='utf-8')

    for i in query_file.readlines():
        # print(get_query(q))
        # print(i)
        list = get_query_match(get_query(i))
        len_of_query = len(list)
        # for k in list.items():
        # print(str(k))
        tf = get_normalized_tf(list, tot_tokens)
        idf = get_idf(list)
        tfidf = get_tf_idf(tf, idf)
        # print(tot_tokens)
        dict_doc_term = get_vector_term(tfidf, tot_tokens)
        dict_query_term = get_query_vector(len_of_query, idf)
        tf_idf_se(dict_doc_term, dict_query_term, qid, tot_tokens, list,file)
        # get_document_magnitude(list,tot_tokens)
        qid = qid + 1
    exit()


def tf_idf_se(doc,query,qid,tot_tokens,list,file):
    cosine_sim = collections.OrderedDict()
    tfidf = {}
    q_doc_mag = collections.OrderedDict()
    doc_magnitude = collections.OrderedDict()
    tfidf = get_sorted_doc_term(doc)
    '''for j in query.items():
        print(j)'''

    for i in tfidf.keys():
        for j in tfidf[i]:
            # print(i)
            for k in query.keys():
                if k == i:
                    if j[0] in cosine_sim.keys():
                        cosine_sim[j[0]] = float(cosine_sim[j[0]] + j[1] * query[k])  # /math.pow(query[k],2)
                    else:
                        cosine_sim[j[0]] = float(j[1] * query[k])

    top_100_documents = sorted(cosine_sim.items(), key=operator.itemgetter(1), reverse=True)
    print(top_100_documents)
    #new_folder_path = os.getcwd()
    #if not os.path.exists("TDIDF-Latest"):
    #    create_folder = os.makedirs(os.path.join(new_folder_path, "TDIDF-Latest"))

    #fname = "tf_idf_SE" + "_Query" + str(qid) + ".txt"
    #create_file = os.path.join(new_folder_path, "TDIDF-Latest", fname + ".txt")

    #file = open(create_file, 'w+', encoding='utf-8')
    c = 1
    #file.write('{:10} {:2} {:40} {:5} {:30} {:10}'.format("QueryId", "Q0", "DocumentName", "Rank", "    Score",
    #                                                      "SystemName") + '\n\n')
    for i in top_100_documents[0:100]:
        # if i in [x[0] for x in map]:
        # for j in map:
        # if i[0]==j[0]:
        file.write(
            '{:10} {:3} {:40} {:5} {:30}'.format("" + str(qid),""+"Q0" ,"" + str(i[0]), "" + str(c), "" + str(i[1]),
                                                       ) + '\n')
        # file.write('Q0'+"\t"+str(j[1]+'\t          '+str(i[1]))+'\t              '+"Shantanu"+'\n')
        # print(str(j[1])+'\t'+str(i[1]))

        # else:
        #    continue
        c = c + 1
    pass
def stemmed_corpus():
    i=1
    #f1 = open('cacm_stem.txt','r',encoding='utf-8')
    f1 = open("cacm_stem.txt",'r',encoding='utf-8').readlines()
    file = ''.join(f1)
    lines = file.split('#')[1:]
    #print(lines)
    if not os.path.exists("Stemmed-Corpus"):
        create_folder = os.makedirs(os.path.join(new_folder_path, "Stemmed-Corpus"))

    for k in lines:
        word=k.split()
        print(word[0])
        filename = word[0]
        content = word[1:]
        create_file = os.path.join(new_folder_path, "Stemmed-Corpus", "CACM-"+filename+ ".txt")

        p = open(create_file, 'w+', encoding='utf-8')

        for j in content:
            p.write(str(j)+'\n')

    #i = i + 1
    # Do stuff with data
    '''for result in re.findall('\#(.*?)\#', f.read(), re.DOTALL):
        print(str(result) + '\n')'''

    pass

# for implementing the search engine uncomment accordingly

#cosine_similarity_se()
tf_idf_main()
#query_processing()
#tokenize()
#stemmed_corpus()
#indexer_unigrams()