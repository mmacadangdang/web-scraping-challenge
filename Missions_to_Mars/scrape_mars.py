# Dependencies and Setup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

# NASA Mars News
def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    mars_soup = BeautifulSoup(html, 'html.parser')

    # Scrape the latest article title and paragraph
    news_title = mars_soup.find('div', class_='content_title').text
    news_p = mars_soup.find('div', class_='article_teaser_body').text
    return news_title, news_p

# JPL Mars Space Images - Featured Image
def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    browser.click_link_by_partial_text('FULL IMAGE')
    sleep(1)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    featured_image_soup = BeautifulSoup(html, 'html.parser')

    # Scrape featured image url and return
    featured_image_url = featured_image_soup.find('figure', class_='lede').a['href']
    return featured_image_url

# Mars Weather
def weather_tweet(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    twitter_soup = BeautifulSoup(html, 'html.parser')
    
    # Scrape tweet and return
    latest_tweet = twitter_soup.find("p", "tweet-text").text
    return latest_tweet

# Mars Facts
def mars_facts():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_df = tables[0]
    mars_df.columns = ['Property', 'Value']
    mars_df.set_index('Property', inplace=True)
    
    # Convert to HTML table string and return
    return mars_df.to_html()

def hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    html = browser.html
    hemi_soup = BeautifulSoup(html, 'html.parser')

    # Retreive mars hemispheres information
    items = hemispheres_soup.find_all('div', class_='item')

    # Create empty hemisphere url list 
    hemi_image_urls = []

    main_url = 'https://astrogeology.usgs.gov'

    # Loop to obtain title and image url
    for i in items: 
        title = i.find('h3').text
    
        image_url = i.find('a', class_='itemLink product-item')['href']
    
        browser.visit(hemispheres_main_url + image_url)
    
        img_html = browser.html
        image_soup = BeautifulSoup(img_html, 'html.parser')
    
        img_url = main_url + image_soup.find('img', class_='wide-image')['src']
    
        # Append obtained informatoin to list
        hemi_image_urls.append({"title" : title, "img_url" : img_url})

    return hemi_image_urls

def scrape():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    
    news_title, news_p = mars_news(browser)
    featured_image_url = featured_image(browser)
    mars_weather = twitter_weather(browser)
    facts = mars_facts()
    hemi_image_urls = hemispheres(browser)

    data = {
        "title": news_title,
        "paragraph": news_p,
        "featured_image": featured_image_url,
        "weather": weather_tweet,
        "mars_facts": facts,
        "hemispheres": hemi_image_urls,
    }
    browser.quit()
    return data 

    
