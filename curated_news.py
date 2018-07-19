import logging
import feedparser
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

# import feedparser

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_feed():
    welcome_msg = render_template('task')
    return question(welcome_msg)


@ask.intent("TopicIntent", convert={'topicResponse': str})
def read_hlines():
    feed = feedparser.parse('http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml')

    news1 = feed.entries[1].title
    news2 = feed.entries[2].title
    '''
    call feedparser
    access RSS feeds of news source
    if extra words: slice
    search keywords
    if keywords:
        headlines = []
        session.attributes['headlines'] = headlines
        headline_msg = render_template('five', headlines=headlines)
    else:
        headline_msg = render_template('none')
    '''
    new=" here is the top headlines, 1, {}, 2, {}, what number do you want to hear about?"
    
    msg = new.format( news1, news2)
    return question(msg)


@ask.intent("AnswerIntent", convert={'number': int})
def read_article(number):
    '''
    winning_article = session.attributes['headlines'][number]
    access RSS feed and go to url of article
    store article in variable "text"
    article_msg = render_template('article', text=text)
    return statement(article_msg)
    '''
    feed = feedparser.parse('http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml')
    if(number == 1):
        feeds = feed.entries[1].published
    else:
        feeds = feed.entries[2].published
    msg = format(feeds)
    return question(msg)

if __name__ == '__main__':
    app.run(debug=True)
    
