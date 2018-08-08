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
    
def rng(num1, num2):#random number generator just because i wanted it
    return random.randint(num1,num2)

def readArticles(article):
        feed = feedparser.parse('http://rss.nytimes.com/services/xml/rss/nyt/' + session.attributes['nameTopic'] + '.xml')
                
        news1 = feed.entries[1].title
        news2 = feed.entries[2].title
        news3 = feed.entries[3].title
        new = " here's the top headlines for {},,1,. {},. 2,,, {}, and, 3, {},. what number do you want to hear about?"
        msg = new.format(session.attributes['nameTopic'], news1, news2, news3)
        return question(msg)

@ask.intent("TopicIntent", convert={'topicResponse': str})
def read_hlines(topicResponse):
    articalsForListen = ["World", "Africa", "Americas", "Asia Pacific", "Europe", "Middle East", "US", "Education", "Politics", "Business",
    "Small Business", "Economy", "Technology", "Sports", "Baseball", "Golf", "Hockey", 
    "Soccer", "Tennis", "Science", "Environment", "Space", "Health", "Arts", "Books", "Dance", "Movies",
    "Music", "Television", "Theater", "Travel", "College Basketball", "College Football"]
    word = ""
    session.attributes['state'] += 1
    if (session.attributes['state'] == 1):
       
        if(topicResponse.lower() == "basketball" or topicResponse.lower() == "football"):
            word = "Pro "+topicResponse
            session.attributes['nameTopic'] = camelcase(word)
        elif (topicResponse.lower() == "nfl"):
            session.attributes['nameTopic'] = camelcase("Pro football")
        elif (topicResponse.lower() == "tv"):
            session.attributes['nameTopic'] = camelcase("Television")
        elif (topicResponse.lower() == "nba" or topicResponse.lower() == "n yeah"):
            session.attributes['nameTopic'] = camelcase("Pro Basketball")
        elif (topicResponse.lower() == "news" or "any" in topicResponse.lower()):
            session.attributes['nameTopic'] = "HomePage"
        else:
            d = 0
            for i in range(len(articalsForListen)):
                if articalsForListen[d].lower() in topicResponse.lower():
                    session.attributes['nameTopic'] = camelcase(articalsForListen[i])
                    feed = feedparser.parse('http://rss.nytimes.com/services/xml/rss/nyt/' + camelcase(articalsForListen[i]) + '.xml')
                    pass
                d += 1
        
        try:
            feed = feedparser.parse('http://rss.nytimes.com/services/xml/rss/nyt/' + session.attributes['nameTopic'] + '.xml')
            news1 = feed.entries[1].title
            
        except:
            articals = ["World", "Africa", "Americas", "Asia Pacific", "Europe", "Middle East", "US", "Education", "Politics", "Business",
            "Small Business", "Economy", "Technology", "Sports", "Baseball", "Basketball", "Football", "Golf", "Hockey", "College Basketball",
            "College Football", "Soccer", "Tennis", "Science", "Environment", "Space", "Health", "Arts", "Books", "Dance", "Movies",
            "Music", "Television", "Theater", "Travel"]
            num1 = rng(0, 34)
            num2 = rng(0, 34)
            while num2 == num1:
                num2 = rng(0, 34)
            session.attributes['state'] = 0
            news1 = articals[num1]
            news2 = articals[num2]
            session.attributes['nameTopic'] = topicResponse
            new = "Sorry, {} is not an option, but you can try something like, {}, or, {}"
            msg = new.format(session.attributes['nameTopic'], news1, news2)
            return question(msg)
        
        feed = feedparser.parse('http://rss.nytimes.com/services/xml/rss/nyt/' + session.attributes['nameTopic'] + '.xml')
                
        news1 = feed.entries[1].title
        news2 = feed.entries[2].title
        news3 = feed.entries[3].title
        new = " here's the top headlines for {},,1,. {},. 2,,, {}, and, 3, {},. what number do you want to hear about?"
        msg = new.format(session.attributes['nameTopic'], news1, news2, news3)
        return question(msg)
    
    elif (session.attributes['state'] == 2):
        msg = read_article(topicResponse)
        return question(msg)
    elif (session.attributes['state'] == 3):
        
        
        if "yes" in topicResponse.lower() or "sure" in topicResponse.lower() or "why not" in topicResponse.lower() or "ok" in topicResponse.lower() or "ye" in topicResponse.lower():
            session.attributes['state'] = 0
            return question("Ok, what would you like to hear about?")
        else:
            msg = "Okay, Thank you"
            return statement(msg)
    elif (session.attributes['state'] == 4):
        session.attributes['state'] = 2
        read_article(topicResponse.lower())
        
            
def cutWord(sentence):
    fillers = ["um", "uh", "like", "hi", "hey", "hello", "oh", "ok", "okay"]
    pronouns = ["i", "we", "you", "he", "she", "it", "they", "his", "her", "their", "my", "our", "your", "me", "us", "him", "her", "them"]
    determiners = ["a", "and", "the", "this", "that", "these", "those", "an"]
    verbs = ["to be", "am", "are", "is"]
    for word in list(sentence): 
        if word.lower() in fillers:
            sentence.remove(word)
    for word in list(sentence): 
        if word.lower() in pronouns:
            sentence.remove(word)
    for word in list(sentence): 
        if word.lower() in determiners:
            sentence.remove(word)
    for word in list(sentence): 
        if word.lower() in verbs:
            sentence.remove(word)
    return sentence
    
def camelcase(s):
    s = s.title()
    words = s.split()
    words = cutWord(words)
    title = "".join(words)
    return title

def read_article(number):

    oldTopic = session.attributes['nameTopic']
    
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
    if(len(blank) < 13):
        return "Sorry, there was no summary, Do you want to hear about another topic?"
    return ","+msg + ", Do you want to hear about another topic?"

if __name__ == '__main__':
    app.run(debug=True)
    

