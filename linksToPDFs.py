################################################################################################################################
#                                                       ABOUT                                                                  #
################################################################################################################################
'''
Program:   linksToPDFs
Pieced together by:    Mike Tjoelker (with help from StackOverflow!)
Last updated:    16 April 2017
Purpose: 
         This python program is being designed based on the desires of a client running the website www.agentorangegmo.com.
         Client wants all linked sources on her webpage to be saved as PDFs, in case any linked articles are taken offline.
         Client has ~180 linked sourced, and I am too lazy to save them all one by one, so decided to try writing my first
         Python program instead, so it could do it for me.
         
         This program will take sites given to it, find all links referenced on those sites, and convert each link to a PDF
         to be stored locally. Some pages return errors (are either offline or are not URI friendly for the PDF converter). 
         These pages will be printed to the screen and will include the error number
         
         Upon running this from Windows cmd, I suggest: python ./linksToPDFs > messages.txt
                                                        (so that printed errors and other information will be put in a text file)

Current version:
      16 April 2017  - As of now, code is very sloppy and not general enough (bad reusability for anyone other than me)

Desired changes:
    1. Name PDFs descriptively (ex: 1_ArticleTitle.pdf or 2_PublisherName.pdf) 
    2. Program should take a text file with a list of web pages on it, that it will gather links from
       (as of now this is hardcoded in, one link at a time)
    3. Don't need two lists - everything could be filtered properly in one
    4. Output a list of all sites that could not be reached (so that client knows which sources no longer work)
    5. Clean up output - maybe put gathered errors into a list to be printed at end - so that it doesn't conflict with
        output of PDF conversion progress.
    
'''
################################################################################################################################
import pdfkit
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
from more_itertools import unique_everseen

# INITIALIZE LISTS
#    -> siteList will contain all links found on the given web pages
#    -> uniqueList will contain the same links, minus duplicates, ones that 
#       do not start with http, and ones that contain links that stay 
#       on the same site (I only want to gather PDFs of outside sources)
siteList = []
uniqueList = []

###########################################################################
#                               FUNCTIONS                                 #
###########################################################################
# Function: addLinksToList
# Returns: nothing
# Purpose: takes a site and adds all of its links to siteList
def addLinksToList(site):
	http = httplib2.Http()
	status, response = http.request(site)

	soup = BeautifulSoup(response, "html5lib")
	
	for link in soup.find_all('a'):
		#if 'href' in getattr(link,'attrs',{}):
		siteList.extend([link['href']])
		#siteList.extend(link)
		
	return
# End of Function



# Function: canConnect
# Returns: boolean
# Purpose: returns true if site can be reached
def canConnect(site):
	http = httplib2.Http()
	try:
		status, response = http.request(site)
	except:
		return 0
	return 1
# End of Function

###############################################################################
#                                  MAIN                                       #
###############################################################################
# 1. Grab links from given sites - they will be added to siteList
# 2. Make uniqueList based on siteList, but removes all duplicate links, 
#    links that don't start with 'http', and links containing 'agentorangegmo' 
# 3. Use PDFkit to convert list of links to PDFs and store on local device
###############################################################################

# 1. Grab links from given sites - they will be added to siteList
addLinksToList('http://agentorangegmo.com/')
addLinksToList('http://agentorangegmo.com/kids-cancer')	
addLinksToList('http://agentorangegmo.com/surge-autism')
addLinksToList('http://agentorangegmo.com/adults-cancer')
addLinksToList('http://agentorangegmo.com/new-news')
addLinksToList('http://agentorangegmo.com/24-d-agent-orange-new-gmo-food-ingredient')
addLinksToList('http://agentorangegmo.com/agent-orange-vietnam-vets')
addLinksToList('http://agentorangegmo.com/money-matters-kids-matter-more')
addLinksToList('http://agentorangegmo.com/roundup-everywhere')
addLinksToList('http://agentorangegmo.com/herbicides-sticking-dinner-snacks')
addLinksToList('http://agentorangegmo.com/what-you-can-do-your-family-yourself')
addLinksToList('http://agentorangegmo.com/upcoming-articles')
addLinksToList('http://agentorangegmo.com/source-links')
	
# 2. Make uniqueList based on siteList, but removes all duplicate links, 
#    links that don't start with 'http', and links containing 'agentorangegmo' 
[uniqueList.append(item) for item in siteList if not item in uniqueList and "http" in item and "agentorangegmo" not in item and canConnect(item)]


# 3. Use PDFkit to convert list of links to PDFs and store on local device
# set up pdf grabber
path_wkthmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

#initialize counter for PDF naming
counter = 1

#print all elements in uniqueList to PDF
# TESTING: for elem in ["https://www.nytimes.com/2016/10/30/business/gmo-promise-falls-short.html","https://www.washingtonpost.com/news/speaking-of-science/wp/2016/05/17/ge-crops/?utm_term=.56c580dec09e"]:
for elem in uniqueList:
	try:
		#print(elem)	
		item = elem
		#kit = pdfkit.from_url(elem,'./PDFs/'+str(counter)+'.pdf',options=options,configuration=config)
		kit = pdfkit.from_url(elem,'./PDFs/'+str(counter)+'.pdf',configuration=config)
		counter += 1
	except:
		print(str(counter)+ ") Error: " + elem)
		continue
    
###########################################################################
#                              END OF PROGRAM                             #
###########################################################################
	

