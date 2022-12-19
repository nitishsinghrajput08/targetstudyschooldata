import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/102.0.0.0 Safari/537.36'}
data_name=[]
data_locality=[]
data_city=[]
data_phone_no=[]
data_dct=[]
URLs = ['https://targetstudy.com/school/schools-in-chandigarh.html','https://targetstudy.com/school/schools-in-panchkula.html','https://targetstudy.com/school/schools-in-mohali.html']
for url in URLs:
    r=requests.get(url, headers=headers )
    soup=bs(r.text,'html.parser')
    def extract_data():
        s=soup.find_all('div',attrs={'class':'col-12'})
        for i in s:
            title=i.find('h4')
            if title:
                name=title.text
                data_name.append(name)
            address=i.find('p')
            try:
                li=address.find_next('i')
                for i in li:
                    locality=i.next.text
                    data_locality.append(locality)
                    city=i.next.next.next.text[2:]
                    data_city.append(city)
            except:
                print("no data")         
        for i in s:
            content=i.find('p')
            try:
                li=content.find_next('i')
                for i in li:
                    phone_no = i.next.next.next.next.next.next.next.next.text
                    data_phone_no.append(phone_no)
            except:
                print("no data")  
        for i in s:
            data_details=[]
            content=i.find('ul', attrs={"class":"list-info"})
            try:
                c2=content.find_all('li')
                for i in c2:
                    detail=i.text
                    data_details.append(detail)
                data_dct.append(data_details)
            except:
                print('no data')
    # dataframe = pd.DataFrame(data_dct)
    # dataframe.to_csv("details_Data.csv" , mode = 'a', header=False, index=False)
    extract_data()
    s=soup.find('ul',attrs={'class':'pagination'})
    pages=s.find_all('a')[:-1]
    for link in pages:
        page = requests.get(url + link['href'], headers=headers )
        soup = bs(page.content, 'html.parser')
        extract_data()
        

all_Data={'School Name':data_name,
          'Locality':data_locality,
          'City':data_city,
          'Phone Number':data_phone_no,
          'Details':data_dct
          }
df = pd.DataFrame(all_Data)
df.to_csv("targetstudy_school_data.csv")