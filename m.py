import requests
import json
import logging as logger
import time

OUTPUT_FOLDER=r"C:\Users\Sohom\Desktop\Scrapping\results.txt"
zip_list=[]

# "07001-08989","87001-88439","00501-14925","27006-28909","58001-58856","43001-45999","73001-74966","97001-97920","15001-19640","29001-29945"


lst2=set()
def find(set1):
    lst1=set()
    for j in set1:
        #print(j)
        try:
            time.sleep(10)
            url_link=requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{j}.json?limit=5&types=country%2Cregion%2Cpostcode%2Cdistrict%2Cplace%2Clocality%2Cneighborhood&language=en-GB&access_token=pk.eyJ1IjoibmF0aW9uYWxkb2dncm9vbWVycyIsImEiOiJjazdvajJzdGMwOXozM2xxcjdrMWttcWNwIn0.9V2c_eNIEBHDynOxKQ_2hQ').text
            data_json=json.loads(url_link) #dictonary
            coordinates=data_json["features"][0]["center"]
            #radius=input("Enter radius(5/10/25/50/100)mi: ")
            url_link_new=requests.get(f'https://api.storepoint.co/v1/15e69f8fd44f25/locations?lat={coordinates[1]}&long={coordinates[0]}&radius=50').text
            data=json.loads(url_link_new)
            final_data=data["results"]["locations"]
            lst1.add(j)
            #count=count+1
            with open(OUTPUT_FOLDER, 'a') as f: 
                for i in final_data:
                    f.write(f'Zip: {j}\n')
                    f.write(f'Name: {i["name"]}\n')
                    f.write(f'Description: {i["description"]}\n')
                    f.write(f'Address: {i["streetaddress"]}\n')
                    f.write(f'Website: {i["website"]}\n')
                    f.write(f'Phone number: {i["phone"]}\n\n')
        except requests.exceptions.ConnectionError as e:
            logger.error(f'Connection failed..')
        except:
            lst1.add(j)
            logger.error(f"Zip doesn't exist")
    return lst1
def scrape():
    for k in zip_list:
        zip=k.split("-")
        set1=set(range(int(zip[0]),int(zip[1])+1))
        lst1=find(set1)
        print(lst1)
        lst2=set1.difference(lst1)
        print(lst2)
        while len(lst2)!=0:
            lst2=lst2.difference(find(lst2))

if __name__=="__main__":
    scrape()