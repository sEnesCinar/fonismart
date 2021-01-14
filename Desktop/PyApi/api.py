from flask import Flask, jsonify, request, Response
import flask
import requests
import urllib
import random
from bs4 import BeautifulSoup
import xml.etree.ElementTree as et

app = Flask(__name__) 
app.config["JSON_SORT_KEYS"] = False

products = []

strs = ['1','2','3','4','B','A','S','E']
str1 = ""

ids = ["104364", "103591"]

def getProducts():
    root = et.Element('root')
    for id in ids:
        i = i+1
        random.shuffle(strs)
        uniq = str1.join(strs)

        bilgiler = []
        renkstok = []
        renkisim = []

        r = requests.get('https://www.akilliphone.com/incele/{0}'.format(id))
        soup = BeautifulSoup(r.content, "lxml")

        
        info = soup.find("div", attrs={"id": "product-info-main"})

        name = soup.find("h1", attrs={"class": "page-title"})

        fiyatFind = info.find("span", attrs={"class": "price"}).text

        categories = soup.find("ol", attrs={"class": "breadcrumb no-hide"})
        categoryLi = categories.find_all("li")
        category = []
        for c in categoryLi:
            cat = c.find("a")
            category.append(cat)

        diger = info.find_all('div', attrs={"class": "product-code"})

        for stor in diger:
            bilgiler.append(stor.strong.text.splitlines())

        renklist = info.find('ul', attrs={"class": "swatch-attribute-options"})
        renkler = renklist.find_all('li')
        #print(renkler)
        for deger in renkler:
            renkstok.append(deger["data-count"])
            renkisim.append(deger["title"])
        renkstok = [float(f) for f in renkstok]

        deschtml = str(soup.find("div", attrs={"id" : "description"}))

        isim = name.text.strip()
        fiyat = fiyatFind.replace('TL', '').strip()
        marka = bilgiler[0][1].strip()
        stok = str(sum(renkstok))
        kategori = category[1].text.strip()

        item = et.Element('item')
        root.append(item)

        stockCode = et.SubElement(item, 'stockCode')
        stockCode.text = uniq

        label = et.SubElement(item, 'label')
        label.text = isim
            
        status = et.SubElement(item, 'status')
        status.text = "1"

        brand = et.SubElement(item, 'brand')
        brand.text = marka

        mainCat = et.SubElement(item, 'mainCategory')
        mainCat.text = kategori

        price1 = et.SubElement(item, 'price1')
        price1.text = fiyat

        stockAmount = et.SubElement(item, 'stockAmount')
        stockAmount.text = stok

        details = et.SubElement(item, 'details')
        details.text = deschtml

        variants = et.SubElement(item, 'variants')
        a = 0
        for renk in renkler:
            variant = et.SubElement(variants, 'variant')

            vstockAmount = et.SubElement(variant, 'vStockAmount')
            vstockAmount.text = str(renkstok[a])

            vPrice1 = et.SubElement(variant, 'vPrice1')
            vPrice1.text = fiyat

            options = et.SubElement(variant, 'options')
            option = et.SubElement(options, 'option')

            variantName = et.SubElement(option, 'variantName')
            variantName.text = "Renk"

            variantValue = et.SubElement(option, 'variantValue')
            variantValue.text = renkisim[a]

            a = a+1
            
            
            #VARYANTLARI EKLEMELİSİN YOKSA YAPTIĞIN PROGRAM BİR BOKA YARAMAZ

        xml = et.tostring(root, encoding="unicode")

    return Response(xml, mimetype='text/xml')

@app.route('/', methods=["GET"])
def home():
    return "<h1>Hello World</h1><p>Bu site bir denemedir.</p>"

@app.route("/api/products", methods=['POST'])
def product():
    return getProducts()
    
app.run()