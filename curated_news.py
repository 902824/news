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
    session.attributes['state'] = 0
    session.attributes['nameTopic'] = ""
    welcome_msg = render_template('task')
    return question(welcome_msg)


@ask.intent("TopicIntent", convert={'topicResponse': str})
def read_hlines(topicResponse):
    session.attributes['state'] += 1
    if (session.attributes['state'] == 1):
        
        feed = feedparser.parse('http://rss.nytimes.com/services/xml/rss/nyt/' + topicResponse + '.xml')
        session.attributes['nameTopic'] = topicResponse
        news1 = feed.entries[1].title
        news2 = feed.entries[2].title
        new = " here is the top headlines,,1,. {},. 2,,, {},. what do you want to hear about?"
        msg = new.format(news1, news2)
        return question(msg)
    if (session.attributes['state'] == 2):
        msg = read_article(topicResponse)
        return question(msg)
    if (session.attributes['state'] == 3):
        msg = "Thank you"
        return statement(msg)
def cutWord(sentence):
    fillers = ["um", "uh", "like", "hi", "hey", "hello", "oh"]
    pronouns = ["i", "we", "you", "he", "she", "it", "they", "his", "her", "their", "my", "our", "your", "me", "us", "him", "her", "them"]
    determiners = ["a", "and", "the", "this", "that", "these", "those"]
    verbs = ["to be", "am", "are", "is"]
    for word in list(sentence): 
        if word in fillers:
            sentence.remove(word)
    for word in list(sentence): 
        if word in pronouns:
            sentence.remove(word)
    for word in list(sentence): 
        if word in determiners:
            sentence.remove(word)
    for word in list(sentence): 
        if word in verbs:
            sentence.remove(word)
    return sentence


def read_article(number):
    '''
    winning_article = session.attributes['headlines'][number]
    access RSS feed and go to url of article
    store article in variable "text"
    article_msg = render_template('article', text=text)
    return statement(article_msg)
    '''
    feed = feedparser.parse('http://rss.nytimes.com/services/xml/rss/nyt/' + session.attributes['nameTopic'] + '.xml')
    if(number == "one" or number == "1"):
        feeds = feed.entries[1].summary
    else:
        feeds = feed.entries[2].summary
    msg = format(feeds)
    return ","+msg

if __name__ == '__main__':
    app.run(debug=True)
    
