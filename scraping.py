# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    img_url, title = hemi_info(browser)
    # Run all scraping functions and store results in dictionary
    data = { 'data': {'news_title': news_title}, 'news_paragraph':news_paragraph, 'featured_image':featured_image(browser), 'facts':mars_facts,'last_modified':dt.datetime.now(),
                'hemi_data': {'hemi_title': title}, 'hemi_url':img_url}
    


    # Stop webdriver and return data    
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    #Add a try element
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p

# ### Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

def mars_facts():
    try:
        # Use pandas to read the HTML data box w/o needing to parse it. And input it into our own dataframe 
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None 
    #Assign columns and set index of data frame
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    #Put the dataframe back into HTML that way it's live. 
    return df.to_html(classes= "table table-stripped")

def hemi_info(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # 3. Write code to retrieve the image urls and titles for each hemisphere
    for i in range(4):
        #create empty dictionary
        hemispheres = {}
        browser.find_by_css('a.product-item h3')[i].click()
        element = browser.find_link_by_text('Sample').first
        img_url = element['href']
        title = browser.find_by_css("h2.title").text
        hemispheres["img_url"] = img_url
        hemispheres["title"] = title
        hemisphere_image_urls.append(hemispheres)
        browser.back()
        # 4. Print the list that holds the dictionary of each image url and title.
        
        return hemispheres, hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())




