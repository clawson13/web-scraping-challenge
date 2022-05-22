#!/usr/bin/env python
# coding: utf-8

# # Part  1: Scraping

# In[1]:


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pymongo
import pandas as pd
import os


# ## NASA Mars News

# In[2]:

def scrape():
    # Set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)


    # In[3]:


    # Link to website
    url = 'https://redplanetscience.com/#'
    browser.visit(url)


    # In[4]:


    # Scrape website and store first news article's title and paragraph in variables
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    print(news_title)
    print(news_p)


    # ## JPL Mars Space Images—Featured Image

    # In[5]:


    # Link to website
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)


    # In[6]:


    # Scrape website for featured image URL; includes click for full image
    html = browser.html
    browser.links.find_by_partial_text('FULL IMAGE').click()
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = 'https://spaceimages-mars.com/' + soup.find('img', class_='headerimage fade-in')['src']

    print(featured_image_url)


    # ## Mars Facts

    # In[7]:


    # Source url
    url = 'https://galaxyfacts-mars.com/'


    # In[8]:


    # Use Panda's `read_html` to parse the url
    tables = pd.read_html(url)

    mars_facts = tables[0] # Select Mars facts table
    mars_facts.columns = ['Description', 'Mars', 'Earth'] # Rename the columns
    mars_facts.set_index('Description', inplace=True) # Set the index to the first column

    # Convert Mars Facts Data Frame to html, removing unwanted newlines
    mars_facts = mars_facts.to_html(classes='table table-stripped', justify='left', border=1)
    mars_facts = mars_facts.replace('\n', '')
    mars_facts


    # ## Mars Hemispheres

    # In[9]:


    # Link to website
    url = 'https://marshemispheres.com/'
    browser.visit(url)


    # In[10]:


    # Scrape website
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    # Collect h3 text for hemisphere links
    container = soup.find('div', class_="collapsible results")
    products = container.find_all('h3')

    # Create list for each link's/image's title and list for combined title and image url
    titles = []
    hemisphere_image_urls = []

    # Collect the hemisphere title names and clean them for later display
    for x in range(0, len(products)):
        title_draft = products[x].text
        titles.append(title_draft)

    # Click each link by title, click to obtain each image's html, and create final list of combined title/url
    for title in titles:
        browser.links.find_by_partial_text(title).click()
        browser.links.find_by_text('Open').click()

        html = browser.html
        soup = BeautifulSoup(html, 'lxml')

        img_url = 'https://marshemispheres.com/' + soup.find('img', class_="wide-image")['src']

        dict_entry = {}
        dict_entry['title'] = title
        dict_entry['img_url'] = img_url

        hemisphere_image_urls.append(dict_entry)


        browser.links.find_by_text('Close').click()
        browser.links.find_by_partial_text('Back').click()

    print(hemisphere_image_urls)


    # In[11]:


    # Quit the browser
    browser.quit()


    # # Part 2: MongoDB and Flask Application

    # In[12]:


    # Set an empty dict for listings that we can save to Mongo
    mars_data = {}


    # In[13]:


    # Add scraped data to the dict
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p
    mars_data['featured_image_url'] = featured_image_url
    mars_data['mars_facts'] = mars_facts
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    # Return the dictionary
    return mars_data