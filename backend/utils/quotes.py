# Motivational Quotes Based on Emotions
# utils/quotes.py

EMOTION_QUOTES = {
    'happy': [
        "Keep that beautiful smile! Your happiness is contagious! 😊",
        "Your joy brightens the world around you! ✨",
        "Happiness looks great on you! Stay positive! 🌟",
        "Your smile is your superpower! Keep shining! ☀️",
        "What a wonderful expression of joy! Keep it up! 🎉"
    ],
    'sad': [
        "Every storm runs out of rain. This too shall pass. 🌈",
        "It's okay to feel sad. Tomorrow brings new hope. 💙",
        "Tough times don't last, but tough people do. You've got this! 💪",
        "Remember: after every sunset comes a sunrise. 🌅",
        "Your strength is greater than any struggle. Keep going! 🌟"
    ],
    'angry': [
        "Take a deep breath. You're stronger than this moment. 🧘",
        "Channel your energy into something positive. You've got this! 💪",
        "Every setback is a setup for a comeback. Stay strong! 🔥",
        "Anger is temporary, but your peace of mind is forever. Choose wisely. ☮️",
        "Transform your frustration into motivation. You're capable of greatness! ⚡"
    ],
    'surprised': [
        "Life is full of wonderful surprises! Embrace them! 🎁",
        "Your amazement shows you're truly living in the moment! ✨",
        "Stay curious, stay surprised, stay amazing! 🌟",
        "The world is full of wonders waiting to surprise you! 🎭",
        "Your enthusiasm is infectious! Keep that wonder alive! 🎪"
    ],
    'neutral': [
        "Balance is beautiful. You're doing great! ⚖️",
        "Calm and composed - a sign of inner strength! 🧘",
        "Your peaceful energy is admirable! 🕊️",
        "Sometimes the best response is calm presence. Well done! 🌊",
        "Your equilibrium shows wisdom beyond measure! 🎯"
    ],
    'fear': [
        "Courage isn't the absence of fear, it's acting despite it! 🦁",
        "You are braver than you believe. Face your fears! 💪",
        "Fear is temporary, regret is forever. You've got this! ⚡",
        "Every brave person was once afraid. You're on your way! 🌟",
        "Your courage will overcome any fear. Believe in yourself! 🔥"
    ],
    'disgust': [
        "Focus on what brings you joy, not what bothers you! 🌸",
        "Your discernment shows you know your worth! 💎",
        "Choose to see beauty in unexpected places! 🌺",
        "Your standards are high - that's a good thing! ⭐",
        "Transform negativity into positive energy! ✨"
    ]
}

def get_quote(emotion):
    """Get a random motivational quote based on emotion"""
    import random
    emotion = emotion.lower()
    
    if emotion in EMOTION_QUOTES:
        return random.choice(EMOTION_QUOTES[emotion])
    else:
        # Default motivational quote
        return "You are amazing just the way you are! Keep being you! 🌟"

def get_counting_message(count, object_type="objects"):
    """Get a message for object counting"""
    messages = {
        0: f"No {object_type} detected. Try adjusting your camera or image! 🔍",
        1: f"Found 1 {object_type[:-1]}! Perfect! ✨",
        2: f"Counted 2 {object_type}! Great! ✌️",
        3: f"I see 3 {object_type}! Nice! 👌",
        4: f"Found 4 {object_type}! Excellent! 🎯",
        5: f"Counted 5 {object_type}! High five! 🖐️",
    }
    
    if count in messages:
        return messages[count]
    elif count > 5:
        return f"Wow! Counted {count} {object_type}! Impressive! 🎉"
    else:
        return f"Detected {count} {object_type}! 👀"
