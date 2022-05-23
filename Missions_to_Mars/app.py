from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_scraps"
mongo = PyMongo(app)

# create a listings collection, lazy loading
mars_collection = mongo.db.mars_data

@app.route("/")
def index():
    # find document from our mongo db and return it.
    mars_results = mars_collection.find_one()
    # pass that listing to render_template
    return render_template("index.html", mars_data=mars_results)

# set our path to /scrape
@app.route("/scrape")
def scraper():
    # call the scrape function in our scrape_mars file, scrape and save to mongo.
    mars_data_scrape = scrape_mars.scrape()
    # update our listings with the data that is being scraped or create&insert if collection doesn't exist
    mars_collection.update_one({}, {"$set": mars_data_scrape}, upsert=True)
    # return a message to our page so we know it was successful.
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)