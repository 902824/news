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
        elif (topicResponse.lower() == "tv"):
            session.attributes['nameTopic'] = camelcase("Television")
        elif (topicResponse.lower() == "nba" or topicResponse.lower() == "n yeah"):
            session.attributes['nameTopic'] = camelcase("Pro Basketball")
        elif (topicResponse.lower() == "news" or "any" in topicResponse.lower()):
            session.attributes['nameTopic'] = "HomePage"
        else:
            session.attributes['nameTopic'] = camelcase(topicResponse)
        
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
        msg = ", would you like to hear about another topic?"
        if topicResponse.lower() == "yes":
            session.attributes['state'] = 0
            return question("okay, what would you like to hear about?")
        else:
            msg = "Thank you, goodbye"
            return statement(msg)
        

            
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
    if(len(blank) < 13):
        return "Sorry, there was no summary, would you like to hear about another topic?"
    return ","+msg + ", would you like to hear about another topic?"

if __name__ == '__main__':
    app.run(debug=True)
    
