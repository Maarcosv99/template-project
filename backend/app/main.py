from fastapi import FastAPI
from .wikihow.wikihow import search

app = FastAPI(
    title='API Wikihow',
    description='Scraping do WikiHow Brasileiro',
    version='1.0.0'
)

@app.get('/search')
def search_article(term: str):
    print('Eae')
    return search(term)