from bs4 import BeautifulSoup
import urllib2


url = "http://www.base-search.net/Search/Results?lookfor=Ebola&type=all&page=1&l=en&oaboost=1&refid=dcpageen.htm"
page=urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
content = soup.find_all("div", class_="ResultsContent")
