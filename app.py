from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Set up app routes/ this is the root route?
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

#Defines the route flask will be using
@app.route("/scrape")
#Start a function that the route will use

    #access the database, scrape the new data, update the database return a message when succesful.
def scrape():  
    #assign a new variable
   mars = mongo.db.mars
   #create a new variable to holf the newly scraped data
   mars_data = scraping.scrape_all()
   #update the database
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)
if __name__ == "__main__":
   app.run()
