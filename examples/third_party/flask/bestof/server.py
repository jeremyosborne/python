import os
import re
import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

# Basic settings.
BASE_DIR = os.path.realpath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Data scraping URL.
SCRAPE_URL = "http://www.craigslist.org/about/best/all"

# Some initialization.
def init():
    print "Downloading static content."
    if not os.path.exists(os.path.join(STATIC_DIR, "normalize.css")):
        print "\tnormalize.css downloading..."
        response = requests.get("http://necolas.github.io/normalize.css/2.1.2/normalize.css")
        with open(os.path.join(STATIC_DIR, "normalize.css"), "w") as f:
            f.write(response.text)
    else:
        print "\tnormalize.css already downloaded"

def scrape(filter=""):
    matched_items = []
    try:
        # Assuming the bestof page is still in the same shape as this was
        # written.
        parser = BeautifulSoup(requests.get(SCRAPE_URL).text)
        # All the items are paragraphs within the first blockquote.
        items = parser.find("section", class_="body").find_all("p")
        for item in items:
            # The best of item is located inside of the second 'a' tag.
            item = item.find_all("a")[1]
            item = {"href": item.get("href"), "text": item.text, }
            if filter:
                if re.findall(re.escape(filter), item["text"], re.I):
                    matched_items.append(item)
            else:
                matched_items.append(item)
    except BaseException as err:
        print "Oops, problem in the scraping...."
        print err
    
    return matched_items

app = Flask(__name__,
            # The template folder has a default.
            #template_folder="templates",
            # The static folder has a default.
            #static_folder="static",
            # What URL path can we send to to get a static URL rewrite? 
            static_url_path="/static/")

# When the url path is...
@app.route("/", methods=['GET', 'POST'])
# ... do this function.
def main():
    # Dynamic data.
    context = {}
    # Request is a globally available object, provided when this instance
    # of flask runs.
    if request.method == "POST":
        context["filter"] = request.form["filter"]
        context["bestof"] = scrape(request.form["filter"] or "")
    
    # Looks in the template folder, sends the template, if found, with
    # context. Uses Jinja2 by default.
    return render_template("index.html", **context)

if __name__ == "__main__":
    init()
    app.run(port=5000, debug=True)
