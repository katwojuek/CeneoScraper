import os
import pandas as pd
from matplotlib import pyplot as plt

print(*[item.split(".").pop(0) for item in os.listdir("reviews")], sep="\n")
product_id = input("Podaj kod produktu: ")

reviews = pd.read_json(f"./reviews/{product_id}.json")

product_rating = reviews.stars.mean()
reviews_count = reviews.shape[0]
pros_count = reviews.pros.map(bool).sum()
cons_count = reviews.cons.map(bool).sum()
print(f"""Dla produktu o identyfikatorze {product_id} dostępnych jest {reviews_count} opinii.
Dla {pros_count} opinii autorzy podali listę zalet, a dla {cons_count} listę wad.
Średnia ocena produktu to {product_rating:.1f}.""")

recommendations = reviews.recommendation.value_counts(dropna = False)
recommendations.plot.pie()
plt.show()




