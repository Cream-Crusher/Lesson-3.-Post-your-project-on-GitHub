import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


def get_short_link(token, parameters):
    authorization_header = {
        'Authorization': 'Bearer {}'.format(token)
    } 
    url = 'https://api-ssl.bitly.com/v4/shorten'
    bitlink = requests.post(
        url,
        json=parameters,
        headers=authorization_header
    )
    bitlink.raise_for_status()
    bitlink = bitlink.json()
    return bitlink['link']


def get_clicks_count(token, bitlink):
    authorization_header = {
        'Authorization': 'Bearer {}'.format(token)
    } 
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(
        (urlparse(bitlink).netloc+urlparse(bitlink).path))
    clicks_count = requests.get(url, headers=authorization_header)
    clicks_count = clicks_count.json()['total_clicks']
    return clicks_count

if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('BITLY_TOKEN') 
    parser = argparse.ArgumentParser(
        description='Описание что делает программа')
    parser.add_argument('link', help='введите ссылку')
    link = parser.parse_args() 
    link = (link.link)
    if link.startswith('https://bit.ly/'):
        print(get_clicks_count(token, link))
    else:
        parameters = {'long_url': link}
        bitlink = get_short_link(token, parameters)
        print(bitlink)
        
        
        
   