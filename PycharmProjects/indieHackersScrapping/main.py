from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from csv import writer
import csv
import requests

HEADERS = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}

with open("people_.csv", "a", encoding="utf-8", newline="") as f:
    header = ["Url", "Description", "Twitter", "E-Mail"]
    csv_writer = csv.writer(f, delimiter=";")
    csv_writer.writerow(header)

    list_attr = []



    #browser = webdriver.Chrome("D:\\user\\Downloads\\chromedriver1\\chromedriver.exe")

    #browser.get("https://www.indiehackers.com/")

    #browser.maximize_window()
    time.sleep(5)

    html_text = requests.get("https://www.indiehackers.com/",timeout=8, headers=HEADERS)

    html_text=html_text.text

    #html_text = browser.page_source

    soup = BeautifulSoup(html_text, "lxml")


    people = soup.find_all("a", class_="user-link__link ember-view")[:5]


    def find_people(person):
        global list_attr
        with open("urls.txt", "r") as read_urls:
            urls = read_urls.readlines()
            if person['href'] in urls:
                return
            for url in urls:
                # print(url,person['href'])
                if url.strip() == person['href']:
                    return
        with open("urls.txt", "a") as write_urls:
            write_urls.write(person['href'])
            write_urls.write('\n')
            write_urls.flush()
        list_attr.append("https://www.indiehackers.com" + person['href'])
        time.sleep(2)
        #browser.get("https://www.indiehackers.com" + person['href'])
        html_text=requests.get("https://www.indiehackers.com" + person['href'],timeout=8, headers=HEADERS)

        html_text = html_text.text
        # browser.maximize_window()
        time.sleep(8)
        #html_text = browser.page_source
        soup = BeautifulSoup(html_text, "lxml")
        print(soup.prettify())
        time.sleep(2)
        credentials = soup.find("div", class_="user-header__metadata").text.strip()

        list_attr.append(' '.join(credentials.split()))

        twitter_mail = soup.find_all("a", class_="user-header__satellite user-header__satellite--contact")

        if len(twitter_mail) == 2:
            for link in twitter_mail:
                list_attr.append(link['href'])
        elif len(twitter_mail) == 0:
            list_attr.append("")
            list_attr.append("")
        elif "mailto" in twitter_mail[0]:
            list_attr.append("")
            list_attr.append(twitter_mail[0]['href'])
        else:
            list_attr.append(twitter_mail[0]['href'])
            list_attr.append("")

        csv_writer.writerow(list_attr)
        f.flush()
        list_attr = []

        followers_div = soup.find("div", class_="users-list ember-view")

        if followers_div is None:
            return
        followers = followers_div.find_all("a", class_="user-link__link ember-view")

        if len(followers) > 5:
            followers = followers[:5]

        for follower in followers:
            if follower['href'] == person['href']:
                continue
            find_people(follower)


    for person in people:
        find_people(person)
        print("person")
