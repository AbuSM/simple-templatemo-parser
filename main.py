import requests
import time
from bs4 import BeautifulSoup


def get_download_links():
    url_base = 'https://templatemo.com'

    names = []
    urls = []
    links = []
    for page in range(1, 48):
        url_search = 'https://templatemo.com/page/' + str(page)
        response = requests.get(url_search)

        soup = BeautifulSoup(response.text, "html.parser")
        for one_a_tag in soup.findAll('a'):
            link = one_a_tag['href']
            print('parsing link: ', link)
            if link[0:3] == '/tm' and link not in links:
                links.append(link)
                redirect_link = url_base + link
                new_response = requests.get(redirect_link)
                soup2 = BeautifulSoup(new_response.text, "html.parser")
                for second_a_tag in soup2.findAll('a'):
                    text = second_a_tag.getText()
                    if text == 'Download':
                        link2 = second_a_tag['href']
                        download_url = url_base + link2
                        print('url: ', download_url)
                        urls.append(download_url)
                        name = link[link.find('/turnstile_') + 1:].replace('/tm-', '')
                        names.append(name)
                        print('name: ', name)
                        open('./links.txt', 'a+').write(f'Name: {name}\nUrl: {download_url}\n------\n')
    print('got names: ', names)
    print('got urls: ', urls)
    return names, urls


def get_urls_from_file(filename):
    urls = []
    names = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    for l in lines:
        line = str(l)
        if line.find('Url:') > -1:
            urls.append(line.replace('Url: ', ''))
        elif line.find('Name:') > -1:
            names.append(line.replace('Name: ', ''))

    return names, urls


def download_files_by_links(names, urls):
    for (name, url) in zip(names, urls):
        print('Downloading %s' % url)
        response = requests.get(url)
        open('./templates/' + name + '.zip', 'a+b').write(response.content)
        print('File %s completely downloaded' % name)


if __name__ == '__main__':
    start_time = time.time()
    names, urls = get_urls_from_file('./links.txt')
    download_files_by_links(names, urls)
    print('Finished in: %s' % (time.time() - start_time))

