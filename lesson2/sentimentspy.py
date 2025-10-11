import colorama 
from colorama import Fore, Style
from textblob import TextBlob
colorama.init()
print(Fore.RED + "hello i am ai bot ?"+Style.RESET_ALL)
user_name=input(f"{Fore.GREEN}what is your name ? {Style.RESET_ALL}").strip()
if not user_name:
    user_name="mystry agent"
conversation_history=[]
print(f"{Fore.CYAN}hello agent {user_name}")
print (f"type a sentence and i will analize your sentences with textblob and show you the sentiment")
print(f"type {Fore.YELLOW},'reset'{Fore.BLUE},{Fore.YELLOW} 'history'{Fore.BLUE},{Fore.YELLOW} 'exit'{Fore.BLUE}to quit.{Style.RESET_ALL}")
while True:
    user_input=input(f"{Fore.GREEN}>>{Style.RESET_ALL}").strip()
    if not user_input:
        print(f"{Fore.RED}please type something{Style.RESET_ALL}")
        continue
    if user_input.lower()=='exit':
        print(f"{Fore.CYAN}bye bye agent {user_name}, have a nice day!👌{Style.RESET_ALL}")
        break
    elif user_input.lower()=='reset':
        conversation_history.clear()
        print(f"{Fore.GREEN}coneverastion history cleared{Style.RESET_ALL}")
        continue
    elif user_input.lower()=='history':
        if not conversation_history:
            print(f"{Fore.RED}no conversation history{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}conversation history:{Style.RESET_ALL}")
            for i ,(text,polarity,sentiment) in enumerate (conversation_history,start=1):
                if sentiment=='positive':
                    color=Fore.GREEN
                    emoji='😊'
                elif sentiment=='negative':
                    color=Fore.RED
                    emoji='😞'
                else:
                    color=Fore.YELLOW
                    emoji='😐'
                print(f"{i}.{color}{emoji} {text} "
                      f"(polarity: {polarity:.2f}, sentiment type: {sentiment}{Style.RESET_ALL})")
        continue
    polarity=TextBlob(user_input).sentiment.polarity
    if polarity >0.25:
        sentiment='positive'
        emoji='😊'
        color=Fore.GREEN    
    elif polarity <-0.25:
        sentiment='negative'
        emoji='😞'
        color=Fore.RED
    else:
        sentiment='neutral'
        emoji='😐'
        color=Fore.YELLOW
    conversation_history.append((user_input,polarity,sentiment))
    print(f"{color}{emoji} your sentence is {sentiment}(polarity: {polarity:.2f}){Style.RESET_ALL}")

      
        
        

