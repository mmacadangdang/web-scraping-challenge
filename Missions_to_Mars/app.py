from flask import Flask, render_template
import scrape_mars
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# pymongo connection setup
conn = 'mongodb://localhost:27017/mission_to_mars'
client = pymongo.MongoClient(conn)

# Set route
@app.route("/")
def index():
    mars = client.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Set scrape route
@app.route("/scrape")
def scrape():
    mars = client.db.mars
    data = scrape_mars.scrape()
    mars.update({}, data)
    return "Scraping successful"

if __name__ == "__main__":
    app.run(debug=True)