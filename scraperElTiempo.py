from bs4 import BeautifulSoup
import csv
import html5lib
from urllib.request import urlopen
import schedule
import time
import datetime
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

    with open("output.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["titulo", "link", "contenido"])
        for a in listaArticulos:
            writer.writerow([a.titulo,a.link, a.contenido])
    print(datetime.datetime.now())


scrape()
schedule.every(5).minutes.do(scrape)

while True:
    schedule.run_pending()
    time.sleep(1)
