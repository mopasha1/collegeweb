from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_tinymce import TinyMCE

app = Flask(__name__,static_url_path='/static')
tinymce = TinyMCE()
tinymce.init_app(app)
# MongoDB configuration
client = MongoClient('localhost', 27017)
db = client['rating_and_reviews']
collection = db['reviews']
questions = db['questions']
# Routes
@app.route('/')
def index():
    reviews = collection.find({})
    return redirect('search')

# @app.route('/add_review/<professorid>', methods=['POST'])
# def add_review(professorid):
    

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_results = []
    if request.method == 'POST':
        search_term = request.form['search-input']
        search_results = collection.find({'$or': [{'name': {'$regex': search_term, '$options': 'i'}}, {'subjects': {'$regex': search_term, '$options': 'i'}}]})
        return render_template('search.html', professors=search_results)
    if request.method == 'GET':
        return render_template('search.html')
    
    
@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    return render_template('search_results.html')

@app.route('/view/<professorid>', methods=['GET', 'POST'])
def view(professorid):
    if request.method == 'GET':
        professor = collection.find_one({'_id': ObjectId(professorid)})
        return render_template('view.html', professor=professor)
    if request.method == 'POST':
        review = {
            'name': request.form['name'],
            'rating': request.form['rate'],
            'class': request.form['class'],
            'comment': request.form['comment']
        }
        filter_query = {'_id': ObjectId(professorid)}  
        update_query = update_query = {
        '$push': {'reviews': review},
        '$inc': {'num_ratings': 1},  # Increment the number of ratings by 1
        '$set': {
            'average_rating': {
                '$avg': ['$avg_rating', review['rating']]  # Calculate the new average rating
            }
    }
}

        # Perform the update operation
        collection.update_one(filter_query, update_query)
    return redirect(url_for('view', professorid=professorid))

@app.route('/discussions', methods=['GET', 'POST'])
def discussions():
    if request.method == 'GET':
        ques = questions.find({})

        return render_template('discussions.html', questions=ques)
    if request.method == 'POST':
        question = {
            'author': request.form['author'],
            'subject': request.form['topic'],
            'text': request.form['text'],
            'responses':[]
        }
        questions.insert_one(question)
        return redirect(url_for('discussions'))
    
@app.route('/discuss/<questionid>', methods=['GET', 'POST'])
def discuss(questionid):
    if request.method == 'GET':
        q = questions.find_one({'_id': ObjectId(questionid)})

        return render_template('discuss.html', question=q)
    if request.method == 'POST':
        comment = {
            'author': request.form['author'],
            'content': request.form['content']
        }
        filter_query = {'_id': ObjectId(questionid)}  
        update_query = {
        '$push': {'responses': comment}}
        questions.update_one(filter_query, update_query)
        return redirect(url_for('discuss', questionid=questionid, question=questions.find_one({'_id': ObjectId(questionid)})
))
    
        

if __name__ == '__main__':
    app.run(debug=True)
