import re
import random
from datetime import datetime, timedelta
from colorama import Fore, init

init(autoreset=True)

locations = {
    "bali": {"temp_min": 24, "temp_max": 32, "conditions": ["sunny", "partly cloudy", "rainy"]},
    "maldives": {"temp_min": 25, "temp_max": 33, "conditions": ["sunny", "humid", "thunderstorms"]},
    "hawaii": {"temp_min": 22, "temp_max": 30, "conditions": ["sunny", "trade winds", "showers"]},
    "paris": {"temp_min": 5, "temp_max": 22, "conditions": ["sunny", "cloudy", "drizzle"]},
    "new york": {"temp_min": -5, "temp_max": 30, "conditions": ["snow", "rain", "sunny", "cloudy"]},
    "tokyo": {"temp_min": 2, "temp_max": 31, "conditions": ["sunny", "rain", "humid"]},
    "london": {"temp_min": 0, "temp_max": 20, "conditions": ["drizzle", "cloudy", "sunny"]},
    "default": {"temp_min": -10, "temp_max": 35, "conditions": ["sunny", "cloudy", "rainy", "snow", "windy"]},
}

weather_jokes = [
    "Why did the woman go outdoors with her purse open? Because she expected some change in the weather.",
    "What did one tornado say to the other? I love your twists and turns!",
    "Why don't weather reporters need to be good at math? Because they already know all about degrees."
]

def normalize_input(text):
    return re.sub(r"\s+", " ", text.strip().lower())

def generate_weather_for_location(loc_key):
    data = locations.get(loc_key, locations["default"])
    temp = random.randint(data["temp_min"], data["temp_max"])
    condition = random.choice(data["conditions"])
    feels_like = temp + random.choice([-2, -1, 0, 1, 2])
    wind_kph = random.randint(0, 40)
    humidity = random.randint(30, 90)
    return {"temp": temp, "feels_like": feels_like, "condition": condition,
            "wind_kph": wind_kph, "humidity": humidity}

def clothing_advice(temp_c):
    if temp_c <= 0:
        return ["heavy coat", "hat", "gloves", "warm boots"]
    if temp_c <= 10:
        return ["coat", "layered clothing", "closed shoes"]
    if temp_c <= 20:
        return ["jacket or sweater", "comfortable shoes"]
    if temp_c <= 25:
        return ["light jacket", "t-shirt", "sneakers"]
    return ["light clothing", "shorts", "sandals", "sun protection"]

def show_help():
    print(Fore.MAGENTA + "- I can:")
    print(Fore.MAGENTA + "1. give current weather for a place (type: weather in <place>)")
    print(Fore.MAGENTA + "2. give a multi-day forecast (type: forecast for <days> days in <place>)")
    print(Fore.MAGENTA + "3. give packing/clothing tips for a place (type: tips for <place>)")
    print(Fore.MAGENTA + "4. tell a weather joke (type: joke)")
    print(Fore.MAGENTA + "type exit or bye to quit")

def report_weather(user_text):

    parts = user_text.replace("in ", " ").split()
    
    loc_candidates = [p for p in parts if p in locations]
    loc = loc_candidates[0] if loc_candidates else parts[-1] if parts else ""
    loc_key = normalize_input(loc)
    weather = generate_weather_for_location(loc_key)
    print(Fore.CYAN + f"weather bot: current weather for {loc_key or 'your location'}")
    print(Fore.GREEN + f"Condition: {weather['condition'].capitalize()}")
    print(Fore.GREEN + f"Temperature: {weather['temp']}°C (feels like {weather['feels_like']}°C)")
    print(Fore.GREEN + f"Humidity: {weather['humidity']}%   Wind: {weather['wind_kph']} kph")
    advice = clothing_advice(weather['feels_like'])
    print(Fore.YELLOW + "Suggested clothing: " + ", ".join(advice))

def forecast(user_text):
    
    tokens = user_text.split()
    days = 3  # default
    for i, t in enumerate(tokens):
        if t.isdigit():
            days = max(1, min(7, int(t)))  

    loc_candidates = [t for t in tokens if t in locations]
    loc_key = loc_candidates[0] if loc_candidates else (tokens[-1] if tokens else "")
    loc_key = normalize_input(loc_key)
    print(Fore.CYAN + f"weather bot: {days}-day forecast for {loc_key or 'your location'}")
    for i in range(days):
        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        w = generate_weather_for_location(loc_key)
        print(Fore.GREEN + f"{date}: {w['condition'].capitalize()}, {w['temp']}°C (feels {w['feels_like']}°C), "
              f"Humidity {w['humidity']}%, Wind {w['wind_kph']} kph")

def packing_tips_for_weather(user_text):
    
    tokens = user_text.split()
    loc_candidates = [t for t in tokens if t in locations]
    loc_key = loc_candidates[0] if loc_candidates else (tokens[-1] if tokens else "")
    loc_key = normalize_input(loc_key)
    w = generate_weather_for_location(loc_key)
    print(Fore.CYAN + f"weather bot: packing/clothing tips for {loc_key or 'your location'} (typical now)")
    print(Fore.GREEN + f"Expected: {w['condition'].capitalize()}, {w['temp']}°C")
    advice = clothing_advice(w['feels_like'])
    for idx, item in enumerate(advice, 1):
        print(Fore.CYAN + f"{idx}. {item}")
    if w['condition'] in ["rainy", "drizzle", "showers", "thunderstorms"]:
        print(Fore.CYAN + "Bring a waterproof jacket or umbrella.")
    if w['condition'] in ["snow"]:
        print(Fore.CYAN + "Consider insulated boots and thermal layers.")

def tell_joke():
    print(Fore.CYAN + f"weather bot: {random.choice(weather_jokes)}")

def chat():
    print(Fore.CYAN + "weather bot: hello i am weather bot")
    name = input(Fore.YELLOW + "weather bot: whats your name? ")
    name = normalize_input(name).title()
    print(Fore.CYAN + f"weather bot: nice to meet you {name}")
    show_help()
    while True:
        user_input = input(Fore.YELLOW + "you: ")
        user_input_norm = normalize_input(user_input)
        if not user_input_norm:
            print(Fore.RED + "weather bot: please say something or type help")
            continue
        if "weather" in user_input_norm or user_input_norm.startswith("in "):
            report_weather(user_input_norm)
        elif "forecast" in user_input_norm:
            forecast(user_input_norm)
        elif "tips" in user_input_norm or "packing" in user_input_norm or "clothing" in user_input_norm:
            packing_tips_for_weather(user_input_norm)
        elif "joke" in user_input_norm or "funny" in user_input_norm:
            tell_joke()
        elif "help" in user_input_norm:
            show_help()
        elif "exit" in user_input_norm or "bye" in user_input_norm:
            print(Fore.CYAN + "weather bot: bye bye, stay safe!")
            break
        else:
            print(Fore.RED + "weather bot: i didnt understand that, could you rephrase or type help?")

if __name__ == "__main__":
    chat()