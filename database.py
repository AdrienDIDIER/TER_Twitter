from myapp import app

app.config['MONGO_DBNAME'] = 'tweetostats_db'
app.config['MONGO_URI'] = 'mongodb://tweetostats:tweetostats34@ds125288.mlab.com:25288/tweetostats_db'
app.config['SECRET_KEY'] = 'super secret key'