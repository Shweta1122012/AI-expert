import re , random 
from colorama import Fore, init
init(autoreset=True)
destinations={
    'beaches'  :['Bali','Maldives','Hawaii','Bahamas'],
    'mountains' :['Swiss Alps','Rocky Mountains','Himalayas','Andes'],
    'cities' :['Paris','New York','Tokyo','London'],
}
jokes=[
    "Why don't programmers like nature? Too many bugs!",

"Why did the computer go to the doctor? Because it had a virus!",

"Why do travelers always feel warm? Because of all their hot spots!"
]
def normalize_input(text):
    return re.sub(r"\s+"," ",text.strip().lower())
def recommend():
    print(Fore.CYAN+"travel bot :(beaches,mountains or cities)")
    prefrence=input(Fore.YELLOW+"you:")
    prefrence=normalize_input(prefrence)
    if prefrence in destinations:
        suggestion=random.choice(destinations[prefrence])
        print(Fore.GREEN+f"travel bot: {suggestion}")
        print(Fore.YELLOW+"TRAVEL BOT: do like the suggestion yes or no ?")
        answer=input(Fore.CYAN+"you:").lower()
        if answer=='yes':
            print(Fore.GREEN+"travel bot: glad you liked it !")
        elif answer=='no':
            print(Fore.RED+"travel bot: no worries, maybe next time !")
            recommend()
        else:
            print(Fore.BLUE+"travel bot: i didnt understand that")
            recommend()
    else:
        print(Fore.RED+"travel bot: i didnt understand that")
    showhelp()
def packing_tips():
    print(Fore.CYAN+"travel bot:where do you want to go?")
    location=normalize_input(input(Fore.YELLOW+"YOU:"))
    print(Fore.GREEN+f"travel bot: how many days?")
    days=input(Fore.YELLOW+"you:")
    print(f"packing tips for {location} for {days} days:")
    print(Fore.GREEN+" here are some packing tips:")
    print(Fore.CYAN+"1. Clothes appropriate for the weather")
    print(Fore.CYAN+"2. Comfortable shoes")
    print(Fore.CYAN+"3. Toiletries and personal items")
def tell_joke():
    print(Fore.CYAN+f"travel bot:{random.choice(jokes)}")
def showhelp():
    print(Fore.MAGENTA+"-i can")
    print(Fore.MAGENTA+"1.recommend a travel destination")
    print(Fore.MAGENTA+"2.give packing tips")
    print(Fore.MAGENTA+"3.tell a travel joke")
    print(Fore.MAGENTA+"type exit or bye to quit")
def chat():
    print (Fore.CYAN+"travel bot: hello i am travel bot")
    name=input(Fore.YELLOW+"travel bot: whats your name ?")
    print(Fore.CYAN+f"travel bot: nice to meet you {name}")
    showhelp()
    while True:
        user_input=input(Fore.YELLOW+"you: ")
        user_input=normalize_input(user_input)
        if "recommend" in user_input or "suggest" in user_input:
            recommend()
        elif "packing" in user_input or "pack" in user_input:
            packing_tips()
        elif "joke" in user_input or "funny" in user_input:
            tell_joke()
        elif "help" in user_input:
            showhelp()
        elif "exit" in user_input or "bye" in user_input:
            print(Fore.CYAN+"travel bot: bye bye , have a nice day !")
            break
        else:
            print(Fore.RED+"travel bot: i didnt understand that could you rephrase")
if __name__=="__main__":
    chat()
            


