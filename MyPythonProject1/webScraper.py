#web scraper project
'''import requests

url = "http://www.linkedin.com"
response = requests.get(url)
print(response)
print(response.content)'''
#########################################################
'''import requests

url = "http://www.pixelford.com"
response = requests.get(url)
print(response)
#print(response.content)
#when pages becomes unresponsive then we use the utils.default_headers() to get UserAgent details
#print(requests.utils.default_headers())
response=requests.get(url,headers={'user-agent':"practice_webscraper"})
print(response.content)'''

#####################################
import requests
from bs4 import BeautifulSoup 

#url = "http://www.pixelford.com"
#response = requests.get(url,headers={"UserAgent":"ScraperPractice"})
#html = response.content
#soup = BeautifulSoup(html,"html.parser")
#h_tags= soup.find_all('h4')
#for h_tag in h_tags:
#    print(h_tag.get_text())

#headings = list(filter(lambda h_tag:h_tag.get_text(),h_tags))
#print(headings)
#headings2= list(map(lambda h_tag:h_tag.get_text(),h_tags))
#print(headings2)
################################
url = "https://pixelford.com/blog/"
#print(requests.utils.default_headers())
#User-Agent': 'python-requests/2.32.3', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'
htmldate = requests.get(url,headers={'User-Agent': 'Practice', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}).content
#print(htmldate)
soup1= BeautifulSoup(htmldate,"html.parser")
dates=soup1.find_all('time',class_='entry-time')
#for data in dates:
#    print(data.get_text())
dateslist=list(map(lambda date:date.get_text(),dates))
#dateslist2=list(filter(lambda data:data.get_text(),dates))
print(dateslist)

