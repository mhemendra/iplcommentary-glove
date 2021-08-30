import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver

def geturls():
    #homepage = 'https://www.espncricinfo.com/series/ipl-2020-21-1210595/match-results'
    #homepage = 'https://www.espncricinfo.com/series/ipl-2019-1165643/match-results'
    homepage='https://www.espncricinfo.com/series/ipl-2018-1131611/match-results'
    page = requests.get(homepage)
    soup = BeautifulSoup(page.content, 'html.parser')
    fixtures = soup.find(class_='card content-block league-scores-container').findAll(class_='match-info-link-FIXTURES')
    commentaryUrls = []
    for fixture in fixtures:
        href = fixture.get('href')
        url = 'https://www.espncricinfo.com'+href.replace('full-scorecard','ball-by-ball-commentary')
        commentaryUrls.append(url)
    return commentaryUrls

def convert_pd(driver):
    SCROLL_PAUSE_TIME = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser').find(class_='match-body')
    comments = soup.findAll(class_='match-comment')
    overs = []
    short_texts = []
    long_texts =[]
    for comment in comments:
        over = comment.find(class_='match-comment-over').text
        short_text = comment.find(class_='match-comment-short-text').text
        long_data = comment.find("div", {"class": "match-comment-long-text", "itemprop":"articleBody"})
        if long_data is None:
            long_text = ""
        else:
            long_text = long_data.text
        overs.append(over)
        short_texts.append(short_text)
        long_texts.append(long_text)

    commentary_data = pd.DataFrame({
        "over":overs,
        "short_text":short_texts,
        "long_text":long_texts
    })
    return commentary_data

def getMatchCommentary(url):

    driver.get(url)
    #Adding below line to handle super overs, Super over is actually li[3] so li[2] selects second innings as usual
    driver.find_element_by_xpath(
        "//section[@id='main-container']/div/div[2]/div[2]/div/div[2]/div/div/div/button/i").click()
    driver.find_element_by_xpath(
        "//section[@id='main-container']/div/div[2]/div[2]/div/div[2]/div/div/div/div/ul/li[2]").click()

    # Get scroll height
    commentary_data_first = convert_pd(driver)
    driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")

    driver.find_element_by_xpath(
        "//section[@id='main-container']/div/div[2]/div[2]/div/div[2]/div/div/div/button/i").click()
    try:
        driver.find_element_by_xpath(
        "//section[@id='main-container']/div/div[2]/div[2]/div/div[2]/div/div/div/div/ul/li").click()
    except:
        driver.find_element_by_xpath(
            "//section[@id='main-container']/div/div[2]/div[2]/div/div[2]/div/div/div/div/ul/li[2]/span").click()
    commentary_data_second = convert_pd(driver)
    commentary_data = pd.concat([commentary_data_first, commentary_data_second], axis=0)
    return commentary_data

if __name__ == '__main__':
    chrome_driver = r'D:\Downloads\chromedriver\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chrome_driver)
    mainDF = pd.DataFrame(columns=["over", "short_text", "long_text"])
    #commentaryUrls = ["https://www.espncricinfo.com/series/ipl-2019-1165643/chennai-super-kings-vs-royal-challengers-bangalore-1st-match-1175356/ball-by-ball-commentary"]
    commentaryUrls = geturls()
    for url in commentaryUrls:
        commentary = getMatchCommentary(url)
        mainDF = pd.concat([mainDF, commentary], axis=0)
    driver.quit()
    mainDF.to_csv(r'data\commentary_data.csv', index = None, header=True)
