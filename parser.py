from bs4 import BeautifulSoup as bs
import requests

def get_requests(url):
    response = requests.get(url)
    return response.text

def get_data(html):
    soup = bs(html, 'lxml')
    catalog = soup.find('div', class_='items-container')
    hotels = catalog.find_all('li', class_='item')

    li = []
    for hotel in hotels:
        try:
            title = hotel.find('div', class_='item-name tile-header clearfix').text.strip()
        except:
            title = ''

        try:
            rating = hotel.find('span', class_='d-block rating-value').text
        except:
            rating = ''

        try:
            ratingcount = hotel.find('span', class_='d-block reviews').text.strip()
        except:
            ratingcount = ''

        try:
            image = hotel.find('img').get('src')
            print(image)
        except:
            image = ''

        data = {
            'title': title,
            'rating': rating,
            'ratingcount': ratingcount,
            'image': image
        }
        li.append(data)
    return li

def main():
    url = 'https://101hotels.com/kyrgyzstan/cholpon-ata'
    html = get_requests(url)
    get_data(html)
    return get_data(html)

if __name__ == '__main__':
    main()
