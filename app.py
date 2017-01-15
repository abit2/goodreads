from flask import Flask, jsonify, request, session
from goodreads import client
import datetime
import os
# from pymongo import MongoClient


app = Flask(__name__)


# MONGO_URL = os.environ.get('MONGOHQ_URL')
# mongo = MongoClient(MONGO_URL)

# db = mongo.heroku_f1tsdbtv
# data = db.data


@app.route('/api/search/book', methods=['GET'])
def get_search_books():
    if request.method == 'GET':
        q = request.args.get('query', type=str)
        gc = client.GoodreadsClient(
            "api key", "api secret")
        try:
            books = gc.search_books(q)
        except TimeoutError:
            print("Oops!  Seems the internet cannot be reached.  Try again... after sometime")

        l = []
        for book in books:
            author_list = book.authors
            each_book_details = {
                'title': book.title,
                'image_url': book.image_url,
                'author': author_list[0].name,
                'book_id': book.gid,
                'average_rating': book.average_rating
            }
            l.append(each_book_details)
            if len(l) == 10:
                break
        return jsonify({'books_list': l})


@app.route('/api/post/book', methods=['POST'])
def post_books():
    lat = request.args.get('lat', type=str)
    lng = request.args.get('lng', type=str)
    book_id = request.args.get('book_id', type=str)
    data = {
        "lat": lat,
        "lng": lng,
        "book_id": book_id
    }

    # if(data.insert_one(data)):
    #     return jsonify({'status': 'done'})
    # return jsonify({'status': 'failed'})
    # saving the particaular lat longitude with book_id in database


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
