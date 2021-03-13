import flask
from db import get_books, add_book, add_author, get_books_of_author

app = flask.Flask(__name__)

# sample data for my own reference
books = [
    {'id': 0, # changed to UUID for security reasons
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

@app.route('/', methods=["GET"])
def home():
    return "<h1>Testing Flask App with Database</h1><p>StudyBuddies is going to be a lit company</p>"

@app.route("/api/v1/resources/books/add", methods=['POST'])
def api_add():
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400  
    
    return add_book(flask.request.get_json())
    
@app.route("/api/v1/people/authors/add", methods=['POST'])
def api_add_author():
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400  
    
    return add_author(flask.request.get_json())

@app.route("/api/v1/resources/books/all", methods=['GET'])
def api_all():
    return get_books() 

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in flask.request.args:
        id = int(flask.request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return flask.jsonify(results)


@app.route('/api/v1/resources/author_books', methods=['GET'])
def api_books_from_author():
    return get_books_of_author(flask.request.get_json()) 



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
