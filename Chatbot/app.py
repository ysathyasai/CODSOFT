"""
Simple rule-based chatbot using Flask.

This module serves a small web UI and answers user messages using explicit
if/elif/else statements (no external dataset). The rules are written directly
in code so the bot responds deterministically to common queries.
"""

from flask import Flask, render_template, request, jsonify
import re
import random
from datetime import datetime, date


# Flask app instance
app = Flask(__name__)


# -------------------------
# Rule-based chatbot logic
# -------------------------
def get_bot_response(message: str) -> str:
    """Return a short reply for a given user message using explicit rules.

    This implementation does not consult an external dataset. It uses a
    prioritized if/elif/else chain to produce one reply per message.
    """
    msg = (message or '').lower().strip()

    # quick empty guard
    if not msg:
        return "I didn't catch that — could you please type something?"

    # Response pools
    greetings = [
        "Hey there! How are you doing today?",
        "Hello! Nice to meet you — what's on your mind?",
        "Hi! I'm here to chat whenever you're ready.",
        "Hey! How's your day going so far?",
        "Hi there! What would you like to talk about?",
    ]

    farewells = [
        "Goodbye, come chat again soon!",
        "See you later — take care!",
        "Bye! It was great talking with you.",
        "Catch you later!",
    ]

    thanks = [
        "You're welcome!",
        "No problem — happy to help!",
        "Anytime! If you have more questions, just ask.",
    ]

    jokes = [
        "Why did the computer catch a cold? It left its Windows open.",
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why was the robot so bad at soccer? It kept stopping to recharge its batteries.",
        "I would tell you a UDP joke, but you might not get it.",
        "Why don't keyboards sleep? They have two shift keys.",
    ]

    weather_replies = [
        "I can't check real-time weather, but I hope it's nice where you are!",
        "I don't have live weather data, but remember: an umbrella is handy if clouds appear.",
        "Can't fetch live weather here — try a weather website or app for the latest forecast.",
    ]

    colors = ["blue", "green", "purple", "teal", "amber", "mint"]

    hobbies = [
        "I enjoy 'reading' logs and learning from examples.",
        "I like talking about ideas and trying to be helpful.",
    ]

    advice = [
        "If you're stuck, try breaking the problem into smaller steps.",
        "Taking a short break often helps recharge your focus.",
    ]

    quotes = [
        "The only limit to our realization of tomorrow is our doubts of today. — F. D. Roosevelt",
        "Code is like humor. When you have to explain it, it’s bad. — Cory House",
    ]

    # prepare matchers used by some branches
    math_match = re.search(r"what(?:'s| is)?\s+(-?\d+(?:\.\d+)?)\s*([+\-*/x×])\s*(-?\d+(?:\.\d+)?)", msg)
    echo_match = re.search(r"\b(?:repeat after me|say)\s+(.+)", msg)

    # 1) Greetings
    if re.search(r"\b(hi|hello|hey|hiya|good\s(morning|afternoon|evening))\b", msg):
        return random.choice(greetings)

    # 2) Farewell
    elif re.search(r"\b(bye|goodbye|see you|see ya|later|farewell)\b", msg):
        return random.choice(farewells)

    # 3) Thanks / gratitude
    elif re.search(r"\b(thank(s| you)?|thx|ty)\b", msg):
        return random.choice(thanks)

    # 4) Asking for the bot's name or identity
    elif re.search(r"\b(your name|what.?s your name|who are you|identify yourself)\b", msg):
        return "I'm your friendly rule-based chatbot!"

    # 5) Creator / origin
    elif re.search(r"\b(who (made|created) you|who (is )?your creator|built you)\b", msg):
        return "I was created by a developer using Python and Flask — you can expand my rules anytime!"

    # 6) Jokes / humor
    elif re.search(r"\b(joke|tell me a joke|make me laugh|funny)\b", msg):
        return random.choice(jokes)

    # 7) Weather-related
    elif re.search(r"\b(weather|rain|sunny|cloudy|temperature|forecast)\b", msg):
        return random.choice(weather_replies)

    # 8) Time and date
    elif re.search(r"\b(time|current time|what time)\b", msg):
        now = datetime.now().strftime("%H:%M:%S")
        return f"The current time is {now}."

    elif re.search(r"\b(date|today's date|what date|today date)\b", msg):
        today = date.today().isoformat()
        return f"Today's date is {today}."

    # 9) Day of the week
    elif re.search(r"\b(day|weekday|what day|which day)\b", msg):
        weekday = datetime.now().strftime("%A")
        return f"Today is {weekday}."

    # 10) How are you / status
    elif re.search(r"\b(how are you|how's it going|how are things|how you doing)\b", msg):
        return "I'm a program, so I don't have feelings, but I'm running smoothly and ready to chat!"

    # 11) Mood / feelings empathy
    elif re.search(r"\b(sad|unhappy|depressed|upset|angry|down)\b", msg):
        return "I'm sorry you're feeling that way. If you'd like to talk about it, I'm here to listen."

    # 12) Favorite color
    elif re.search(r"\b(favorite color|favourite colour|what color do you like|favou?rite color)\b", msg):
        return f"I like {random.choice(colors)} — it's soothing for bot eyes."

    # 13) Basic math like 'what is 2 + 2' or 'calculate 7*8'
    elif math_match:
        a = float(math_match.group(1))
        op = math_match.group(2)
        b = float(math_match.group(3))
        try:
            if op in ['+', 'plus']:
                res = a + b
            elif op in ['-', '−', 'minus']:
                res = a - b
            elif op in ['*', 'x', '×']:
                res = a * b
            elif op == '/':
                if b == 0:
                    return "I can't divide by zero."
                res = a / b
            else:
                return "I couldn't parse that operator. Try +, -, * or /."
            if float(res).is_integer():
                res = int(res)
            return f"The answer is {res}."
        except Exception:
            return "I couldn't compute that — maybe check the numbers?"

    # 14) Ask for help or capabilities
    elif re.search(r"\b(help|what can you do|capabilities|features|commands)\b", msg):
        return (
            "I can respond to greetings, tell jokes, report the current time/date, do simple math, "
            "and answer other simple questions. Try: 'Hi', 'Tell me a joke', 'What time is it?', or 'What is 3 + 4'."
        )

    # 15) Privacy-safe replies to personal info requests
    elif re.search(r"\b(age|how old are you|phone|address|social security|ssn|email)\b", msg):
        return "I don't share personal or private information. I'm a simple demo chatbot."

    # 16) Echo / repeat
    elif echo_match:
        to_say = echo_match.group(1).strip()
        return f"You asked me to say: {to_say}"

    # 17) Ask for example conversation or sample commands
    elif re.search(r"\b(example|sample|commands|usage)\b", msg):
        return (
            "Try: 'Hi', 'What's your name?', 'Tell me a joke', 'What time is it?', 'What is 3 + 4', 'What's the weather like?', or 'Bye'."
        )

    # 18) If user says they like something, respond amicably
    elif re.search(r"\b(i like|i love|i enjoy|i'm into)\b", msg):
        return "That's great! It's nice to hear what you enjoy."

    # 19) Compliment / small talk
    elif re.search(r"\b(nice|cool|awesome|great|good job|well done)\b", msg):
        return "Thanks! I try my best to be helpful."

    # 20) Hobbies or interests
    elif re.search(r"\b(hobby|hobbies|what do you do for fun|interests)\b", msg):
        return random.choice(hobbies)

    # 21) Simple advice
    elif re.search(r"\b(advice|suggest|tip|tips)\b", msg):
        return random.choice(advice)

    # 22) Quotes
    elif re.search(r"\b(quote|inspire|motivate|motivation)\b", msg):
        return random.choice(quotes)

    # 23) Programming related (simple)
    elif re.search(r"\b(programming|code|python|javascript|java|bug|debug)\b", msg):
        return "I can talk about programming basics. What's your language or question?"

    # 24) Food / breakfast / coffee small talk
    elif re.search(r"\b(food|hungry|breakfast|lunch|dinner|coffee|tea)\b", msg):
        return "I don't eat, but I can help you find a recipe or suggest something tasty!"

    # 25) Small talk about news or current events
    elif re.search(r"\b(news|updates|headlines|current events)\b", msg):
        return "I don't fetch live news here, but you can check a news site or ask me for general topics."

    # 26) Favorite programming language (playful)
    elif re.search(r"\b(favorite language|fav programming|what language)\b", msg):
        return "I speak JSON, Python, and a little bit of human. 😉"

    # 27) Fallback: default reply with a tip so user knows what to try next
    else:
        fallback_responses = [
            "I didn't quite understand that. Try asking for the time, a joke, or say 'help'.",
            "Huh — I don't know that one yet. Ask me for a joke or the time, or try a different phrase.",
            "I'm still learning new phrases. You can ask me 'What can you do?' for ideas.",
        ]
        return random.choice(fallback_responses)

# -------------------------
# Flask routes
# -------------------------

@app.route('/')
def index():
    """Serve the main chat page. The template contains a small frontend that posts user
    messages to the `/chat` endpoint and displays replies."""
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """Receive a JSON payload with a user message and return a JSON response with the bot's reply.

    Expected JSON body: {"message": "..."}
    Response JSON: {"reply": "..."}
    """
    data = request.get_json(force=True)
    user_message = data.get('message', '')

    # Get the bot reply using the rule engine
    reply = get_bot_response(user_message)

    # Return a JSON response to the frontend's fetch request
    return jsonify({'reply': reply})


# Run the Flask development server when invoked directly. In production you would use a WSGI server.
if __name__ == '__main__':
    # Debug mode is useful during development. Remove debug=True in production.
    # Start the server and listen on all interfaces so the app is reachable from
    # forwarded ports or other machines on the network.
    app.run(debug=True, host="0.0.0.0", port=5000)
