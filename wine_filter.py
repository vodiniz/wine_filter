#get all wine type 
from logging import exception
import requests, json
from bs4 import BeautifulSoup


class Wine():
    def __init__(self, name, price, score, url, country, wine_type, bundle):
        self.name = name
        self.price = price
        self.score = score
        self.url = url
        self.country = country
        self.type = wine_type
        self.bundle = bundle
        self.name_type_tuple_list = []


    def update_bundle(self,wine_tuple):
        if self.bundle:
            self.name_type_tuple_list.append(wine_tuple)
    
    def print_wine(self):
        print('----------------')
        print(self.name)
        print('Preço:',self.price)
        print('Nota: ',self.score,'/5')
        print('Link: ',self.url)
        print('País: ',self.country)
        if self.bundle:
            print('Vinhos do kit')
            for element in self.name_type_tuple_list:
                print('Vinho :', element[0])
                print('Classificação:', element[1])
                print(' ')



def check_invalid_page(page_soup):
    url_error = page_soup.find('h2',{'class':'Title-title'}).getText().rstrip()
    if url_error == 'erro 400':
        return True


def check_bundle(soup):
    name = (soup.find('div',{'class':'hidden-xs hidden-sm'})).\
        find('h1').get_text()
    return 'Kit' in name

def get_wine_url_list(page_number,out_of_page):
    url = "https://www.wine.com.br/vinhos/cVINHOS-p{}.html".format(page_number)
    url_request = requests.get(url)
    soup = BeautifulSoup(url_request.content, "html.parser")
    wines = soup.find_all('article',{'class':'ProductDisplay ProductDisplay--horizontal'})
    wine_url_list = []
    for wine in wines:
        wine_url_list.append('https://www.wine.com.br'+ wine.find('a',{'class':'js-productClick'}).get('href'))
    out_of_page = check_invalid_page(soup)
    return wine_url_list

def get_wine_name(soup):
    return (soup.find('div',{'class':'hidden-xs hidden-sm'})).\
        find('h1').get_text()

def get_wine_price(soup):
    price = (soup.find('price-box')).attrs[':product'].split(',')
    for string in price:
        if 'clubPrice' in string:
            price = string.strip().split(":")   
            price = (float(price[1]))  
    return price

def get_wine_score(soup):
    score = soup.find('li',{'class':'PageHeader-tag Rating hidden-xs'}).find('rating').attrs[':ratio']
    score = float(score)
    return score

def get_wine_country(soup):
    return soup.find('li',{'class':'PageHeader-tag'}).find('img').get('title')



def get_wine_type(soup):
    wine_classification = soup.find_all('div',{'class':'col-md-12 TechnicalDetails-description'})
    wine_type = None
    for caption in wine_classification:
        new_caption = caption.find('dt',{'class':'w-caption'})
        if new_caption.get_text() == 'Classificação':
            wine_type = caption.find('dd',{'class':'w-paragraph'}).get_text()
        return wine_type

def get_bundle_details(soup):
    wine_names = soup.find_all('div',{'class':'ProductItem'})
    name_list = []
    for wine in wine_names:
        name_list.append(wine.find('strong',{'class':'ProductItem-name'}).get_text())

    type_list = []
    captions = soup.find_all('div',{'class':'col-md-12 TechnicalDetails-description'})
    for caption in captions:
        new_caption = caption.find('dt',{'class':'w-caption'})
        if new_caption.get_text() == 'Classificação':
            type_list.append(caption.find('dd',{'class':'w-paragraph'}).get_text())
    
    return name_list, type_list


def check_desired_type(desired_type, wine):
    if desired_type == wine.type:
        return True
    for element in wine.name_type_tuple_list:
        if desired_type == element[1]:
            return True
        


def get_wine(url):
    url_request = requests.get(url)
    soup = BeautifulSoup(url_request.content, "html.parser")


    bundle = check_bundle(soup)
    if bundle:
        country = None
        name_list, type_list = get_bundle_details(soup)
        wine_type = 'kit'
    else:
        #print(country)
        country = get_wine_country(soup)

        wine_type = get_wine_type(soup)
        #print(wine_type)

    name = get_wine_name(soup)
    #print(name)

    price = get_wine_price(soup)
    #print(price)

    score = get_wine_score(soup)
    #print(score)

    
    

    
    if bundle:
        new_wine = Wine(name,price,score,url,country,wine_type,bundle)

        for name, wine_type  in zip(name_list, type_list):
            new_wine.update_bundle((name, wine_type))
        return new_wine
        
    else:
        new_wine = Wine(name,price,score,url,country,wine_type,bundle)
        return new_wine  



def main():
    out_of_page = False
    page_count = 1
    url_list = []

    wine_list = []
    filtered_list = []
    wine_json_list = []
    filtered_json_list = []


    while not out_of_page:
        url_list, page_count = get_wine_url_list(page_count, out_of_page)
        for url in url_list:
            try:
                wine = get_wine(url)
            except Exception as ex:
                print (ex)
                print(url)
                wine = Wine(None,None,None, url,None, None, False)
            wine_list.append(wine)
            wine_json_list.append(wine.__dict__)
            if check_desired_type('Suave/Doce', wine):
                wine.print_wine
                filtered_list.append(wine)
                filtered_json_list.append(wine.__dict__)
                print(filtered_json_list)
            print('-----')
            print('Page: ',page_count)
            print('Wines Done:',(len(wine_list)-1))
            print('Filtered_wines,',len(filtered_list))
        page_count += 1
        if len(wine_list) >= 903:
            out_of_page =True
        

    with open('wine_json.json', 'w') as f:
        json.dump(wine_json_list, f, indent=4)

    with open('filtered.json', 'w') as f:
        json.dump(filtered_json_list, f,  indent=4)

main()
