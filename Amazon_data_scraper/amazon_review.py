import requests
from bs4 import BeautifulSoup
import pandas as pd



headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
url='https://www.amazon.in/Colgate-Advanced-Ayurvedic-Solution-Toothpaste/product-reviews/B09DP9K9CF/ref=cm_cr_getr_d_paging_btm_next_5?ie=UTF8&pageNumber=1'

#page=requests.get(url,headers=headers)



reviewlist=[]


def get_soup(url):
    r=requests.get(url,headers=headers)
    #r=requests.get('http//localhost:8050/render.html',params={'url':url,'wait':2})
    soup = BeautifulSoup(r.content,'html.parser')
    #soup= BeautifulSoup(r.text,'html.parser')
    return soup


def get_reviews(soup):
    reviews = soup.find_all('div',{'data-hook':'review'})
    try:
        for item in reviews:
            review={
                
            'name' :item.find('span', {'class':"a-profile-name"}).text.strip(),

            'rating':float(item.find('i',{'data-hook':'review-star-rating'}).text.replace('out of 5 stars','').strip()),
            'title':item.find('a',{'data-hook':'review-title'}).text.strip(),
            
            'reviews' :item.find('span',{'data-hook':'review-body'}).text.strip(),
            }
            reviewlist.append(review)
            
    except:
        pass
            
            

for x in range(1,6):
    soup =get_soup(f'https://www.amazon.in/Colgate-Advanced-Ayurvedic-Solution-Toothpaste/product-reviews/B09DP9K9CF/ref=cm_cr_getr_d_paging_btm_next_5?ie=UTF8&pageNumber={x}')
    print(f'Getting page:{x}')
    get_reviews(soup)
    print(len(reviewlist))
    if not soup.find('li',{'class':'a-disabled a-last'}):
        pass
    else:
        break
    
df=pd.DataFrame(reviewlist)
df.to_csv('colagate_reviews.csv',index=False)

