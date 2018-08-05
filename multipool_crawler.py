import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from multiprocessing import Pool


def get_html(url):
    r = requests.get(url)  # Response
    return r.text


def get_all_links(html, base=None):
    soup = BeautifulSoup(html, 'lxml')
    prep = soup.find('div', class_='ReactVirtualized__Grid ReactVirtualized__Table__Grid').find_all('a')
    links = []
    for a in prep:
        link = a.get("href")
        if link is not None:
            # print(a.get("href"))
            if base is not None:
                links.append(base+link)
            else:
                links.append(link)
    return links

# <span class="h0o2f9-1 bztrIH"...> ... </span>


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    price = ""
    name = ""
    try:
        name = soup.find("span", class_ ="h0o2f9-1 bztrIH").text.strip()
        price = soup.find("div", class_ ="s62mpio-0 eBbTse").text.strip()
    except Exception as e:
        print("...")
    data = {'name': name,
            'price': price}
    return data


def write_csv(data):
    with open('marketplace.csv', 'a') as file:
        writer = csv.writer(file)

        writer.writerow((data['name'], data['price']))
        print(data['name'], 'parsed. ')


def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)


def main():
    url = 'https://www.binance.com/ru'

    start = datetime.now()
    all_links = get_all_links(get_html(url), 'https://www.binance.com')

    """  for index, value in enumerate(all_links):
        html = get_html(value)
        data = get_page_data(html)
        write_csv(data, index)
    """
# map(function, list_, ) берёт элемент из list и передаёт в function


    with Pool(100) as pool:
        pool.map(make_all, all_links)

    end = datetime.now()
    total = end - start
    print(str(total))

if __name__ == '__main__':
    main()
