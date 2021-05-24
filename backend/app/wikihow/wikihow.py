import requests
import json
import bs4

api = 'https://pt.wikihow.com/api.php?format=json&action='

def info_article(id):
    article_details = {}
    r = requests.get(api + 'query&prop=info|templates|categories&inprop=url&pageids=' + str(id))
    data = r.json()
    article_details['url'] = data['query']['pages'][str(id)]['fullurl']
    article_details['title'] = data['query']['pages'][str(id)]['title']
    if 'templates' not in data['query']['pages'][str(id)]:
        article_details['is_stub'] = False
    else:
        templates = data['query']['pages'][str(id)]['templates']
        if not any(d['title'] == 'Template:Stub' for d in templates):
            article_details['is_stub'] = False
        else:
            article_details['is_stub'] = True
    if 'categories' not in data['query']['pages'][str(id)]:
        article_details['low_quality'] = True
    else:
        categories = data['query']['pages'][str(id)]['categories']
        if not any (d['title'] == 'Category:Articles in Quality Review' for d in categories):
            article_details['low_quality'] = False
        else:
            article_details['low_quality'] = True
    return article_details

def get_images(id):
    images = []
    r = requests.get(api + 'parse&prop=images&pageid=' + str(id))
    data = r.json()
    image_list = data['parse']['images']
    for i in image_list:
        im_data = requests.get(api + 'query&titles=File:' + i + '&prop=imageinfo&iiprop=url')
        image_info = im_data.json()
        pages = image_info['query']['pages']
        for key in pages.keys():
                image_url = pages[key]['imageinfo'][0]['url']
        images.append(image_url)
    return images

def search(search_term):
    search_results = []
    r = requests.get(f'{api}query&format=json&utf8=&list=search&srsearch={search_term}')
    data = r.json()
    data = data['query']['search']
    for result in data:
        listing = {}
        details = info_article(result['pageid'])
        listing['title'] = result['title']
        listing['article_id'] = result['pageid']
        listing['url'] = details['url']
        listing['images'] = get_images(result['pageid'])
        search_results.append(listing)
    return search_results