from lxml import html
import requests


'''This file scrapes each page of Blue Apron for a pdf link and, if possible, downloads the recipe file'''

inum = 122

while inum < 1094:

    recipe = 'https://www.blueapron.com/recipes/' + str(inum)

    page = requests.get(recipe)  # get the page data
    tree = html.fromstring(page.content)  # turns page html into bytes

# xpath searches the tree for all <a> with class 'pdf-download-link' and returns the href value as a string
    url = str(tree.xpath('//a[@class="pdf-download-link"]/@href'))

    for char in url:
        if char in "[']":
            url = url.replace(char, '')

    if url == '':  # 404s result in blank strings so we only write successful pulls to pdf
        inum += 1
    else:
        file_name = url.split('/')[-1]  # This grabs the final part of the url to get an accurate file name
        print(file_name)
        print(url)
        with open(file_name, 'wb') as pdf:
            a = requests.get(url, stream=True)
            for block in a.iter_content(512):
                if not block:
                    break
                pdf.write(block)
        inum += 1

print('Test')
