from bs4 import BeautifulSoup
import csv
import html5lib
from urllib.request import urlopen
import schedule
import time
import datetime
import redis
class articulo:
    titulo=''
    link=''
    contenido=''

def scrape():
    listaArticulos=[]
    print(datetime.datetime.now())
    soup = BeautifulSoup(urlopen("http://www.eltiempo.com"),'html5lib')
    for unArticulo in soup.find_all('div',class_="main_article"):
        nuevoArticulo=articulo()
        nuevoArticulo.titulo=unArticulo.a.string
        nuevoArticulo.link=unArticulo.a['href']
        nuevoArticulo.contenido=""


        if nuevoArticulo.link.startswith('/'):
            nuevoArticulo.link= "http://www.eltiempo.com" + nuevoArticulo.link
        noodles = BeautifulSoup(urlopen(nuevoArticulo.link),'html5lib')
        nuevoArticulo.contenido = (noodles.find('div',id="contenido"))
        listaArticulos.append(nuevoArticulo)






    store(listaArticulos)
    with open("output.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["titulo", "link", "contenido"])
        for a in listaArticulos:
            print(a.titulo)
            writer.writerow([a.titulo,a.link, a.contenido])
    print(datetime.datetime.now())

def store(content):
    r = redis.StrictRedis(host='redis://h:pa0a474b04ddb82c4670e2fe833833ae4736b85e531a767925c17d2ab36e03ff3@ec2-54-235-101-32.compute-1.amazonaws.com', port=20829, db=0)
    r.set('news' , content)



scrape()
schedule.every(5).minutes.do(scrape)

while True:
    schedule.run_pending()
    time.sleep(1)
