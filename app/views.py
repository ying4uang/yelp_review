from app import app
from flask import g, Flask, jsonify, render_template, request, redirect, Response, url_for
from redis import StrictRedis
from lxml import html
from lxml import etree
import requests




def scrape_reviews(name, num_reviews):

   
    sum_rating = 0
    restaurant = ""
    

    if 'new york' in name.lower():

        restaurant = name.strip().replace(" ","-").replace("'","")

        print(restaurant)

    else:
        restaurant = name.strip().replace(" ","-").replace("'","") + "-new-york"

    print(restaurant)
    start_urls = 'http://www.yelp.com/biz/'+restaurant

    page = requests.get(start_urls)
    tree = html.fromstring(page.text)
    
    num_reviews = int(num_reviews)

    raw_reviews = tree.xpath("//div[contains(@class,'review-content')]//p[@lang='en']")

    if not raw_reviews:

        return None, None

    
    top_reviews = []
    for i in range(num_reviews):
        #print(raw_reviews[i].text_content())
        top_reviews.append(raw_reviews[i].text_content())



    raw_ratings = tree.xpath("//div[contains(@class,'biz-rating biz-rating-large clearfix')]//img//@alt")
 
    for j in range(num_reviews):

        sum_rating += float(raw_ratings[j][:3])

    avg_rating = float("{0:.2f}".format(sum_rating/num_reviews))



    return top_reviews, avg_rating



@app.route('/display_reviews')
def display_reviews():
    return render_template('display_reviews.html')

@app.route("/create", methods=['POST'])
def search_reviews():
    rname = request.form["cname"]
    num_reviews = request.form["ctarget"]
    
    reviews, rating = scrape_reviews(rname, num_reviews)

    if not reviews:
        return "restaurant not found!"
    else:
        return render_template('display_reviews.html', rname = rname, rev = reviews, rating = rating)



@app.route('/')
def index():
    return render_template('index.html')
 
 
