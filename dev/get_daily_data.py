import pickle
import pandas
from gnews import GNews
# import beautifulsoup
import csv

google_news = GNews(max_results=3, period='7d')
news_dict = dict()
cities = pandas.read_csv("worldcities.csv").set_index('city').T.to_dict('list')
city_number = 0
for city in cities:
    city_number += 1
    print(city_number, city)
    news_dict[city] = ""
    req = google_news.get_news(city)
    for i in range(len(req)):
        news_pop_up = '<a href=' + req[i]['url'] + ">" + str(i + 1) + '.' + \
                      req[i]['title'] + '</a>'
        news_dict[city] += news_pop_up + '\n'

f = open("daily_news.pkl", "wb")
pickle.dump(news_dict, f)
f.close()
