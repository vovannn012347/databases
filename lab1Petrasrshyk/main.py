import urllib;
from lxml import html;
from lxml.html.clean import clean_html;
from lxml import etree;

url1 = "http://isport.ua/"
url2 = "http://portativ.ua/category_841832.html?limit=20&mode=list"

def task1():
    page = html.fromstring(urllib.urlopen(url1 ).read())

    head = url1 .split('/', 3)[2]

    returndoc = etree.Element("data")
    analyzepages = page.xpath("//a[contains(@href, '" + head + "')]/@href")

    if analyzepages[0] != url1 :
        analyzepages.insert(0, url1 );

    analyzepages = analyzepages[0:21]

    for curpage in analyzepages:

        page = html.fromstring(urllib.urlopen(curpage).read())

        elempage = etree.SubElement(returndoc, "page")
        elempage.set("url", curpage)

        textlist = clean_html(page).xpath("//text()")
        imagelist = clean_html(page).xpath("//img/@src")

        for i in textlist:
            i = i.strip()
            if i:
                etree.SubElement(elempage, "fragment", type="text").text = unicode(i);

        for i in imagelist:
            if (i.startswith("http://")):
                etree.SubElement(elempage, "fragment", type="image").text = unicode(i);

    f = open("lab1task1.xml", "w")
    f.write(etree.tostring(returndoc, encoding=unicode, pretty_print=True).encode("utf-8"))

def task2():

    page = html.fromstring(urllib.urlopen(url1).read())

    analyzepages = page.xpath("//a/@href")

    for e in analyzepages:
        if (e.startswith("http://") or e.startswith("https://")):
            print(e)

def task3():

    page = html.fromstring(urllib.urlopen(url2).read())

    products = page.xpath("//div[@class = 'cataloglistline-item-container']")

    list = etree.Element('products')

    for product in products:
        image = product.xpath(".//img[@class = 'UI-CATALOG-PRODUCT-IMAGE'][1]/@src")[0]
        price = " ".join(product.xpath(".//span[@class = 'price']//text()"))
        descriptionlines = product.xpath(".//div[@class = 'cataloglist-item-descr']//li")
        description = str()

        for line in descriptionlines:
            description = description.__add__(" ".join(line.xpath(".//text()")) + "\n")

        etree.SubElement(list, 'product', description=description, image=image, price=price)

    et = etree.ElementTree(list)

    f = open("lab1task3.xml", "w")
    et.write(f, xml_declaration=True, encoding='UTF-8',  pretty_print=True)

def task4():
    data_file = 'lab1task3.xml'
    xslt_file = 'lab1task4.xslt'
    output_file = 'lab3task4.html'
    xslt = etree.parse(xslt_file)
    result = etree.parse(data_file).xslt(xslt)
    open(output_file, mode='w').write(str(result))
    print('Results written to', data_file)

def main():
    #task1()
    #task2()
    #task3()
    task4()

if __name__ == '__main__':
    main()