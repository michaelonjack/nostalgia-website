import os
import webapp2
import jinja2
import random

from urllib2 import urlopen
from urllib2 import Request
from auth import authenticate
from json import load # decodes retrieved JSON
from google.appengine.ext import ndb

# Set up the jinja environment
template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
        autoescape = True) #Jinja will now autoescape all html
        
############# urllib2 example ######################
#
#	// Send a request to google.com and store its response in variable 'website'
#	website = urlopen("http://google.com/")
#	
#	// Read the text of google's response
#	resp = website.read()
#

# THREE FUNCTIONS FOR RENDERING BASIC TEMPLATES
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)
    
    def render_str(self,template, **kw):
        t = jinja_env.get_template(template)
        return t.render(kw)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))












# Database of images that are displayed on the site
#	- link = link to the image that is displayed
#	- category = which category the image is filed under (general,tv,etc.)
#	- created = date/time the image was added to the database
class Image(ndb.Model):
    link = ndb.StringProperty(required=True)
    category = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    
class Waitlist(ndb.Model):
    link = ndb.StringProperty(required=True)
    category = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    
    
    
    
    
    
    
    
    
    
    
########################## DATASTORE FUNCTIONS ###################################################    
def addImage(imglink,category,inWaitlist):
	if imglink:
		if inWaitlist:
    			newImg = Waitlist(link=imglink,category=category)
    		else:
    			newImg = Image(link=imglink,category=category)
    		newImg.put()

def removeImage(imglink,inWaitlist):
	if inWaitlist:
		pics = Waitlist.query(Waitlist.link==imglink)
	else:
		pics = Image.query(Image.link==imglink)
	if pics:
		for pic in pics:
			pic.key.delete()
def removeAll(category,inWaitlist):
	if inWaitlist:
		pics = Waitlist.query(Wailist.category==category)
	else:
		pics = Image.query(Image.category==category)
	for pic in pics:
		removeImage(pic.link,inWaitlist)
		
def getNumPages(picList):
	count = 0
	numPages = 1
	
	for pic in picList:
		count = count + 1
	
	numPages = numPages + count/26
		
	return numPages
		
##############################################################################################    










########################## IMGUR FUNCTIONS ###################################################

def upload_to_imgur(client,category,url):
	# Enter metadata for the upload (all are optional)
	album = imgur_album_dict[category]
	config = {
		'album': album, # album must be album id number
		'name': category,
		'title': 'Nostalgic-thirst',
		'description': "From " + url
	}
	
	image = client.upload_from_url(url, config=config, anon=False)
	
	return image['link']
	
	
	
	
def get_imgur_album(category):

	album = imgur_album_dict[category]
	url_request = 'https://api.imgur.com/3/album/' + album
	
	request = Request(url_request)
	request.add_header('Authorization','Client-ID d67e71100199547')
	response = urlopen(request)
	json_obj = load(response)
	
	images = json_obj['data']['images']
	
	return images
	
		
##############################################################################################










cursorAnimations = [84980, 84981, 84982, 84983, 84984, 84985, 84988, 84989, 67418]
numAnimations = len(cursorAnimations)
def getCursorNum():
	cursorNum = random.randint(0,numAnimations-1)
    	cursorNum = cursorAnimations[cursorNum]
    	return cursorNum
	


imgur_album_dict = {
		"general":"ebt94",
		"games":"r5DjN",
		"advertisements":"NGfeo",
		"technology":"JK4Zf",
		"television":"eAsZW",
		"movies":"Q5TNS" }
		





####################### PAGE HANDLERS ##########################################################

class MainPage(Handler):
    def get(self):
    	self.render("nostalgia.html",cursorNum=getCursorNum())

class TelevisionPage(Handler):
   def get(self):
    	# Get all pictures stored in the database
        pics = Image.query(Image.category=="television")
        # Sort images by the dates they were added (newer pics first)
        pics.order(-Image.created)
        # Get the number of pages necessary to display all images for this category (25 per page)
        numPages = getNumPages(pics)
        # Get the current page from url parameters
        currentPage = self.request.get("page") 
        # Convert the url parameter to an integer
        currentPage = int(currentPage)
    	self.render("category.html",cursorNum=getCursorNum(),category="television",pics=pics,numPages=numPages, 			currentPage=currentPage)
    
   def post(self):
    	# Get the link of the image that was submitted
     	imglink = self.request.get("img_link")
    	addImage(imglink,"television",1)
    	pics = Image.query(Image.category=="television")
    	pics.order(-Image.created)
    	numPages = getNumPages(pics)
    	currentPage = self.request.get("page")
    	currentPage = int(currentPage)
    	self.render("category.html",cursorNum=getCursorNum(),category="television",pics=pics,numPages=numPages, 			currentPage=currentPage)
    	
class TechnologyPage(Handler):
    def get(self):
    	# Get all pictures stored in the database
        pics = Image.query(Image.category=="technology")
        pics.order(-Image.created)
        numPages = getNumPages(pics)
        currentPage = self.request.get("page")
        currentPage = int(currentPage)
    	self.render("category.html",cursorNum=getCursorNum(),category="technology",pics=pics,numPages=numPages, 			currentPage=currentPage)
    	
    def post(self):
    	# Get the link of the image that was submitted
    	imglink = self.request.get("img_link")
    	addImage(imglink,"technology",1)
    	pics = Image.query(Image.category=="technology")
    	pics.order(-Image.created)
    	numPages = getNumPages(pics)
    	currentPage = self.request.get("page")
    	currentPage = int(currentPage)
    	self.render("category.html",cursorNum=getCursorNum(),category="technology",pics=pics,numPages=numPages, 			currentPage=currentPage)
    	
class MoviesPage(Handler):
    def get(self):
    	# Get all pictures stored in the database
        pics = Image.query(Image.category=="movies")
        pics.order(-Image.created)
        numPages = getNumPages(pics)
        currentPage = self.request.get("page")
        currentPage = int(currentPage)
    	self.render("category.html",cursorNum=getCursorNum(),category="movies",pics=pics,numPages=numPages, 			currentPage=currentPage)
    	
    def post(self):
    	# Get the link of the image that was submitted
    	imglink = self.request.get("img_link")
    	addImage(imglink,"movies",1)
    	pics = Image.query(Image.category=="movies")
    	pics.order(-Image.created)
    	numPages = getNumPages(pics)
    	currentPage = self.request.get("page")
    	currentPage = int(currentPage)
    	self.render("category.html",cursorNum=getCursorNum(),category="movies",pics=pics,numPages=numPages, 			currentPage=currentPage)
    	
class GamesPage(Handler):
    def get(self):
    	# Get all pictures stored in the database
        pics = Image.query(Image.category=="games")
        pics.order(-Image.created)
        numPages = getNumPages(pics)
        currentPage = self.request.get("page")
        currentPage = int(currentPage)
    	self.render("category.html",cursorNum=getCursorNum(),category="games",pics=pics,numPages=numPages, 			currentPage=currentPage)
    	
    def post(self):
    	# Get the link of the image that was submitted
    	imglink = self.request.get("img_link")
    	addImage(imglink,"games",1)
    	pics = Image.query(Image.category=="games")
    	pics.order(-Image.created)
    	numPages = getNumPages(pics)
    	currentPage = self.request.get("page")
    	currentPage = int(currentPage)
    	self.render("category.html",cursorNum=getCursorNum(),category="games",pics=pics,numPages=numPages, 			currentPage=currentPage)
    	
class GeneralPage(Handler):
    def get(self):
    	# Get all pictures stored in the database
        pics = Image.query(Image.category=="general")
        pics.order(-Image.created)
        numPages = getNumPages(pics)
        currentPage = self.request.get("page")
        currentPage = int(currentPage)
    	self.render("category.html",cursorNum=getCursorNum(),category="general",pics=pics,numPages=numPages, 			currentPage=currentPage)
    	
    def post(self):
        # Get the link of the image that was submitted
    	imglink = self.request.get("img_link")
    	addImage(imglink,"general",1)
    	pics = Image.query(Image.category=="general")
    	pics.order(-Image.created)
    	numPages = getNumPages(pics)
    	currentPage = self.request.get("page")
    	currentPage = int(currentPage)
    	self.render("category.html",cursorNum=getCursorNum(),category="general",pics=pics,numPages=numPages, 			currentPage=currentPage)

class AdsPage(Handler):
    def get(self):
    	# Get all pictures stored in the database with category 'ads'
        pics = Image.query(Image.category=="advertisements")
        pics.order(-Image.created)
        numPages = getNumPages(pics)
        currentPage = self.request.get("page")
        currentPage = int(currentPage)
    	self.render("category.html",cursorNum=getCursorNum(),category="advertisements",pics=pics,numPages=numPages, 			currentPage=currentPage)
    	
    def post(self):
    	# Get the link of the image that was submitted
    	imglink = self.request.get("img_link")
    	addImage(imglink,"advertisements",1)
    	pics = Image.query(Image.category=="advertisements")
    	pics.order(-Image.created)
    	numPages = getNumPages(pics)
    	currentPage = self.request.get("page")
    	currentPage = int(currentPage)
    	self.render("category.html",cursorNum=getCursorNum(),category="advertisements",pics=pics,numPages=numPages, 			currentPage=currentPage)
    	
class AdminPage(Handler):
    def get(self):
        # Get all picture currently on the waitlist
        pics = Waitlist.query()
        self.render("admin.html",pics=pics)
        
    def post(self):
    	submission = self.request.get("submission")
    	divide = submission.find(":")
    	category = submission[0:divide]
    	link = submission[divide+1:]
    	client = authenticate()
    	
    	if category=="delete":
    		# Remove from both image and waitlist database
    		removeImage(link,1)
    		removeImage(link,0)
    	else:
    		imgur_url = upload_to_imgur(client,category,link)
    		addImage(imgur_url,category,0)
    		
    	removeImage(link,1)
    	pics = Waitlist.query()
    	self.render("admin.html",pics=pics)
        

     
#############################################################################################


		
	









######################## URL MAPS ############################################################

application = webapp2.WSGIApplication([
    ('/', MainPage),
    (r'/television.*',TelevisionPage),
    (r'/technology.*',TechnologyPage),
    (r'/movies.*',MoviesPage),
    (r'/games.*',GamesPage),
    (r'/general.*',GeneralPage),
    (r'/ads.*',AdsPage),
    ('/adminyoyo',AdminPage)
    ], debug=True)
    
    
##############################################################################################
