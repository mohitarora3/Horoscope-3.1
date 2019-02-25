from __future__ import print_function

import random
# ------------------------------------------------------------------------------
# ---------------------------- Main Handler ------------------------------------
# ------------------------------------------------------------------------------

def lambda_handler(event, context):
    """ 
    This is the Main Handler function that will call other functions.
    We get two inputs : event , context
    """
    
    if event['request']['type'] == "LaunchRequest":
        return onLaunch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return onIntent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return onSessionEnd(event['request'], event['session'])
        
# ------------------------------------------------------------------------------
# ----------------------------- Event Handlers ---------------------------------
# ------------------------------------------------------------------------------

def onLaunch(launchRequest, session):
    """
    This function welcomes the user , if the person does not Know how to 
    interact with the Skill 
    """
    
    return welcomeGuest()
    

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def onIntent(intentRequest, session):
             
    intent = intentRequest['intent']
    intentName = intentRequest['intent']['name']

    if intentName == "WhatIsMyZodiac":
        return set_zodiac(intent, session)
    elif intentName =="ZodiacInformation":
        return zodiac_information(intent,session)
    elif intentName == "AMAZON.HelpIntent":
        return welcomeGuest()
    elif intentName == "AMAZON.CancelIntent" or intentName == "AMAZON.StopIntent":
        return handleSessionEndRequest()
    else:
        raise ValueError("Invalid intent")
        

def onSessionEnd(sessionEndedRequest, session):
    """ 
    Called when the user ends the session.
    """
    print("on_session_ended requestId=" + sessionEndedRequest['requestId'] + ", sessionId=" + session['sessionId'])
        
    
# ------------------------------------------------------------------------------
# --------------------------- Behaviour Handlers -------------------------------
# ------------------------------------------------------------------------------

def welcomeGuest():
    """
    Giving Welcome Instructions to User
    """
    
    sessionAttributes = {}
    cardTitle = "Welcome Information"
    speechOutput =  "Welcome to Horoscope 3.1, " \
                    "tell me your date of birth, " \
                    "for example: three december. "
    repromptText =  "tell me your date of birth, " \
                    "for example: three december. "
    shouldEndSession = False
    
    return buildResponse(sessionAttributes, buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession))


def create_zodiac_attributes(Zodiac):
    return {"zodiac": Zodiac}



def set_zodiac(intent, session):
    """ Sets the zodiac of the person and prepares the speech to reply the same to the
    user.
    """

    
    card_title = "Zodiac Sign"
    session_attributes = {}
    should_end_session = False

    Zodiac=""
            
    if 'month' in intent['slots']: 
        if 'date' in intent['slots'] and intent['slots']['date']['value'].isnumeric():
            birth_month=intent['slots']['month']['value'].lower()
            birth_day=int(intent['slots']['date']['value'])
    
            if (birth_day>=20 and birth_month=="january" and birth_day<=31) or (birth_day>=1 and birth_day<=18 and  birth_month=="february"):        
                Zodiac="Aquarius"
            
            elif (birth_day>=19 and birth_month=="february"and birth_day<=29) or (birth_day>=1 and  birth_day<=20 and  birth_month=="march"):
                Zodiac="Pisces"
            
            elif (birth_day>=21 and birth_month=="march" and birth_day<=31) or (birth_day>=1 and birth_day<=19 and birth_month=="april"):
                Zodiac="Aries"
            
            elif (birth_day>=20 and birth_month=="april" and birth_day<=30) or (birth_day>=1 and birth_day<=20 and birth_month=="may"):
                Zodiac="Taurus"
            
            elif (birth_day>=21 and birth_month=="may" and birth_day<=31) or (birth_day>=1 and  birth_day<=20 and birth_month=="june"):
                Zodiac="Gemini"
            
            elif (birth_day>=21 and birth_month=="june" and birth_day<=30) or (birth_day>=1 and birth_day<=22  and birth_month=="july"):
                Zodiac="Cancer"
            
            elif (birth_day>=23 and  birth_month=="july" and birth_day<=31) or (birth_day>=1 and birth_day<=22 and birth_month=="august"):
                Zodiac="Leo"
            
            elif (birth_day>=23 and birth_month=="august" and birth_day<=31) or (birth_day>=1 and birth_day<=22 and birth_month=="september"):
                Zodiac="Virgo"
            
            elif (birth_day>=23 and birth_month=="september" and birth_day<=30) or (birth_day>=1 and birth_day<=22 and birth_month=="october"):
                Zodiac="Libra"
        
            elif (birth_day>=23 and birth_month=="october" and birth_day<=31) or (birth_day>=1 and birth_day<=21 and birth_month=="november"):
                Zodiac="Scorpio"
            
            elif (birth_day>=22 and birth_month=="november" and birth_day<=30) or (birth_day>=1 and birth_day<=21 and birth_month=="december"):
                Zodiac="Sagittarius"
            
            elif (birth_day>=22 and birth_month=="december" and birth_day<=31) or (birth_day>=1 and birth_day<=19 and birth_month=="january"):
                Zodiac="Capricorn"
    
    if(len(Zodiac)>1):
                session_attributes = create_zodiac_attributes(Zodiac)
                speech_output = "Your zodiac sign is " + \
                        Zodiac+ \
                        ". You can ask me information about yourself by saying, " \
                        "describe me"
                reprompt_text = "You can ask me information about yourself by saying, " \
                            "describe me"
    else:
        speech_output = "Sorry, i can't tell your zodiac sign because you provided invalid details. " \
                        "Please try again.  "\
                        "Tell me your date of birth, " \
                        "for example: three december. "
        reprompt_text = "Tell me your date of birth, " \
                        "for example: three december. "
    return buildResponse(session_attributes, buildSpeechletResponse(
        card_title, speech_output, reprompt_text, should_end_session))

def zodiac_information(intent, session):
    """ 
    Provides some funny and ineteresting facts about person.
    """
    cardTitle = "Interesting Information"
    sessionAttributes = {}
    if session.get('attributes', {}) and "zodiac" in session.get('attributes', {}):
        Zodiac = session['attributes']['zodiac']
        zodiac_info=Information[Zodiac]
        speechOutput = zodiac_info+" That's all. Thank you for trying Horoscope 3.1, please take a moment to rate and review the skill, have a nice day!!"
        repromptText=None
        shouldEndSession = True

    else:
        speechOutput ="I can't describe you until you tell me your date of birth. " \
                        "First, "\
                        "tell me your date of birth, " \
                        "for example: three december. "

        repromptText = "Tell me your date of birth " \
                        "for example: three december. "
        shouldEndSession = False
    return buildResponse(sessionAttributes, buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession))


def handleSessionEndRequest():
    cardTitle = "Session Ended"
    speechOutput = "Thank you for trying horoscope 3.1 " \
                    "Have a nice day! "
    shouldEndSession = True
    return buildResponse({}, buildSpeechletResponse(cardTitle, speechOutput, None, shouldEndSession))    

# ------------------------------------------------------------------------------
# --------------------------- Response Builders --------------------------------
# ------------------------------------------------------------------------------

def buildSpeechletResponse(title, output, repromptTxt, endSession):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
            },
            
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
            },
            
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': repromptTxt
                }
            },
        'shouldEndSession': endSession
    }


def buildResponse(sessionAttr , speechlet):
    return {
        'version': '1.0',
        'sessionAttributes': sessionAttr,
        'response': speechlet
    }

# ------------------------------------------------------------------------------
# ---------------------------- Zodiac Information ---------------------------------
# ------------------------------------------------------------------------------

Information={"Aquarius" : "your lucky Colors are: light-blue and silver. \
your lucky day is: saturday. \
your lucky numbers are: 4, 7, 11, 22, and 29. \
your best match for marriage and partnership is: leo. \
your strengths are: inventive, humanistic, friendly, altruistic, sociable and reformative. \
your weaknesses are: emotionally detached, scatterbrained, irresponsible, inability to compromise and hot tempered. \
you like: fun with friends, helping others, fighting and intellectual conversation . \
you dislike: being lonely, dull or boring situations, restrictions and incomplete promises. \
you are shy and quiet, but on the other hand you are eccentric and energetic. you are deep thinker and highly intellectual. ",\


"Pisces": "your lucky colors are: mauve, lilac, purple, violet and sea green. \
your lucky day is: thursday. \
your lucky numbers are: 3, 9, 12, 15, 18 and 24. \
your best match for marriage and partnership is: virgo. \
your strengths are: compassionate, artistic, intuitive, gentle, wise, adaptable and imaginative. \
your weaknesses are: oversensitive, indecisive, lazy, escapist and fearful. \
you like: creativity, being alone, sleeping, music, romance and swimming. \
you dislike: rules and restrictions, hardwork, criticism, and being under pressure. \
you are very friendly, you enjoy company of different people. you are selfless, you are always willing to help others, without hoping to get anything back. ",\

"Aries":"your lucky color is: red. \
your lucky day is: tuesday. \
your lucky numbers are: 1, 8 and 17. \
your best match for marriage and partnership is: libra. \
your strengths are: courageous, determined, confident, enthusiastic, optimistic, honest and passionate. \
your weaknesses are: impatient, moody, short-tempered, impulsive and aggressive. \
you like: loud music, parties, friends, fights, sporting events, being outdoors and action movies. \
you dislike: waiting, being disappointed and being ignored. \
you are natural born leader that knows how to take charge, you are straight-forward and you have zero time for bullshit, you are ultra competitive and wont give up without one hell of a fight. you hate dull and repetitive routines. " ,\

            
"Taurus":"your lucky colors are: green and pink. \
your lucky days are: friday and monday. \
your lucky numbers are: 2, 6, 9, 12 and 24. \
your best match for marriage and partnership is: scorpio. \
your strengths are: steady, driven, tenacious, patient, enduring, dedicated, determined and trustworthy. \
your weaknesses are: materialistic, resistant to change, fanatical, indulgent, gluttonous, possessive, stubborn and narrow-minded. \
you like: gardening, cooking, music, romance, high quality clothes, beauty and harmony. \
you dislike: being rushed into making a decision, uncomfortable surroundings, being pestered or annoyed. \
you are practical and well-grounded, you feel the need to always be surrounded by love and beauty, turned to the material world, hedonism, and physical pleasures. you are ready to endure and stick to your choices until you reach the point of personal satisfaction. ",\
                
"Gemini":"your lucky colors are: light-green and yellow. \
your lucky day is: wednesday. \
your lucky numbers are: 5, 7, 14 and 23. \
your best match for marriage and partnership is: sagittarius. \
your strengths are: intelligent, adaptable, agile, communicative, and informative. \
your weaknesses are: talkative, exaggerating, deceptive, cunning, superficial and inconsistent. \
you like: music, books, magazines, solving problems, playing games and short trips around the town. \
you dislike: obsessive amounts of seriousness, boredom ,immaturity, repetition, broken promises and dullness  .\
you try to avoid conflict and will walk away before things get too heated, you are fiercely loyal friend, ally and lover. your mind always racing with thoughts and ideas. " ,\

"Cancer":"your lucky Color is: white. \
your lucky days are: monday and thursday. \
your best match for marriage and partnership is: capricorn. \
your lucky numbers are: 2, 3, 15 and 20. \
your strengths are: tenacious, highly imaginative, loyal, emotional, sympathetic and persuasive. \
your weaknesses are: moody, pessimistic, suspicious, manipulative and insecure. \
you like: money, art, home, helping loved ones and a good meal with friends. \
you dislike: strangers, cruelty, being alone and negative thinking. \
you are deeply intuitive and sentimental. you are very emotional and sensitive, and care deeply about matters of the family and your home. you are sympathetic and attached to people you keep close. you are very loyal and able to empathize with other people's pain and suffering. ",\

"Leo":"your lucky colors are: gold, yellow and orange. \
your lucky day is: sunday. \
your lucky numbers are: 1, 3, 10 and 19. \
your best match for marriage and partnership is: aquarius. \
your strengths are: creative, passionate, generous, warm-hearted, cheerful and humorous. \
your weaknesses are: arrogant, stubborn, self-centered, lazy and inflexible. \
you like: theater, taking holidays, being admired, expensive things, bright colors and fun with friends. \
you dislike: being ignored, facing difficult reality and not being treated like a king or queen. \
you are natural born leaders. you are dramatic, creative, self-confident, dominant and extremely difficult to resist, able to achieve anything you want to in any area of life you commit to. ",\

"Virgo":"your lucky colors are: grey, beige and pale-yellow. \
your lucky Day is: wednesday. \
your best match for marriage and partnership is: pisces. \
your lucky numbers are: 5, 14, 15, 23 and 32. \
your strengths are: truthful, loyal, straightforward, analytical, kind, hardworking and practical. \
your weaknesses are: shyness, worry, obsessive and timidity. \
you like: animals, healthy food, books, nature and cleanliness. \
you dislike: rudeness, asking for help and acting as a leader. \
you always pay attention to the smallest details and your deep sense of humanity makes you one of the most careful person. your methodical approach to life ensures that nothing is left to chance, and although you are often tender, your heart might be closed for the outer world. ",\

"Libra":"your lucky colors are: pink and green. \
your lucky day is: friday. \
your best match for marriage and partnership is: aries. \
your lucky Numbers are: 4, 6, 13, 15 and 24. \
your strengths are: cooperative, diplomatic, gracious, fair-minded and social. \
your weaknesses are: indecisive, unreliable, manipulative and stubborn. \
you like: harmony, gentleness, balance, kindness, parting with others and outdoor activities. \
you dislike: violence, injustice and crowd. \
you  are smart enough to learn from your mistakes and you tend to remember everything so that you don’t make the same error of judgement twice. you are also willing to be patient and wait for the right person to come along and wont just settle for the first person that shows interest. ",\

"Scorpio":"your lucky colors are: scarlet, red and rust. \
your lucky Day is: tuesday. \
your best match for marriage and partnership is: taurus. \
your lucky numbers are: 8, 11, 18 and  22. \
your strengths are: resourceful, brave, passionate, determined and dedicated. \
your weaknesses are: distrusting, jealous, secretive and violent. \
you like: truth, facts, being loyal, being right, mysteries and  challenges. \
you dislike: dishonesty, revealing secrets and mind games. \
you are passionate and assertive. you are determined and decisive, and will research until you find out the truth. you are a great leader, always aware of the situation. \
you live to experience and express emotions. you keep secrets, whatever they may be.",\

"Sagittarius":"your lucky color is: blue. \
your lucky Day is: thursday. \
your best match for marriage and partnership is: gemini. \
your lucky numbers are: 3, 7, 9, 12 and 21. \
your strengths are: generous, idealistic and  great sense of humor. \
your weaknesses are: inability to fulfill promises, lacks patience and lack of tact. \
you like: freedom, travel, philosophy and being outdoors. \
you dislike: dishonesty, pessimism, restrictions and norms. \
you are curious and energetic, you are biggest traveller. your open mind and philosophical view motivates you to wander around the world in search of the meaning of life. \
you are extrovert, optimistic and enthusiastic, and like changes. you can transform your thoughts into concrete actions and you can do anything to achieve your goals. ",\

"Capricorn":"your lucky colors are: brown and black. \
your lucky day is: saturday. \
your best match for marriage and partnership is: cancer. \
your lucky numbers are: 4, 8, 13 and 22. \
your strengths are: responsible, disciplined, self-control, determined and good managing skills. \
your weaknesses are: pessimistic, greedy, cynical, fearful, ruthless in achieving a goal and rigid. \
you like: family, traditions, music and responsibility. \
you dislike: gossip, laziness, being angry and wasting time. \
you are very serious by nature. you possess an inner state of independence that enables significant progress both in your personal and professional lives. you are master of self-control and have the ability to lead the way, make solid and realistic plans, and manage many people who work for you at any time. you learn from your mistakes and get to the top based solely on your experience and expertise. "}
