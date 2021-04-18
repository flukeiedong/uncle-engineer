from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
import time


# Don't open the browser
opt = wd.ChromeOptions()
opt.add_argument('headless')


# Open chrome
PATH = "/Users/los_napath/PycharmProjects/Uncle Engineer/Twitter Scrapping/chromedriver"
driver = wd.Chrome(PATH, options=opt)


def scroll(loop=10):
    for k in range(loop):
        depth = str(5000*(k+1))
        driver.execute_script("window.scrollTo(0," + depth + ")")
        time.sleep(1)


def format_user(raw_user):
    username = raw_user.replace("\n", "")
    username = username.replace("\u200f\xa0", "\t")
    try:
        username = username.replace("Verified account", "")
    except:
        pass
    return username


def hashtag(name):
    url = "https://twitter.com/hashtag/" + name
    driver.get(url)

    scroll()

    page_html = driver.page_source

    data = soup(page_html, "html.parser")

    tweet_user = data.findAll("a", {"class": "account-group js-account-group js-action-profile js-user-profile-link js-nav"})
    tweet_text = data.findAll("p", {"class": "TweetTextSize"})

    for i, tw in enumerate(zip(tweet_user, tweet_text)):
        print(i)
        print(format_user(tw[0].text))
        print(tw[1].text)
        print("-----------------------------------------------------")

    driver.close()
    print("CLOSED DRIVER")


hashtag("หนุ่มแว่น")
print("Total time", time.process_time())
