# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup


# ### For a Windows machine
# * executable_path = {'executable_path': 'chromedriver.exe'}
# * browser = Browser('chrome', **executable_path, headless=False)

# ### Running on a Mac

# In[2]:


# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
get_ipython().system('which chromedriver')


# In[3]:


# Set executable path and start up Chrome browser
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# ### NASA Mars News

# * Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

# LINK:  https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest

# In[4]:


# Directs to open to https://mars.nasa.gov/news
url = 'https://mars.nasa.gov/news'
browser.visit(url)


# In[5]:


# HTML object
html = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')
news_element=soup.select_one('ul.item_list li.slide')
titles=news_element.find('div', class_ = 'content_title').get_text()

# Get Title
titles


# Grab coordinating teaser paragraph
teaser_p = news_element.find('div', class_='article_teaser_body').get_text()
teaser_p


# ### JPL Mars Space Images - Featured Image

# * Visit the url for JPL Featured Space Image here.
# 
# 
# * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
# 
# 
# * Make sure to find the image url to the full size .jpg image.
# 
# 
# * Make sure to save a complete url string for this image.
# 
# 
# 

# LINK:  https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars

# In[7]:


# Directs to open to https://mars.nasa.gov/news
image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(image_url)

# Clicking through to find full-featured url
browser.find_by_id('full_image').click()

# Clicking through to find full-featured url
more_info_element = browser.links.find_by_partial_text('more info').click()

# Clicking through to find full-featured url
html2 = browser.html
main_image_soup = BeautifulSoup(html2, 'html.parser')
main_image_url = main_image_soup.select_one('figure.lede a img').get('src')

# Get main image url
main_image_url

# Find full-featured url
main_url = "https://www.jpl.nasa.gov"
final_main_image = main_url + main_image_url

# Full-featured url
final_main_image


# ### Mars Facts

# * Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# 
# * Use Pandas to convert the data to a HTML table string.
# 
# 
# 
# 

# LINK: https://space-facts.com/mars/

# In[12]:


# Dependencies
import pandas as pd


# In[13]:


# Pulling data from this url
url = 'https://space-facts.com/mars/'


# In[14]:


# Reading the HTML tables into a list of tables 
tables = pd.read_html(url)
tables


# In[15]:


# Pulling the first table listed and creating column names
df = tables[0]
df.columns = ['Description','Value']
df


# In[16]:


# Set index to Description
df.set_index('Description',inplace=True)


# In[17]:


# Display the new dataframe
df


# In[18]:


# Generate new table to html
# Stripping unwanted new lines
mars_facts = df.to_html()
mars_facts.replace('\n', '')


# ### Mars Hemispheres

# * Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
# 
# 
# * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# 
# 
# * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# 
# 
# * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

# LINK: https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

# In[19]:


hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemisphere_url)
html_hemis = browser.html
#parse
soup_hemis = BeautifulSoup(html_hemis, 'html.parser')


# In[20]:


urls_hemis =  soup_hemis.find_all('div', class_ = 'item')

hemis_output = []
core_url = "https://astrogeology.usgs.gov"
for mh in urls_hemis:
    
    #Store the title
    title = mh.find('h3').text
    
    #look for the image
    temp_image = mh.find('a', class_ = 'itemLink product-item')['href']
    
    browser.visit(core_url + temp_image)
    
    #convert to html object
    temp_image_html = browser.html
    #parse it
    soup_hemis2 = BeautifulSoup(temp_image_html, 'html.parser')
    
    #scrape it
    full_image = core_url + soup_hemis2.find('img', class_='wide-image')['src']
    
    
    #create a dic and append to list
    hemis_output.append({"title":title, "image_url": full_image})

  
   


# In[21]:


hemis_output


# In[22]:


browser.quit()

