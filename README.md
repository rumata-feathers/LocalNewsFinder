# Local News Finder 
Python Project for MIPT (Technology of Programming)

## The project is hosted on your local server, connects to main news agregators like google news, bbc and etc. and creates a list of news 

Before checking out my project, run these commands in comman line:
- pip install -r requirements.txt	

Then every morning run (one time a day/week etc) 
-python3 get_daily_news.py
This will load daily_news for every city and save it to daily_news.pkl
then run
-python3 main.py and either open html file(map.html) or click on server's ip(usually smth like 127.0.0.1:5000
choose map theme and serf the news!
