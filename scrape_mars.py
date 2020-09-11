# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    # Replaced the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # ----VISIT MARS NEWS SITE----

    # Visit mars.nasa.gov/news
    url = "https://mars.nasa.gov/news"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the news title of the first post
    news_element = soup.select_one('ul.item_list li.slide')
    titles = news_element.find('div', class_ = 'content_title').get_text()

    # Get Title
    titles

    # Grab coordinating teaser paragraph
    teaser_p = news_element.find('div', class_='article_teaser_body').get_text()
    teaser_p

    # ----JPL Mars Space Images - Featured Image----
    
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

    # Store data in a dictionary
    mars_data = {
          "News Title:":titles,
          "News Teaser:":teaser_p,
          "Full Featured Image:":final_main_image
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
