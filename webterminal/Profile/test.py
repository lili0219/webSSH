import requests
from requests.exceptions import RequestException


def get_one_page(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    try:
        if response.status_code == 200:
            return response.text
    except RequestException:
        return None


def main():
    url = 'http://maoyan.com/board'
    html = get_one_page(url)
    print(html)


if __name__ == '__main__':
        main()