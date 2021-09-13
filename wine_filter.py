#get all wine type 
import requests
from bs4 import BeautifulSoup


class Wine():
    def __init__(self, name, price, score, url, wine_type, bundle):
        self.name = name
        self.price = price
        self.score = score
        self.url = url
        self.type = wine_type
        self.bundle = bundle
        self.bundle_wine_list = None


    def update_bundle(self,wine_list):
        if self.bundle:
            self.bundle_wine_list = []

            for wine in wine_list:
                wine.append(self.bundle_wine_list)

            


url = "https://www.wine.com.br/vinhos/cVINHOS-p1.html"
url_request = requests.get(url)
soup = BeautifulSoup(url_request.content,'html.parser')

out_of_url = "https://www.wine.com.br/vinhos/cVINHOS-p104.html"
out_of_url_request = requests.get(out_of_url)
soup2 = BeautifulSoup(out_of_url_request.content,'html.parser')
import requests

def check_invalid_page(page_soup, out_of_page):
    url_error = page_soup.find('h2',{'class':'Title-title'}).getText().rstrip()
    if url_error == 'erro 400':
        return True

def get_wine_details(url):
    url_request = requests.get(url)
    soup = BeautifulSoup(url_request.content, "html.parser")
    name = soup.find('h1',{'class':'PageHeader-title w-title--4  text-center '})
    print(name)

def get_wine_url_list(page_number):
    url = "https://www.wine.com.br/vinhos/cVINHOS-p{}.html".format(page_number)
    url_request = requests.get(url)
    soup = BeautifulSoup(url_request.content, "html.parser")
    wines = soup.find_all('article',{'class':'ProductDisplay ProductDisplay--horizontal'})
    wine_url_list = []
    for wine in wines:
        wine_url_list.append('https://www.wine.com.br'+wine.find('a',{'class':'js-productClick'}).get('href'))
    print(wine_url_list)
    



def main():
    out_of_page = False
    page_count = 1

    wine_list = []
    filtered_list = []
   #wine_url_list = get_wine_url_list(page_count)
    get_wine_details('https://www.wine.com.br/vinhos/champagne-montaudon-brut-/prod3170.html')

    # while not out_of_page:
    #     print('hello')



main()
