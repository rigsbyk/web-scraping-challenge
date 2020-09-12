# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests


def init_browser():
    # Replaced the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Store data in a dictionary
    # Create a scrape_news dict that we can insert into mongoDB
    mars_dict = {}

    # Run the first function
    titles, teaser_p = scrape_news()
   
    # Run all functions and store in a dictionary
    mars_dict["title"] = titles
    mars_dict["paragraph"] = teaser_p 
    mars_dict["main_image"] = scrape_mars_images()
    mars_dict["mars_facts"] = mars_facts()
    mars_dict["mars_hemispheres"] = mars_hemis() 

    browser.quit()
    return mars_dict

def scrape_news():

    browser = init_browser()

    # ----VISIT MARS NEWS SITE----

    # Visit mars.nasa.gov/news
    url = "https://mars.nasa.gov/news"
    browser.visit(url)
    
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    try:
    # Get the news title of the first post
        news_element = soup.select_one('ul.item_list li.slide')
        titles = news_element.find('div', class_ = 'content_title').get_text()

    # Grab coordinating teaser paragraph
        teaser_p = news_element.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    browser.quit()

    return titles, teaser_p

def scrape_mars_images():

    browser = init_browser()

    # ----JPL MARS SPACE IMAGES - FEATURED IMAGE----
    
    # Directs to open to https://mars.nasa.gov/news
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(1)

    # Clicking through to find full-featured url
    browser.find_by_id('full_image').click()

    # Clicking through to find full-featured url
    more_info_element = browser.links.find_by_partial_text('more info').click()

    # Clicking through to find full-featured url
    html2 = browser.html
    main_image_soup = bs(html2, 'html.parser')
    main_image_url = main_image_soup.select_one('figure.lede a img').get('src')

    # Get main image url
    main_image_url

    # Find full-featured url
    main_url = "https://www.jpl.nasa.gov"
    final_main_image = main_url + main_image_url

    browser.quit()
    return final_main_image

    # ----MARS FACTS----
def mars_facts():

    browser = init_browser()
    # Pulling data from this url
    url = 'https://space-facts.com/mars/'

    # Reading the HTML tables into a list of tables 
    tables = pd.read_html(url)
    tables

    # Pulling the first table listed and creating column names
    df = tables[0]
    df.columns = ['Description','Mars']
    df

    # Set index to Description
    df.set_index('Description',inplace=True)

    # Display the new dataframe
    df

    # Generate new table to html
    # Stripping unwanted new lines
    mars_facts = df.to_html()
    mars_facts.replace('\n', '')

    browser.quit()

    return mars_facts

def mars_hemis():

    browser = init_browser()
    # ----MARS HEMISPHERE----
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    html_hemis = browser.html

    #Parse
    soup_hemis = bs(html_hemis, 'html.parser')
    urls_hemis =  soup_hemis.find_all('div', class_ = 'item')

    # Loop through astrogeology.usgs.gov to find urls and titles
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
        soup_hemis2 = bs(temp_image_html, 'html.parser')

        #scrape it
        full_image = core_url + soup_hemis2.find('img', class_='wide-image')['src']
    
        #create a dic and append to list
        hemis_output.append({"title":title, "image_url": full_image})
    
    # Get hemis_output
    browser.quit()
    return hemis_output