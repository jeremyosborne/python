import requests
import xmltodict
from flask import Flask, jsonify

# Data scraping URL.
XML_URL = "http://www.w3schools.com/xml/cd_catalog.xml"

app = Flask(__name__)

@app.route("/")
def main():
    xml = requests.get(XML_URL).text
    converted = xmltodict.parse(xml)
    return jsonify(converted)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
