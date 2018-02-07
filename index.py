from auth import *
from retrieve_tweets.dated_tweets.filters import filter
from retrieve_tweets.tweets_collection import delete_many_tweets

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filtered-results')
def filtered():
    filter("Nutella")
    return render_template('index.html')

@app.route('/delete-all-tweets')
def deleted():
    delete_many_tweets()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
