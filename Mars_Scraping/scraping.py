# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    #set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)
    
    #run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_images(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_image_urls
    }
      # Stop webdriver and return data
    browser.quit()
    return data



def mars_news(browser):
    #scrape mars news
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #convert thr browser html to a soup obejct and then quit the broswer
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one('div.list_text')
        
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        #Use the parent function to find the paragraph text 
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
   
    #add a return statement
    return news_title, news_paragraph


### JPL Space images featured image

def featured_images(browser):
    
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        # Find the relative image URL
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    #Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# ### Mars Facts
def mars_facts():
    try:
        #use 'read html' to scrape facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    except BaseException:
        return None
    
    #assign columns and set index to dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)  
      
    #convert table to html format
    return df.to_html(classes="table table-striped")



###Mars Hemispheres images
def hemisphere_image_urls():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.    
    hemisphere_image_urls = []
    
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    img_soup = soup(html, 'html.parser')

        
    items = img_soup.find_all('div', class_='item')
    ### Hemispheres
    try:
        for item in items:
            
            hemispheres = {}
            
            title = item.find('h3').get_text()
            
            page_href=item.find('a').get('href')
            browser.visit(f'https://marshemispheres.com/{page_href}')    
            
            html2 = browser.html
            img_soup2 = soup(html2, 'html.parser')
            full_image = img_soup2.find('div', class_='downloads').find('a').get('href')
            
            full_image_url = f'https://marshemispheres.com/{full_image}'
            hemispheres = {
                'img_url':full_image_url,
                'title': title}
            
            hemisphere_image_urls.append(hemispheres)

            browser.back()
    except AttributeError:
        return None
        
    # 5. Quit the browser
    browser.quit()
    return hemisphere_image_urls

if __name__=="__main__":
    print(scrape_all())


        





