from bs4 import BeautifulSoup
import lxml
import requests
import json
from selenium import webdriver
import time

url = f'https://zadolba.li/'


# req = requests.get(url + str(20210405))
# src = req.text

# with open('index.html', 'w', encoding='utf-8') as f:
#     f.write(src)

def parse_page(id):
    req = requests.get(url + str(id))
    src = req.text

    soup = BeautifulSoup(src, 'lxml')

    stories_dict = {}
    stories = soup.find_all(class_='story')
    if stories == None:
        return ''
    for item in stories:
        try:
            title = ''
            if item.find('h2').find('a'):
                title = item.find('h2').find('a').text.strip()
            datetime = ''
            if item.find('time', class_='date-time'):
                datetime = item.find('time', class_='date-time').get('datetime')
            category = ''
            if item.find('ul'):
                category = [i.text for i in item.find('ul').find_all('li')]
            body = item.find(class_='text').text.strip()
        except Exception as ex:
            print(ex)

        stories_dict[title] = {
            'title': title,
            'datetime': datetime,
            'category': category,
            'body': body
        }

    return stories_dict


link = 'https://zadolba.li/20210411'

res_dict = {}


def save_selenium():
    try:
        browser = webdriver.Chrome()
        browser.get(link)

        while browser.current_url != 'https://zadolba.li/20090908':
            current_id = browser.current_url.split('/')[-1]
            # link = f'https://zadolba.li/{current_id}'
            print(current_id)
            res_dict[current_id] = parse_page(current_id)

            button = browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[1]/div/ul/li[4]/a')
            button.click()

        with open(f'data/data.json', 'w', encoding='utf-8') as f:
            json.dump(res_dict, f, indent=4, ensure_ascii=False)
    except Exception as ex:
        print(ex)

    finally:
        time.sleep(300)
        if browser.current_url == 'https://zadolba.li/20090908':
            browser.quit()


print(parse_page(20210411))

if __name__ == '__main__':
    save_selenium()
