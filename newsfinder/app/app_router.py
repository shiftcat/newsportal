

import os
from flask import Flask, render_template, request, make_response

from elasticsearch import Elasticsearch

import pymongo
# pip install Flask-PyMongo
from flask_pymongo import PyMongo

# pip install gensim
from gensim.models import word2vec

from app.paging import Page
from app.utils import QueryString


es = Elasticsearch(host=os.getenv('ELASTICSEARCH_SERVER'), port=int(os.getenv('ELASTICSEARCH_PORT', 9200)), timeout=60)

flask_app = Flask(__name__)

flask_app.config["MONGO_URI"] = "mongodb://{}:{}/news".format(os.getenv('MONGO_SERVER'), os.getenv('MONGO_PORT', 27017))
mongo = PyMongo(flask_app)


def get_collection(col_nm):
    collection = mongo.db[col_nm]
    return collection


@flask_app.route("/")
def index():
    query_string = str(request.query_string, encoding='utf-8')
    qs = QueryString(query_string)

    pageNum = qs.get_int('page', 1)

    collection = get_collection('articles')
    row_cnt = collection.count_documents({})

    qs.unset('page')
    page = Page(10, 10)
    pageValue = page.paging("./?{}&page=".format(qs.make_string()), row_cnt, pageNum)

    rows = collection.find({}).sort([('date.first_ins', pymongo.DESCENDING)]).skip(pageValue.getStartRow()).limit(10)

    articles = []
    for row in rows:
        content = row['content']
        con_len = row['images'] and 600 or 300
        sumarry = None
        if len(content) > con_len:
            sumarry = content[:con_len] + '...'
        else:
            sumarry = content

        row['sumarry'] = sumarry
        del row['content']
        articles.append(row)

    data = {}
    data['articles'] = articles
    data['pages'] = pageValue.getPages()
    data['current_page'] = pageValue.getCurrentPage()
    data['prev_page'] = pageValue.getPrev()
    data['next_page'] = pageValue.getNext()
    data['input_data'] = qs

    return render_template("home.html", **data)




def make_query(keyword, repoter, start_dt, end_dt, op=False):

    q_or = {
        "multi_match": {
            "query": keyword,
            "fields": ["subject", "content"],
            "type": "best_fields",
            "tie_breaker": 0.8,
        }
    }

    q_and = {
        "multi_match": {
            "query": keyword,
            "fields": ["subject", "content"],
            "type": "best_fields",
            "tie_breaker": 0.8,
            "operator": "and"
        }
    }

    # q_and = {
    #     "match_phrase": {
    #         "content": keyword
    #     }
    # }

    # q_and = {
    #     "terms": {
    #         "content": [keyword]
    #     }
    # }

    q_repoter = {
        "match": {
            "repoter": repoter
        }
    }

    range_date = {}
    if start_dt:
        range_date['gte'] = start_dt.replace('-', '.') + " 00:00:00"
    if end_dt:
        range_date['lte'] = end_dt.replace('-', '.') + " 23:59:59"

    if range_date:
        q_date = {
            "range": {
                "date.first_ins": range_date
            }
        }

    conlist = []

    if op:
        conlist.append(q_and)
    else:
        conlist.append(q_or)

    if repoter:
        conlist.append(q_repoter)

    if range_date:
        conlist.append(q_date)

    query = {
        "query": {
            "bool": {
                "must": conlist
            }
        }
    }

    return query


def get_sort(sort):
    print("sort => ", sort)
    if sort == 'default':
        return None
    elif sort == 'date':
        return "date.first_ins:desc"
    elif sort == 'subject':
        return "subject:asc"
    elif sort == 'repoter':
        return "repoter:asc"
    else:
        return None


@flask_app.route("/search")
def search():
    query_string = str(request.query_string, encoding='utf-8')

    qs = QueryString(query_string)

    sk = qs.get_param('q')
    pageNum = qs.get_int('page', 1)

    # if qs.get_param('sort') is None:
    #     qs.set_param('sort', 'default')

    status = None
    res = []
    data = {}

    if sk:
        flask_app.logger.debug(sk)
        op_and = qs.get_param('operator') == 'on'
        query = make_query(qs.get_param('q'), qs.get_param('repoter'), qs.get_param('start_dt'), qs.get_param('end_dt'), op_and)
        flask_app.logger.debug(query)

        cnt_res = es.count(index="news", doc_type="article", body=query)

        qs.unset('page')
        page = Page(15, 5)
        pageValue = page.paging("./search?{}&page=".format(qs.make_string()), cnt_res['count'], pageNum)

        sort = get_sort(qs.get_param('sort', 'default'))
        if sort:
            flask_app.logger.debug(sort)
            search_result = es.search(index="news", doc_type="article", body=query, size=15, from_=pageValue.start_row, sort=sort)
        else:
            search_result = es.search(index="news", doc_type="article", body=query, size=15, from_=pageValue.start_row)

        flask_app.logger.debug(search_result)

        if search_result.get('hits'):
            tcnt = search_result.get('hits')['total']
            status = "검색건수 {}".format(tcnt)

            for row in search_result['hits']['hits']:
                article = row['_source']
                content = article['content']
                con_len = article['images'] and 600 or 300
                sumarry = None
                if len(content) > con_len:
                    sumarry = content[:con_len] + '...'
                else:
                    sumarry = content
                article['sumarry'] = sumarry
                del article['content']
                res.append(article)

        data['status'] = status
        data['search_results'] = res
        data['pages'] = pageValue.getPages()
        data['current_page'] = pageValue.getCurrentPage()
        data['prev_page'] = pageValue.getPrev()
        data['next_page'] = pageValue.getNext()
        data['input_data'] = qs

    else:
        status = "검색어 입력되지 않음."

        data = {
            'status': status,
            'search_results': res,
            'input_data': qs
        }

    return render_template("search_list.html", **data)


import os
import json


@flask_app.route("/similar")
def similar():
    path = os.path.dirname(os.path.abspath(__file__))
    print(path)


    query_string = str(request.query_string, encoding='utf-8')
    qs = QueryString(query_string)
    word = qs.get_param("word", "")

    model = word2vec.Word2Vec.load(path + '/data/news.model')
    data = model.wv.most_similar(positive=word.split(' '))

    json_data = json.dumps(data, ensure_ascii=False)
    res = make_response(json_data)
    res.headers['Content-Type'] = 'application/json'

    return res




if __name__ == "__main__":
    flask_app.run(host="localhost", port=8080, debug=True)
