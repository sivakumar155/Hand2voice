"""Phrase labels used by the gesture model and communication board.

The number keys are collection shortcuts, not universal sign-language meanings.
Choose and teach a comfortable, distinct gesture for each phrase with the user.
"""
PHRASES = {
    "1": "I need water",
    "2": "I am hungry",
    "3": "I need food",
    "4": "I need help",
    "5": "I am in pain",
    "6": "I need the bathroom",
    "7": "Please call a doctor",
    "8": "I need my family",
    "9": "Yes",
    "0": "No",

    'a': "i need medicine",
    'b':"i love you",
    'c':' i miss you',
    'd':"thank you",
}

CATEGORIES = {
    "Basic needs": [
        "I need water", "I am hungry", "I need food",
        "I need the bathroom", "I am tired", "I need to sit",
    ],
    "Emergency and health": [
        "I need help", "I am in pain", "Please call a doctor",
        "Call emergency services", "I need my medicine",
    ],
    "Daily communication": [
        "Hello", "Goodbye", "Yes", "No", "Please",
        "Thank you", "I am happy", "I am okay",
    ],
    "Feelings and comfort": [
        "I feel cold", "I feel hot", "I am scared",
        "I am sad", "I am uncomfortable",
    ],
}
