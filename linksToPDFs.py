################################################################################################################################
#                                                       ABOUT                                                                  #
################################################################################################################################
'''
Program:   linksToPDFs
Pieced together by:    Mike Tjoelker (with help from StackOverflow!)
Last updated:    18 April 2017
Purpose: 
         This python program is being designed based on the desires of a client running the website www.agentorangegmo.com.
         Client wants all linked sources on her webpage to be saved as PDFs, in case any linked articles are taken offline.
         Client has ~180 linked sourced, and I am too lazy to save them all one by one, so decided to try writing my first
         Python program instead, so it could do it for me.
         
	 This program will take sites given to it(via local file startSites.txt), find all links referenced on those sites, 
	 and convert each link(that does not include a string from local file excludeStrings.txt) to a PDF to be stored locally.
	 Any errors will be printed to screen after all possible PDFs are saved.
         
         Upon running this from Windows cmd, I suggest: python ./linksToPDFs > messages.txt
                                                        (so that printed errors and other information will be put in a text file)

Current version:
      16 April 2017  - As of now, code is very sloppy and not general enough (bad reusability for anyone other than me)

Desired changes:
    1. Name PDFs descriptively (ex: 1_ArticleTitle.pdf or 2_PublisherName.pdf) 
    3. Don't need two lists - everything could be filtered properly in one
    
'''
################################################################################################################################
import pdfkit
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
from more_itertools import unique_everseen


# INITIALIZE LISTS
#    -> foundLinks will contain all links found on the given web pages
#    -> sourceLinks will contain the same links, minus duplicates, ones that 
#       do not start with http, and ones that contain links that stay 
#       on the same site (I only want to gather PDFs of outside sources)
foundLinks = [] # list of all links found on page 
sourceLinks = [] # list of all links on pages in startSites that are sources
errorList = [] # list of all errors
successList = [] # list of successes

startSites = [] # list of sites we want to grab sources from - grab these from local file startSites.txt
with open("startSites.txt") as f:
	for line in f:
		try:
			startSites.append(line.rstrip('\n'))
			'''
			success test
			'''
			successList.append("startSites.append SUCCESS: "+line.rstrip('\n'))		
		except:
			errorList.append("startSite.append ERROR: "+line.rstrip('\n'))
			continue

excludeStrings = []  # list of strings we do not want in source links to save as pdfs - grab from local file excludeStrings
with open("excludeStrings.txt") as f:
	for line in f:
		try:
			excludeStrings.append(line.rstrip('\n')) 
			'''
			success test
			'''
			successList.append("excludeStrings.append SUCCESS: "+line.rstrip('\n'))	
		except:
			excludeStrings.append("excludeStrings.append ERROR: "+line.rstrip('\n'))
			continue

###########################################################################
#                               FUNCTIONS                                 #
###########################################################################
# Function: addLinksToList
# Returns: nothing
# Purpose: takes a site and adds all of its links to foundLinks
def addLinksToList(site):
	http = httplib2.Http()
	status, response = http.request(site)

	soup = BeautifulSoup(response, "html5lib")
	
	for link in soup.find_all('a'):
		try:
			foundLinks.append(link['href']) 
			'''
			success test
			'''
			successList.append("foundLinks.append SUCCESS: "+link['href'])	

		except:
			errorList.append("foundLinks.append ERROR: "+link['href'])
			continue
		
	return
# End of Function



# Function: canConnect
# Returns: boolean
# Purpose: returns true if site can be reached
def canConnect(site):
	http = httplib2.Http()
	try:
		status, response = http.request(site)
		'''
		success test
		'''
		successList.append("canConnect SUCCESS: "+site)	
	except:
		errorList.append("canConnect ERROR: "+site)
		errorList.append("   -> Site unreachable and will not become a PDF")		
		return 0
	return 1
# End of Function

###############################################################################
#                                  MAIN                                       #
###############################################################################
# 1. Grab links from given sites - they will be added to foundLinks
# 2. Make sourceLinks based on foundLinks, but removes all duplicate links, 
#    links that don't start with 'http', and links containing 'agentorangegmo' 
# 3. Use PDFkit to convert list of links to PDFs and store on local device
###############################################################################

# 1. Grab all links found on webpages in startSites - they will be added to foundLinks
for site in startSites:
	try:
		addLinksToList(site)
		'''
		success test
		'''
		successList.append("addLinksToList SUCCESS: "+site)	
	except:
		errorList.append("addLinksToList ERROR: " + site)
		errorList.append("   -> Site unreachable and will not be included for gathering source links from")
		continue
	
# 2. Make sourceLinks based on foundLinks, but removes all duplicate links, 
#    links that don't start with 'http', and links containing 'agentorangegmo' 
#[sourceLinks.append(item) for item in foundLinks if not item in sourceLinks and "http" in item and badString not in item and canConnect(item)]
[sourceLinks.append(item) for item in foundLinks if not item in sourceLinks and "http" in item and not any(badString in item for badString in excludeStrings) and canConnect(item)]

# 3. Use PDFkit to convert list of links to PDFs and store on local device
# set up pdf grabber
path_wkthmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

#initialize counter for PDF naming
counter = 1

#print all elements in sourceLinks to PDF
for elem in sourceLinks:
	try:
		kit = pdfkit.from_url(elem,'./PDFs/'+str(counter)+'.pdf',configuration=config)
		'''
		success test
		'''
		successList.append("PDF SUCCESS: "+str(counter)+") "+elem)
		counter += 1
	except:
		errorList.append("PDF ERROR: "+str(counter)+") "+elem)
		counter += 1
		continue



'''	
#PRINT SUCCESS LIST HERE	
'''
print()
print("**********************************")
print("*          SUCCESS LIST          *")
print("**********************************")
print()
for sux in successList:
	print(sux)

		
'''	
#PRINT ERROR LIST HERE	
'''
print()
print("**********************************")
print("*           ERROR LIST           *")
print("**********************************")
print()
for err in errorList:
	print(err)

	
###########################################################################
#                              END OF PROGRAM                             #
###########################################################################
	

