from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    newsurl = 'https://redplanetscience.com/'
    browser.visit(newsurl)
    html = browser.html
    newsoup = bs(html, 'html.parser')

    title = newsoup.find('div', class_='content_title').text
    pgraph = newsoup.find('div', class_='article_teaser_body').text


    picurl = 'https://spaceimages-mars.com/'
    browser.visit(picurl)
    pichtml = browser.html
    picsoup = bs(pichtml, 'html.parser')

    pic = picsoup.find('img', class_='thumbimg')
    picsrc = pic['src']
    featured_image_url = picurl + picsrc

    dataurl = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(dataurl)
    marsdata = tables[0]
    header = marsdata.iloc[0]
    marsdata = marsdata[1:]
    marsdata.columns = header

    marsdata = marsdata.set_index("Mars - Earth Comparison")

    marshtml = marsdata.to_html()

    hemiurl = 'https://marshemispheres.com/'
    browser.visit(hemiurl)    
    hemihtml = browser.html
    hemisoup = bs(hemihtml, 'html.parser')

    results = hemisoup.find_all('div', class_='description')

    
    hemisphere_pic_urls = []

    for result in results:
        

        #find the title and href and add it to the base url
        title = result.h3.text
        href = result.find('a')['href']
        tempurl = url + href
        
        # go to temp url and find high res image link
        browser.visit(tempurl)
        hemihtml = browser.html
        hemisoup = bs(hemihtml, 'html.parser')
        imagesrc = hemisoup.find('img', class_="wide-image")['src']
        imageurl = url + imagesrc


        temp_dic = {}
        temp_dic['title'] = title
        temp_dic['img_url'] = imageurl
        hemisphere_pic_urls.append(temp_dic)

        mars_dict = {
            "news_title": title,
            "news_p": pgraph,
            "featured_image_url": featured_image_url,
            "mars_table" : str(marshtml),
            "hemisphere_image_urls": hemisphere_pic_urls
        }

    browser.quit()
    print(mars_dict)

    return mars_dict

        
