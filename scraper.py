import json
import requests
from bs4 import BeautifulSoup

def extract_element(ancestor, selector, attribute=None, extract_list=False):
    try:
        if extract_list:
            return ", ".join([item.text.strip() for item in ancestor.select(selector)])
        if attribute:
            return ancestor.select(selector).pop(0)[attribute].strip()
        return ancestor.select(selector).pop(0).text.strip()
    except IndexError: return None

selectors = {
    "author": ["span.user-post__author-name"],
    "recommendation": ["span.user-post__author-recomendation > em"],
    "stars": ["span.user-post__score-count"],
    "content": ["div.user-post__text"],
    "publish_date": ["span.user-post__published > time:nth-child(1)", "datetime"], 
    "purchase_date": ["span.user-post__published > time:nth-child(2)", "datetime"],
    "useful": ["span[id^=votes-yes]"],
    "useless": ["span[id^=votes-no]"],
    "pros": ["div.review-feature__title--positives ~ div.review-feature__item", None, True],
    "cons": ["div.review-feature__title--negatives ~ div.review-feature__item", None, True]
}

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
            single_review = {
                key: extract_element(review, *value)
                    for key, value in selectors.items()
            }

            single_review["review_id"] = review["data-entry-id"]
            single_review["recommendation"] = True if single_review["recommendation"] == "Polecam" else False if single_review["recommendation"] == "Nie polecam" else None
            single_review["stars"] = float(single_review["stars"].split("/").pop(0).replace(",", "."))
            single_review["content"] = single_review["content"].replace("\n", " ").replace("  ", " ").strip()
            single_review["publish_date"] = single_review["publish_date"].split(" ").pop(0)
            try:
                single_review["purchase_date"] = single_review["purchase_date"].split(" ").pop(0)
            except AttributeError:
                single_review["purchase_date"] = None
            single_review["useful"] = int(single_review["useful"])
            single_review["useless"] = int(single_review["useless"])

            all_reviews.append(single_review)
        page_no += 1
    else: page_no = None

f = open("reviews/"+product_id+".json", "w", encoding="UTF-8")
json.dump(all_reviews, f, indent=4, ensure_ascii=False)