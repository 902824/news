import logging
import feedparser
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import random
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

@ask.intent("AMAZON.StopIntent")
def stop():
    return statement("okay")

@ask.intent("TopicIntent", convert={'topicResponse': str})
def read_hlines(topicResponse):
    word = ""
    session.attributes['state'] += 1
    if (session.attributes['state'] == 1):
       
        if(topicResponse.lower() == "basketball" or topicResponse.lower() == "football"):
            word = "Pro "+topicResponse
            session.attributes['nameTopic'] = camelcase(word)
        elif (topicResponse.lower() == "nfl"):
            session.attributes['nameTopic'] = camelcase("football")
        elif (topicResponse.lower() == "nba" or topicResponse.lower() == "n yeah"):
            session.attributes['nameTopic'] = camelcase("Pro Basketball")
        elif (topicResponse.lower() == "news"):
            ran = random.randint(0,14)
            articles = ["World", "Africa", "Americas", "Politics", "Sports", "Space", "Movies", "Travel", "Golf", "Baseball", "Soccer", "Science", "Education", "Technology"]
            session.attributes['nameTopic'] = camelcase(articles[ran])
        
        else:
            session.attributes['nameTopic'] = camelcase(topicResponse)
        
        try:
            feed = feedparser.parse('http://rss.nytimes.com/services/xml/rss/nyt/' + session.attributes['nameTopic'] + '.xml')
            news1 = feed.entries[1].title
            #print(session.attributes['state']+ "try")
        except:
            session.attributes['state'] == 0
            new = "Sorry, {} is not an option"
            
            #print(session.attributes['state'])
            
            msg = new.format(session.attributes['nameTopic'])
            return question(msg)
        feed = feedparser.parse('http://rss.nytimes.com/services/xml/rss/nyt/' + session.attributes['nameTopic'] + '.xml')
                
        news1 = feed.entries[1].title
        news2 = feed.entries[2].title
        news3 = feed.entries[3].title
        new = " here's the top headlines for {},,1,. {},. 2,,, {}, and, 3, {},. what number do you want to hear about?"
        msg = new.format(session.attributes['nameTopic'], news1, news2, news3)
        return question(msg)
    if (session.attributes['state'] == 2):
        msg = read_article(topicResponse)
        return statement(msg)
    if (session.attributes['state'] == 3):
        msg = "Thank you"
        return statement(msg)
        

            
def cutWord(sentence):
    fillers = ["um", "uh", "like", "hi", "hey", "hello", "oh"]
    pronouns = ["i", "we", "you", "he", "she", "it", "they", "his", "her", "their", "my", "our", "your", "me", "us", "him", "her", "them"]
    determiners = ["a", "and", "the", "this", "that", "these", "those", "an"]
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
    
def camelcase(s):
    s = s.title()
    words = s.split()
    words = cutWord(words)
    title = "".join(words)
    return title

def read_article(number):
    '''
    winning_article = session.attributes['headlines'][number]
    access RSS feed and go to url of article
    store article in variable "text"
    article_msg = render_template('article', text=text)
    return statement(article_msg)
    '''
    feed = feedparser.parse('http://rss.nytimes.com/services/xml/rss/nyt/' + session.attributes['nameTopic'] + '.xml')
    if(number.lower() == "one" or number == "1" or "first" in number.lower() or "1" in number.lower()):
        feeds = feed.entries[1].summary
    elif(number.lower() == "two" or number == "2" or "second" in number.lower() or "mid" in number.lower() or "middle" in number.lower() or "2" in number.lower()):
        feeds = feed.entries[2].summary
    elif(number.lower() == "three" or number == "3" or "last" in number.lower() or "last one" in number.lower()) or "3" in number.lower() or "final" in number.lower():
        feeds = feed.entries[3].summary
    else:
        feeds = "Sorry, that was not an option"
        
    msg = format(feeds)
    blank = msg.strip()
    if(len(blank) < 2):
        return "Sorry, there was no summary"
    return ","+msg

if __name__ == '__main__':
    app.run(debug=True)
    
