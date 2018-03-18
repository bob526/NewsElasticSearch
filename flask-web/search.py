from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
app = Flask(__name__)
es = Elasticsearch()

@app.route('/')
def search_main():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    searchtext=request.args.get('searchtext', '')
    
    searchDSL = {
        "query": {
            #match or term or range": {col: keyword}
            "match": {"content" : searchtext}
        }
    }

    searchrespond = es.search(index="news", body=searchDSL)
    #Process searchrespond
    return '<h1>Hits: '+str(searchrespond['hits']['total'])+'</h1>'


```
Helpful site:
https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html
https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.search
https://elasticsearch-py.readthedocs.io/en/master/#example-usage

```