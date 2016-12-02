from bs4 import BeautifulSoup
import urllib2
#http://www.base-search.net/Search/Results?lookfor=Ebola&type=all&oaboost=1&ling=1&name=&newsearch=1&refid=dcbasen
#liste = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
out = open("renseignement.txt", 'w')
for i in range(1, 2):
	url = "http://www.base-search.net/Search/Results?lookfor=Ebola&type=all&page="+str(i)+"&l=en&oaboost=1&refid=dcpageen.htm"
	page=urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	content = soup.find_all("div", class_="ResultsContent")
i = 0	
for name in content:
	out.write("\n")
	out.write(str(i)+"\t")
	i += 1
	content1 = name.find_all("div", class_="Metadata")
	for name1 in content1:
		content2 = name1.find_all("div", class_="Item")
		for name2 in content2:
			content3=name2.find("div", class_="ItemLeft_en")
			
			if content3.getText().encode('ascii', 'xmlcharrefreplace') == "Title:":
				
				content4=name2.find("div", class_="ItemRight_en")
				
				out.write(content4.getText().encode('ascii', 'xmlcharrefreplace')+"\t")
				
			if content3.getText().encode('ascii', 'xmlcharrefreplace') == "Author:":
				
				content4=name2.find("div", class_="ItemRight_en")
				auth = content4.find("div",class_="Hidden").getText().encode('ascii', 'xmlcharrefreplace')
				
				auth1 = auth.split(';')
				for j in range(0,len(auth1)):
					out.write(auth1[j]+";")
					print auth1[j],";" 
				#out.write(content4.find("div",class_="Hidden").getText().encode('ascii', 'xmlcharrefreplace'))
			out.write("\t")	
			if content3.getText().encode('ascii', 'xmlcharrefreplace') == "Description:":
				
				
				content4=name2.find("div", class_="ItemRight_en")
				if content4.find("div",class_="Hidden"):
					out.write(content4.find("div",class_="Hidden").getText().encode('ascii', 'xmlcharrefreplace')+"\t")
				
				else:
					out.write(content4.getText().encode('ascii', 'xmlcharrefreplace')+"\t")
				
			if content3.getText().encode('ascii', 'xmlcharrefreplace') == "Year of Publication:":
				
				content4=name2.find("div", class_="ItemRight_en")
				
				out.write(content4.getText().encode('ascii', 'xmlcharrefreplace'))
				
			
		#eliminate duplicate names
		
		   
out.close()


python  1_make_NGrams/main.py   pubmed_result_PTSD_Fanny.xml
     output: InvDict_monograms.txt and InvDict_bigrams.txt

python  2_process_NGrams/main.py  InvDict_monograms.txt
    output: InvDict_monograms.csv
    
#content2[1].find_all("div",class_="ItemRight_en")[0].getText()
