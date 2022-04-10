import json
import requests
from bs4 import BeautifulSoup

def extract_element(ancestor, selector, attribute=None):
    try:
        if attribute:
            return ancestor.select(selector).pop(0)[attribute].strip()
        else:
            return ancestor.select(selector).pop(0).text.strip()
    except IndexError: return None

product_id = input("Podaj identyfokator produktu: ")
url_pre = "https://www.ceneo.pl/"
url_post = "/opinie-"
page_no = 1
all_reviews = []

while(page_no):
    url = url_pre+product_id+url_post+str(page_no)
    response = requests.get(url, allow_redirects=False)
    if response.status_code == requests.codes.ok: 
        page_dom = BeautifulSoup(response.text, 'html.parser')
        reviews = page_dom.select("div.js_product-review")
        for review in reviews: 
            review_id = review["data-entry-id"]
            author = extract_element(review,"span.user-post__author-name")
            recommendation = extract_element(review, "span.user-post__author-recomendation > em")
            stars = extract_element(review, "span.user-post__score-count")
            content = extract_element(review, "div.user-post__text")
            publish_date = extract_element(review, "span.user-post__published > time:nth-child(1)", "datetime")
            purchase_date = extract_element(review, "span.user-post__published > time:nth-child(2)", "datetime")
            useful = extract_element(review, "span[id^=votes-yes]")
            useless = extract_element(review, "span[id^=votes-no]")
            
            pros = review.select("div.review-feature__title--positives ~ div.review-feature__item")
            pros = [item.text.strip() for item in pros]
            pros = ", ".join(pros)

            cons = review.select("div.review-feature__title--negatives ~ div.review-feature__item")
            cons = [item.text.strip() for item in cons]
            cons = ", ".join(cons)

            recommendation = True if recommendation == "Polecam" else False if recommendation == "Nie polecam" else None
            stars = float(stars.split("/").pop(0).replace(",", "."))
            content = content.replace("\n", " ").replace("  ", " ").strip()
            publish_date = publish_date.split(" ").pop(0)
            purchase_date = purchase_date.split(" ").pop(0)
            useful = int(useful)
            useless = int(useless)

            single_review = {
                "review_id": review_id,
                "author": author,
                "recommendation": recommendation,
                "stars": stars,
                "content": content,
                "publish_date": publish_date, 
                "purchase_date": purchase_date,
                "useful": useful,
                "useless": useless,
                "pros": pros,
                "cons": cons
            }
            all_reviews.append(single_review)
        page_no += 1
    else: page_no = None

f = open("reviews/"+product_id+".json", "w", encoding="UTF-8")
json.dump(all_reviews, f, indent=4, ensure_ascii=False)