#
# SAMS Alexa course -- first Skill
# This skill allows you to play the memory game multiple times
# adapted from:
# https://developer.amazon.com/blogs/post/Tx14R0IYYGH3SKT/flask-ask-a-new-python-framework-for-rapid-alexa-skills-kit-development
# [20170711} (air) Initial version
#
# Student(s): <put your name(s) here>
#
# <comment on your features>
#

import sys
import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session


app = Flask(__name__)
ask = Ask(app, "/")
# logging.getLogger("flask_ask").setLevel(logging.DEBUG)


# state information
def trace_state(tag, state,dir):
    sys.stderr.write('--------------[{}]----> {} {}\n'.
                     format(tag,str(session.attributes['state']),dir))
    sys.stderr.flush()
# print things to the command window
def trace(string):
    sys.stderr.write(string+'\n')
    sys.stderr.flush()
    return

    
TRACE = True   # turn tracing on/off
# helper function: create a number sequence, embed in a challenge, return
def make_game():
    if not TRACE:
        return('')
    msg = 'I was here'
    trace_state(' make_game() ',str(session.attributes['state']),'f()')
    
    numbers = [randint(0, 9) for _ in range(session.attributes['long'])]
    msg = render_template('round', numbers=numbers)
    session.attributes['numbers'] = numbers[::-1]  # reverse
    session.attributes['game'] += 1  # game counter
    
    return(msg)


## root node
@ask.launch
def new_game():

    # the following is unnecessary for this skill, but this is a way
    # to have a skill say something only once
    if 'hello' in session.attributes:
        prefix = ''
    else:
        session.attributes['hello'] = 1
        prefix = 'Welcome to the SAMS memory game...'

    # the main bit of state that the skill needs to track from turn to turn
    # there's also 'numbers', which will show up later
    session.attributes['state'] = 1  # state we came from, state on exit from Intent
    session.attributes['game']  = 0  # how many games we've played so far
    session.attributes['win']   = 0  # how many the user won
    session.attributes['long']  = 3  # length of the digit string, start with 2
        
    # say hi, explain the game and ask user if they're ready
    task_msg = prefix+render_template('task',long=session.attributes['long'])
    # question() makes alexa listen for something from the user
    session.attributes['state'] = 1

    trace_state('start',session.attributes['state'],' ')
    return question(task_msg)


# NoIntent (a "no") can be a response to several originating states;
# use the (previous) state to select the right one
@ask.intent("NoIntent")
def all_done():

    trace_state('OLD state',session.attributes['state'],'from')

    # the user bails immediately; i.e. no games were played. Express regret
    if session.attributes['state'] == 1:  # origin state
        
        # starement() says something then exists immediately
        msg = "Ah well, that could have been fun ... Goodbye."
        session.attributes['state'] = 5  # set current state
        trace_state('NEW state',session.attributes['state'],'to')
    
    # the user played; give them some feedback on their performance
    elif session.attributes['state'] == 3:  # origin state
        
        msg = 'You played {}, and won, {}. Good job!'.format(
 		session.attributes['game'], session.attributes['win'])
        session.attributes['state'] = 4  # set current state
        trace_state('NEW state',session.attributes['state'],'to')
    else:
        
        msg = 'oh dear... came from {}. We should stop playing.'.format(session.attributes['state'])

        # starement() says something then exists immediately
    return statement(msg)


# NoIntent (a "yes") can be a response to several originating states;
# use the (previous) state to select the right one
@ask.intent("YesIntent")
def next_round():
    #dispatch per the originating state; for now state 2,3 'yes' works
    trace_state('OLD state',session.attributes['state'],'from')
    
    # when it's user turn to play, create a game instance
    if (session.attributes['state'] == 1) or (session.attributes['state'] == 3):
        msg = make_game()
   # oh-oh, not from a legal origin.
    else:
        msg ='you came from state, {}. Something went wrong.'.format(session.attributes['state'])
        return statement(msg)

        
    session.attributes['state'] = 2  # current (this) state
    trace_state('NEW state',session.attributes['state'],'to')
    return question(msg)


@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})
def answer(first, second, third):

    trace_state('OLD state',session.attributes['state'],'from')
    trace('*ASR: [{}] [{}] [{}]'.format(first, second, third))

    # create the correct answer sequence
    winning_numbers = session.attributes['numbers']
    # was the sequence 2 long?
    if session.attributes['long'] == 2:
        # score it and feedback
        if [first, second] == winning_numbers:
            msg = render_template('win')
            session.attributes['win'] += 1  # win counter
        else:
            msg = render_template('lose')
    # was the sequence 3 long?
    elif session.attributes['long'] == 3:
        # score it and feedback
        if [first, second, third] == winning_numbers:
            msg = render_template('win')
            session.attributes['win'] += 1  # win counter
        else:
            msg = render_template('lose')
    # code here for anything longer...

    session.attributes['state'] = 3  # set current state
    trace_state('NEW state',session.attributes['state'],'to')
    return question(msg+'... Do you want to keep playing?')


##########################
if __name__ == '__main__':
    app.run(debug=True)

#
    
