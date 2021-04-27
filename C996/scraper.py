from bs4 import BeautifulSoup
import requests
import csv


source = requests.get('https://www.census.gov/programs-surveys/popest.html').text

soup = BeautifulSoup(source, 'lxml')

body = soup.findAll('a')

uniqueUrls = set()
externalUrls = set()


def isExternalLink(href):
    if(href[0:22] == 'https://www.census.gov'):
        externalUrls.add(stripSlash(href))
    else:
        uniqueUrls.add(stripSlash(href))


def stripSlash(href):
    if(href[len(href)-1] == '/'):
        return href[0:len(href)-1]
    else:
        return href


for i in range(len(body)-1):
    url = body[i].get('href')
    if(url is not None):
        if(url[0] == '/'):
            url = 'https://www.census.gov'+url
            isExternalLink(url)
        elif (url[0:8] == 'https://'):
            isExternalLink(url)


# writes unique urls to csv
def writeToCsv(setOfUrls):
    for url in setOfUrls:
        csv_writer.writerow([str(url)])


csv_file = open('urls_from_page'+'.csv', 'w')

csv_file = csv_file
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Internal Total '+str(len(uniqueUrls))])


writeToCsv(uniqueUrls)
csv_writer.writerow(['\nExternal Total '+str(len(externalUrls))])

writeToCsv(externalUrls)

csv_file.close()
