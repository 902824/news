import logging

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


@ask.intent("TopicIntent")
def read_hlines():
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
    return question(headline_msg)


@ask.intent("AnswerIntent", convert={'number': int})
def read_article(number):
    '''
    winning_article = session.attributes['headlines'][number]
    access RSS feed and go to url of article
    store article in variable "text"
    article_msg = render_template('article', text=text)
    return statement(article_msg)
    '''


if __name__ == '__main__':
    app.run(debug=True)
    
