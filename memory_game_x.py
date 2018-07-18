#

import sys
import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_game():

    session.attributes['game'] = 0
    session.attributes['win']  = 0
    session.attributes['long'] = 2
#    session.attributes['numbers'] = [ 1, 2, 3]
    sys.stderr.write('\n\n-------------------------------'+'\n\n')
    welcome_msg = render_template('welcome',long=session.attributes['long'])
    return question(welcome_msg)


@ask.intent("NoIntent")
def all_done():
    return statement("Well, that was fun ... goodbye, now...")

@ask.intent("YesIntent")
def next_round():

    numbers = [randint(0, 9) for _ in range(3)]
    round_msg = render_template('round', numbers=numbers)
    session.attributes['numbers'] = numbers[::-1]  # reverse
    return question(round_msg)



def next_roundx():

    sys.stderr.write('\n\n-Y------------------------------'+'\n\n')
    sys.stderr.flush()
    numbers = [randint(0, 9) for _ in range(3)]
    sys.stderr.write('\n\n-Y------------------------------'+numbers+'\n\n')
    sys.stderr.flush()
    round_msg = render_template('round', numbers=numbers)
#    sys.stderr.write('\n\n-------------------------------'+round_msg+'\n\n')
    session.attributes['numbers'] = numbers[::-1]  # reverse
    return question(round_msg)

@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})
def answer(first, second, third):

    winning_numbers = session.attributes['numbers']
    if [first, second, third] == winning_numbers:
        msg = render_template('win')
    else:
        msg = render_template('lose')
    return statement(msg)


def answerx(first, second, third):

    winning_numbers = session.attributes['numbers']
    session.attributes['game'] += 1
    if [first, second, third] == winning_numbers:
        msga = render_template('win')
        session.attributes['win'] += 1
        if (session.attributes['win'] > 2) and ( session.attributes['win'] == session.attributes['game']):
             session.attributes['long'] += 1
             return question("Youre doing good. Lets make the game harder. Ready?") 
        
    else:
        msga = render_template('lose')

    msg = msga + render_template('score',
                                 win=session.attributes['win'],
                                 game=session.attributes['game']) + render_template('again')
    return question(msg)


if __name__ == '__main__':
    app.run(debug=True)

#
    
