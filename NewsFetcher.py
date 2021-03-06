#!/usr/bin/python
# -*- coding: utf-8 -*-

# Made some imports I'll need later on.
import os
import time
import facepy
import requests
import ast
import unicodedata
from TaskThreaderModule import *
from bs4 import BeautifulSoup
from six.moves import urllib
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


# Setting global variables for Facebook share function.
token = os.environ.get('facebook_token')
graph = facepy.GraphAPI(token, version=2.9)

# A simple function to get number of shares on Facebook of a url using social shares module.
def facebookShares(url):
    global token
    global graph
    response = graph.get('?og_object&share_count&id=' + str(link) + '&fields=og_object,engagement&access_token=' + str(token))
    return response["engagement"]["share_count"]

# The 'stories' list will store all news stories once scraping is complete.
stories = []

# Using this function to display data saved as dicts to the list 'stories'.
def displayStories():
    global stories
    for i in range(0, len(stories)):
        print
        print stories[i]['headline']
        print stories[i]['url']
        print stories[i]['shares']
        print ''


# A clean function that scrapes Fox News.com
def scrapeFoxNews():
    source = "Fox News"
    global foxnewslist
    foxnewslist = []
    foxnews = 'http://www.foxnews.com/'
    r = requests.get(foxnews)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    for i in range(0, 15):
        foundstories = soup.find_all('article', class_='article story-'
                + str(i))
        for data in foundstories:
            htmlatag = data.find('h2', class_='title').find('a')
            headline = htmlatag.getText()
            url = htmlatag.get('href')
            d = {"source": source, 'headline': headline, 'url': url}
            foxnewslist.append(d)


# A function that scrapes the Daily Wire.
def scrapeDailyWire():
    source = "Daily Wire"
    global dailywirelist
    dailywirelist = []
    dailywire = 'https://www.dailywire.com/'
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options, executable_path='C:\\Users\\Seth\\Documents\\geckodriver\\geckodriver.exe')
    driver.get(dailywire)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    for h3 in soup.find_all('article',
                            class_='article-teaser f-deflate-1-s fx ai-c mb-3-s mb-4-ns'
                            ):
        if h3.find("a", text=True) != None:
            blah = h3.find('a', text=True)
            headline = blah.text
            url = 'https://www.dailywire.com' + blah['href']
            d = {"source": source, 'headline': headline, 'url': url}
            dailywirelist.append(d)
    driver.quit()


# A function that scrapes The Gateway Pundit.
def scrapeTheGatewayPundit():
    source = "Gateway Pundit"
    global gatewaypunditlist
    gatewaypunditlist = []
    thegatewaypundit = 'https://www.thegatewaypundit.com/'
    user_agent = \
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}
    request = urllib.request.Request(thegatewaypundit, None, headers)  # The assembled request
    response = urllib.request.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data, 'lxml')
    for h3 in soup.find_all('h3', class_='post-title'):
        blah = h3.find('a', text=True)
        headline = blah.text
        url = blah['href']
        d = {"source": source, 'headline': headline, 'url': url}
        gatewaypunditlist.append(d)


# This function scrapes WND's political frontpage only.
def scrapeWND():
    source = "WND"
    global wndlist
    wndlist = []
    wnd = 'http://www.wnd.com/category/front-page/politics/'
    user_agent = \
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}
    request = urllib.request.Request(wnd, None, headers)  # The assembled request
    response = urllib.request.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data, 'lxml')
    for i in soup.find_all('a', class_='cat-feature', href=True):
        headline = i.find('h1', class_='posttitle').text
        url = i['href']
        d = {"source": source, 'headline': headline, 'url': url}
        wndlist.append(d)


# This function scrapes all stories from Conservative Tribune.
def CT():
    source = "Conservative Tribune"
    global ctlist
    ctlist = []
    ct = 'https://www.westernjournal.com/ct/'
    r = requests.get(ct)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    for article in soup.find_all('article', class_='post'):
        headline = article.find('h3', class_='entry-title').text
        url = article.find('a', attrs={'data-type': 'Internal link'},
                           href=True)['href']
        d = {"source": source, 'headline': headline, 'url': url}
        ctlist.append(d)


# This function takes the front stories from Fox News Insider.
def InsiderFoxNews():
    source = "Fox News Insider"
    global insiderfoxlist
    insiderfoxlist = []
    fox = 'http://insider.foxnews.com/'
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options, executable_path='C:\\Users\\Seth\\Documents\\geckodriver\\geckodriver.exe')
    driver.get(fox)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    for i in soup.find_all('h2')[0:40]:
        if i.find("a") != None:
            headline = i.find('a').text
            url = i.find('a', href=True)['href']
            d = {"source": source, 'headline': headline, 'url': url}
            insiderfoxlist.append(d)
    driver.quit()


# This function scrapes TheHill.com.
def TheHill():
    source = "The Hill"
    global thehilllist
    thehilllist = []
    hill = 'http://thehill.com/'
    r = requests.get(hill)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    for story in soup.find_all('div', class_="top-story-item"):
        headline = story.find('a')["title"]
        url = 'http://thehill.com' + story.find('a', href=True)['href']
        d = {"source": source, 'headline': headline, 'url': url}
        thehilllist.append(d)

#This function scrapes IJ Review.
def ijr():
    import os
    global ijrlist
    os.environ["PATH"] += os.pathsep + 'C:\\Users\\Seth\\Documents\\geckodriver\\geckodriver.exe'
    source = "IJ Review"
    ijrlist = []
    ijr = 'https://ijr.com/'
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options, executable_path='C:\\Users\\Seth\\Documents\\geckodriver\\geckodriver.exe')
    driver.get(ijr)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    for story in soup.find_all('div', class_='col-12'):
        if story.find("h2") != None and story.find("a", href=True) != None:
            headline = story.find("h2").text
            source = ijr + story.find("a", href=True)["href"]
            ijrlist.append({"source" : "IJ Review" ,"headline" : headline, "url" : source})
    driver.quit()
    listofindexes = []
    # Check for duplicates in IJR stories.
    for a in range(0, len(ijrlist)):
        if a != len(stories):
            for b in range(a+1, len(ijrlist)):
                if ijrlist[a]["headline"] in ijrlist[b]["headline"]:
                    listofindexes.append(a)

    for i in sorted(listofindexes, reverse=True):
        ijrlist.pop(i)  

# This function scrapes Breitbart's website.
def Breitbart():
    source = "Breitbart"
    global soup
    global breitbartlist
    breitbartlist = []
    breitbart = 'http://www.breitbart.com/'
    r = requests.get(breitbart)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    soup = soup.find("ul", id="BBTrendUL")
    for story in soup.find_all('li'):
        headline = story.find('a').text
        url = story.find("a", href=True)["href"]
        d = {"source": source, 'headline': headline, 'url': url}
        breitbartlist.append(d)

# This function scrapes FreeBeacon.com
def FreeBeacon():
    source = "Free Beacon"
    global freebeaconlist
    freebeaconlist = []
    fb = 'http://freebeacon.com/'
    r = requests.get(fb)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    soup = soup.find("div", class_="show-for-large-up")
    for story in soup.find_all("article",class_="post"):
        headline = story.find("a", {"rel":"bookmark"})['title']
        url = story.find("a", href=True)["href"]
        d = {"source": source, 'headline': headline, 'url': url}
        freebeaconlist.append(d)

# This function finds stories from dennismichaellynch.com
def Dennis():
    source = "Dennis Michael Lynch"
    global dennislist
    dennislist = []
    link = "http://dennismichaellynch.com/"
    user_agent = \
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}
    request = urllib.request.Request(link, None, headers)  # The assembled request
    response = urllib.request.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data, 'lxml')
    for story in soup.find_all("div", class_="td_module_14 td_module_wrap td-animation-stack"):
        headline = story.find("a")["title"]
        url = story.find("a", href=True)["href"]
        d = {"source": source, 'headline': headline, 'url': url}
        dennislist.append(d)

# This function extracts stories from Western Journal.
def WesternJournal():
    source = "Western Journal"
    global westernjournallist
    westernjournallist = []
    link = "https://www.westernjournal.com/"
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    soup = soup.find("div", id="fhe-section-0")
    for story in soup.find_all("div", class_="fhe-headline"):
        headline = story.find("a").text
        url = story.find("a", href=True)["href"]
        d = {"source": source, 'headline': headline, 'url': url}
        westernjournallist.append(d)

# This function gets news from JudicialWatch.com
def JudicialWatch():
    source = "Judicial Watch"
    global judicialwatchlist
    judicialwatchlist = []
    link = "http://www.judicialwatch.org/"
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    soup = soup.find("ul", id="tslinks")
    for story in soup.find_all("li"):
        headline = story.find("a").text
        url = story.find("a", href=True)["href"]
        if url[0:8] != "https://":
            print "not a valid url"
        else:
            d = {"source": source, 'headline': headline, 'url': url}
            judicialwatchlist.append(d)
            time.sleep(.3)
        
# This function gets news from the daily caller.
def DailyCaller():
    source = "Daily Caller"
    global dailycallerlist
    dailycallerlist = []
    link = "http://dailycaller.com/"
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    soup = soup.find("div", "articles trending")
    for story in soup.find_all("a", href=True):
        headline = story.find("h4").text
        url = "http://dailycaller.com" + story["href"]
        d = {"source": source, 'headline': headline, 'url': url}
        dailycallerlist.append(d)

# This function searches Weasel Zippers for stories.
def WeaselZippers():
    source = "Weasel Zippers"
    global weaselzipperslist
    weaselzipperslist = []
    link = "https://www.weaselzippers.us/"
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    for story in soup.find_all("div","post")[0:10]:
        headline = story.find("a").text
        url = story.find("a",href=True)['href']
        d = {"source": source, 'headline': headline, 'url': url}
        weaselzipperslist.append(d)

# This function searches Mad World News for stories.
def MadWorldNews():
    source = "Mad World News"
    global madworldlist
    madworldlist = []
    madworld = 'https://madworldnews.com/'
    r = requests.get(madworld)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    for story in soup.find_all("article", class_="post"):
        if story.find("a"):
            url = story.find("a", href=True)["href"]
            headline = story.find("a", href=True)["title"]
            d = {"source": source, 'headline': headline, 'url': url}
            madworldlist.append(d)

# This function searches Red State Watcher for stories.
def RedStateWatcher():
    source = "Red State Watcher"
    global redstatelist
    redstatelist = []
    redstatewatcher = 'http://redstatewatcher.com/'
    r = requests.get(redstatewatcher)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    for story in soup.find_all("div", class_="col-sm-4"):
        if story.find("a"):
            url = redstatewatcher + story.find("a", href=True)["href"]
            headline = story.find("img")["alt"]
            d = {"source": source, 'headline': headline, 'url': url}
            redstatelist.append(d)

# This function searches NTKNetwork for stories.
def NTKNetwork():
    source = "NTK Network"
    global ntknetworklist
    ntknetworklist = []
    ntknetwork = 'https://ntknetwork.com/'
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options, executable_path='C:\\Users\\Seth\\Documents\\geckodriver\\geckodriver.exe')
    driver.get(ntknetwork)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    for story in soup.find_all("article"):
        f = story.find("div", class_="text")
        if f.find("a", href=True):
            url = f.find("a", href=True)["href"]
            headline = f.find("a", href=True).text
            d = {"source": source, 'headline': headline, 'url': url}
            ntknetworklist.append(d)
    driver.quit()

# This function searches Chicks on the Right for stories.
def ChicksOnTheRight():
    source = "Chicks On The Right"
    global chicksontherightlist
    chicksontherightlist = []
    link = "https://www.chicksonright.com/blog/category/politics/"
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options, executable_path='C:\\Users\\Seth\\Documents\\geckodriver\\geckodriver.exe')
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    print soup
    for story in soup.find_all("div",class_="td-block-span6")[0:3]:
        headline = story.find("a").text
        url = story.find("a",href=True)['href']
        d = {"source": source, 'headline': headline, 'url': url}
        chicksontherightlist.append(d)
    driver.quit()

# This function searches FederalistPapers for stories.
def FederalistPapers():
    source = "Federalist Papers"
    global federalistpaperslist
    federalistpaperslist = []
    federalistpapers = 'https://thefederalistpapers.org/'
    r = requests.get(federalistpapers)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    for story in soup.find_all("article", class_="post")[0:5]:
        if story.find("a"):
            url = story.find("a", href=True)["href"]
            headline = story.find("h3").text
            d = {"source": source, 'headline': headline, 'url': url}
            federalistpaperslist.append(d)

# This function searches Sean Hannity for stories.
def SeanHannity():
    source = "Sean Hannity"
    global seanhannitylist
    seanhannitylist = []
    seanhannity = 'https://www.hannity.com/'
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options, executable_path='C:\\Users\\Seth\\Documents\\geckodriver\\geckodriver.exe')
    driver.get(seanhannity)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    print soup
    for story in soup.find_all("div", class_="size-h"):
        if story.find("a"):
            url = story.find("a", href=True)["href"]
            headline = story.find("h2").text
            d = {"source": source, 'headline': headline, 'url': url}
            seanhannitylist.append(d)
    driver.quit()

# This function searches Biz Pac Review for stories.
def BizPacReview():
    source = "Biz Pac Review"
    global bizpacreviewlist
    bizpacreviewlist = []
    link = "https://www.bizpacreview.com/#home"
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    for story in soup.find_all("div", class_="bordered-box")[0:10]:
        if story.find("h4") != None and story.find("a",href=True) != None:
            headline = story.find("h4").text
            url = story.find("a",href=True)['href']
            d = {"source": source, 'headline': headline, 'url': url}
            bizpacreviewlist.append(d)

# This function searches Washington Examiner for stories.
def WashingtonExaminer():
    source = "Washington Examiner"
    global washingtonexaminerlist
    washingtonexaminerlist = []
    link = "https://www.washingtonexaminer.com/"
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options, executable_path='C:\\Users\\Seth\\Documents\\geckodriver\\geckodriver.exe')
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    for story in soup.find_all("li", class_="TimelineList-items-item"):
        if story.find("a") != None:
            headline = story.find("a").text
            url = story.find("a",href=True)['href']
            d = {"source": source, 'headline': headline, 'url': url}
            washingtonexaminerlist.append(d)
    driver.quit()

# This function searches Washington Times for stories.
def WashingtonTimes():
    source = "Washington Times"
    global washingtontimeslist
    washingtontimeslist = []
    link = "https://www.washingtontimes.com/news/politics/"
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options, executable_path='C:\\Users\\Seth\\Documents\\geckodriver\\geckodriver.exe')
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    for story in soup.find_all("article", class_="story"):
        if story.find("h2") != None:
            headline = story.find("h2").find("a").text
            url = "https://www.washingtonexaminer.com" + story.find("h2").find("a", href=True)["href"]
            d = {"source": source, 'headline': headline, 'url': url}
            washingtontimeslist.append(d)
    driver.quit()

# This function searches LifeZette for stories.
def LifeZette():
    source = "LifeZette"
    global lifezettelist
    lifezettelist = []
    link = "https://www.lifezette.com/"
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    for story in soup.find_all("article", class_="article")[0:10]:
        if story.find("h2") != None:
            headline = story.find("h2").find("a").text
            url = story.find("h2").find("a", href=True)["href"]
            d = {"source": source, 'headline': headline, 'url': url}
            lifezettelist.append(d)

# This function searches The Right Scoop for stories.
def TheRightScoop():
    source = "The Right Scoop"
    global rightscooplist
    rightscooplist = []
    link = "http://therightscoop.com/"
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    for story in soup.find_all("article", class_="post")[0:7]:
        if story.find("h2") != None:
            headline = story.find("h2").find("a").text
            url = story.find("h2").find("a", href=True)["href"]
            d = {"source": source, 'headline': headline, 'url': url}
            rightscooplist.append(d)

# This function searches The Anti Media for stories.
def TheAntiMedia():
    source = "The AntiMedia"
    global antimedialist
    antimedialist = []
    link = "https://theantimedia.com/"
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    for story in soup.find_all("div", class_="content")[0:9]:
        if story.find("a") != None:
            headline = story.find("a").find("h6").text
            url = story.find("a", href=True)["href"]
            d = {"source": source, 'headline': headline, 'url': url}
            antimedialist.append(d)


# This function gets as many share-counts from Facebook's API as it safely can.
def getshares(linklist):
    global stories
    for i in range(0,85):
        shares = facebookShares(linklist[i]['url'])
        stories[i]["shares"] = str(shares)
        time.sleep(22)

# This function appends all scraped data to the global stories list.
def connectNewsLists():
    global stories
    data = [foxnewslist, dailywirelist, gatewaypunditlist, wndlist, ctlist, insiderfoxlist, thehilllist, ijrlist, breitbartlist, freebeaconlist, westernjournallist, judicialwatchlist, dailycallerlist, weaselzipperslist, madworldlist, redstatelist, ntknetworklist, chicksontherightlist, seanhannitylist, bizpacreviewlist, washingtonexaminerlist, washingtontimeslist, lifezettelist, rightscooplist, antimedialist]
    length = len(data)
    for site in range(0, length):
        length2 = len(data[site])
        for i in range(0,length2):
            stories.append(data[site][i])
    print "finished!"
                
# The 'scrapingfunctions' list contains all functions that search for news stories.
scrapingfunctions = [scrapeFoxNews, scrapeDailyWire, scrapeTheGatewayPundit, scrapeWND, CT, InsiderFoxNews, TheHill, ijr, Breitbart, FreeBeacon, Dennis, WesternJournal, JudicialWatch, DailyCaller, WeaselZippers, MadWorldNews, RedStateWatcher, NTKNetwork, ChicksOnTheRight, FederalistPapers, SeanHannity, BizPacReview, WashingtonExaminer, WashingtonTimes, LifeZette, TheRightScoop, TheAntiMedia]

# This function prints all items from the global 'stories' list.
def printStories():
    global stories
    for story in stories:
        print story["source"]
        print story["headline"]
        print story["url"]
        print ""
    print "Complete!"

# This functions runs the storyfinding processes.
def start():
    global scrapingfunctions
    print "Starting Processes"
    runTasks(scrapingfunctions)
    print "Complete!"
    time.sleep(2)
    connectNewsLists()
    print "Printing Results:"
    printStories()

    
