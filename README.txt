The ZIP contains the following :
=================================

A) 6 souce codes:
-------------------
1) HW3.java (Lucene Search Engine)
-- This source code will give the lucene score and rank for all the documents having the query terms in them


2) Indexer.py 
-- This source code contains codes for indexing, tokenization, query processing, tfidf search engine, cosine similarity search engine, stemming and stopping.
-- This code generates the following files, depending on the part of code implemented :
	i)		Inverted Index file for normal corpus, stemmed corpus and stopped corpus
	ii)		Tokens count file for normal corpus, stemmed corpus and stopped corpus
	iii)	Query file for normal corpus and stopped corpus
	iv)		tfidf search engine top 100 results for all 64 queries
	v) 		Cosine similarity search engine top 100 results for all 64 queries
	vi)		Corpus folder fo normal, stemmed and stopped implementation


3) tfidf_calc.py
-- This source code generates inverted_index with tfidf score of each document for each term and a file that provides a list of terms present in each document for the given corpus.


4) query_expansion.py
-- Generates a file that consists of expanded queries formed using Rocchio Algorithm.


5) PrecisionRecall.py
-- Calculates the evaluation measures for output files of tfidf search engine, cosine similarity search engine, lucene search engine and lucene search engine for stopped corpus.


6) BM25.py
-- Generates the top 100 results for a given corpus and a set of query based on the BM25 score. Follow the commented instructions in the py file. 




B) 42 files:
-----------------------
1)		bm25_expanded_query_results.txt 
2) 		bm25_general_corpus_results.txt
3)		bm25_stemmed_corpus_results.txt
4) 		bm25_stopped_corpus_results.txt	
5)		Cosine_Results.txt
6)		eval_results_cosine.txt
7)		eval_results_cosine_p_at_k.txt
8)		eval_results_lucene.txt	
9)		eval_results_lucene_p_at_k.txt
10) 	eval_results_lucene_stopped.txt
11)		eval_results_lucene_stopped_p_at_k.txt
12)		eval_results_tfidf.txt
13)		eval_results_tfidf_p_at_k.txt
14) 	inverted_index_stemmed_unigrams.txt
15)		inverted_index_stopped_unigrams.txt
16)		inverted_index_unigrams.txt      // It is the inverted index for the general corpus
17)		Lucene_Results.txt
18)		Lucene_Results_Stopped.txt
19)		Precision_at_K_BM25_general.txt
20) 	Precision_at_K_BM25_stemmed.txt
21)		Precision_at_K_BM25_stopped.txt
22)		query.txt
23)		query_stopped.txt
24)		Relevant_Docs_for_each_query.txt
25)		terms_in_docs.txt				//	For general inverted index
26)		terms_in_docs_stemmed.txt		//	For inverted index of stemmed corpus
27)		terms_in_docs_stopped.txt		//	For inverted index of stopped corpus
28)		tfidf_invindex.txt				//	inverted_index with tfidf score of each document for each term 
29)		TFIDF_Results.txt
30)		tokenscount.txt					//	For general inverted index
31)		tokenscount_stemmed.txt			//	For inverted index of stemmed corpus
32)		tokenscount_stopped.txt			//	For inverted index of stopped corpus
33)		cacm.query
34)		cacm_rel.txt
35)		cacm_stemmed.query.txt
36)		cacm_stem.txt
37)		common_words.txt
38)		CACMCORPUS folder				// General corpus
39)		CACMCORPUS-STOPPED folder		// Stopped corpus
40)		Stemmed-Corpus folder			// Stemmed Corpus
41) 	Project_Report.pdf
42)		README.txt

SETUP:
----------------
1) Check if python 3.0 + is installed on the machine which you are going to operate.

2) Create a python new project and just copy paste all the sourse codes provided to you in the ZIP to the python shell.

3) Download and install the following external libraries using the pip command in the CommandPrompt of the script file present in your python folder.
	a)import operator
	b)import requests
	c)from collections
	d)import re
	e)from bs4 import BeautifulSoup
	f)import string
	g)import urlib
	h)import nltk
	i)from operator import itemgetter

   for example: ( pip install nltk )
 
    Please Note: You will need to download all the packages of the NLTK library by using the following two commands on your shell. Failing to do so will not execute the code.
	
	import nltk
	nltk.download('all')
 
4) For output, go to the python (IDLE 3.6 64 bit) and either press (fn + F5) or click on run tab and run module to execute the python code.
   You can also double click the .py file to execute.
   

IMPLEMENTATION:
--------------------
1) Run the indexer.py file first , modify the paths for files and folders accordingly (commented part in the code)
2) Firstly run the function tokenize() then indexer() and lastly query_processing()
3) Use can also call stemmed_corpus() to get the stemmed output
4) There are functions for cosine similarity, tf-idf etc so run the functions for the respective outputs
5) Run tfidf_calc.py
6) Run BM25.py
7) Run query_expansion.py
8) Run HW3.java in netbeans for the Lucene Search Engine ouput
9) Run PrecisionRecall.py

NOTES:
-----------
1) The cosine similarity search engine takes about 40-50 mins to run for 64 queries due to complex coding
2) The tf-idf search engine takes about 6-8 mins to run for 64 queries
3) Rest all files take moderate amount of time.
4) Open the files in Notepad++ to view the output correctly.


