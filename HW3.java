/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package lucenesearche;

/**
 *
 * @author shantanu
 */
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Formatter;
import java.util.Scanner;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class HW3 {
    private static Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_47);
    private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);

    private IndexWriter writer;
    private ArrayList<File> queue = new ArrayList<File>();

    public static void main(String[] args) throws IOException {
	System.out
		.println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");

	String indexLocation = null;
	BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
	String s = br.readLine();

	HW3 indexer = null;
	try {
	    indexLocation = s;
	    indexer = new HW3(s);
	} catch (Exception ex) {
	    System.out.println("Cannot create index..." + ex.getMessage());
	    System.exit(-1);
	}
        String query1,query2,query3,query4;
                query1="Lucene_Results_Stopped.txt";
                query2="Lucene_Q2_top100.txt";
                query3="Lucene_Q3_top100.txt";
                query4="Lucene_Q4_top100.txt";
                
        File luceneFile = new File(query1); // change filename for each query
        int query_id;
                
	// ===================================================
	// read input from user until he enters q for quit
	// ===================================================
	while (!s.equalsIgnoreCase("q")) {
	    try {
		System.out
			.println("Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
		System.out
			.println("[Acceptable file types: .xml, .html, .html, .txt]");
		s = br.readLine();
		if (s.equalsIgnoreCase("q")) {
		    break;
		}

		// try to add file into the index
		indexer.indexFileOrDirectory(s);
	    } catch (Exception e) {
		System.out.println("Error indexing " + s + " : "
			+ e.getMessage());
	    }
	}

	// ===================================================
	// after adding, we always have to call the
	// closeIndex, otherwise the index is not created
	// ===================================================
	indexer.closeIndex();

	// =========================================================
	// Now search
	// =========================================================
	IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
		indexLocation)));
	IndexSearcher searcher = new IndexSearcher(reader);
	//TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);
        Formatter f = new Formatter();
        
	s = "";
        File file1 = new File("C:\\Users\\shantanu\\Downloads\\NetBeansProjects\\LuceneSearchE\\src\\lucenesearche\\query_stopped.txt");
        ScoreDoc[] hits;
	    try {
                BufferedReader b = new BufferedReader(new FileReader(file1)); 
                query_id = 1;
                FileInputStream fis = new FileInputStream("C:\\Users\\shantanu\\Downloads\\NetBeansProjects\\LuceneSearchE\\src\\lucenesearche\\query_stopped.txt");
                Scanner scanner = new Scanner(fis);


                luceneFile.createNewFile();
                FileWriter writer = new FileWriter(luceneFile);
                
                while (scanner.hasNextLine()){
                String line;    
                    
                //line = b.readLine();
		line = scanner.nextLine();
                if(line == null)
                    break;
                
                System.out.println(b.readLine());
		//s = br.readLine();
                if (s.equalsIgnoreCase("q")) {
		    break;
		}
                TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);
		Query q = new QueryParser(Version.LUCENE_47, "contents",
			sAnalyzer).parse(line);
		searcher.search(q, collector);
                //System.out.println(searcher);
		
		hits = collector.topDocs().scoreDocs;
                
		System.out.println(hits.length);
                
                // 4. display results
                 // change this for new query 
                //writer.write(String.format("%-10s %-10s %-80s %-10s %-40s %-20s","Query ID","Q0","Document Name","Rank","Cosine Similarity Score","System Name\n"));
		System.out.println("Found " + hits.length + " hits.");
                //System.out.println(f.format("%-10s %-10s %-80s %-10s %-40s %-20s","Query ID","Q0","Document Name","Rank","Cosine Similarity Score","System Name"));
		for (int i = 0; i < hits.length; ++i) {
                    Formatter fmt = new Formatter();
		    int docId = hits[i].doc;
		    Document d = searcher.doc(docId);
                    //System.out.println(d.get("filename"));
		    //System.out.println((i+1) +". " + d.get("path")+" "+ hits[i].score);
                    String a = d.get("filename");
                    String parts=a.substring(0,a.indexOf('.'));
                    //System.out.println(parts);
                    
                    writer.append(String.format("%-10s %-10s %-30s %-10s %-30s",query_id,"Q0", parts,(i + 1),hits[i].score));
                    writer.append('\n');
                    writer.flush();
                    //System.out.println(fmt.format("%-10s %-10s %-80s %-10s %-40s %-20s",""+query_id,"Q0",""+d.get("path"),""+(i + 1),""+hits[i].score,"Shantanu-SYS-001"));
		}
                
                    
		// 5. term stats --> watch out for which "version" of the term
		// must be checked here instead!
		/*Term termInstance = new Term("contents", s);
		long termFreq = reader.totalTermFreq(termInstance);
		long docCount = reader.docFreq(termInstance);
		System.out.println(s + " Term Frequency " + termFreq
			+ " - Document Frequency " + docCount);*/
                query_id+=1;
                }
            writer.close();
            } catch (Exception e) {
		System.out.println("Error searching " + s + " : "
			+ e.toString());
		//break;
	    }

	

    }

    /**
     * Constructor
     * 
     * @param indexDir
     *            the name of the folder in which the index should be created
     * @throws java.io.IOException
     *             when exception creating index.
     */
    HW3(String indexDir) throws IOException {

	FSDirectory dir = FSDirectory.open(new File(indexDir));

	IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,
		sAnalyzer);

	writer = new IndexWriter(dir, config);
    }

    /**
     * Indexes a file or directory
     * 
     * @param fileName
     *            the name of a text file or a folder we wish to add to the
     *            index
     * @throws java.io.IOException
     *             when exception
     */
    public void indexFileOrDirectory(String fileName) throws IOException {
	// ===================================================
	// gets the list of files in a folder (if user has submitted
	// the name of a folder) or gets a single file name (is user
	// has submitted only the file name)
	// ===================================================
	addFiles(new File(fileName));

	int originalNumDocs = writer.numDocs();
	for (File f : queue) {
	    FileReader fr = null;
	    try {
		Document doc = new Document();

		// ===================================================
		// add contents of file
		// ===================================================
		fr = new FileReader(f);
		doc.add(new TextField("contents", fr));
		doc.add(new StringField("path", f.getPath(), Field.Store.YES));
		doc.add(new StringField("filename", f.getName(),
			Field.Store.YES));

		writer.addDocument(doc);
		System.out.println("Added: " + f);
	    } catch (Exception e) {
		System.out.println("Could not add: " + f);
	    } finally {
		fr.close();
	    }
	}

	int newNumDocs = writer.numDocs();
	System.out.println("");
	System.out.println("************************");
	System.out
		.println((newNumDocs - originalNumDocs) + " documents added.");
	System.out.println("************************");

	queue.clear();
    }

    private void addFiles(File file) {

	if (!file.exists()) {
	    System.out.println(file + " does not exist.");
	}
	if (file.isDirectory()) {
	    for (File f : file.listFiles()) {
		addFiles(f);
	    }
	} else {
	    String filename = file.getName().toLowerCase();
	    // ===================================================
	    // Only index text files
	    // ===================================================
	    if (filename.endsWith(".htm") || filename.endsWith(".html")
		    || filename.endsWith(".xml") || filename.endsWith(".txt")) {
		queue.add(file);
	    } else {
		System.out.println("Skipped " + filename);
	    }
	}
    }

    /**
     * Close the index.
     * 
     * @throws java.io.IOException
     *             when exception closing
     */
    public void closeIndex() throws IOException {
	writer.close();
    }
}
