from colorama import init, Fore
import random

# Initialize colorama
init()

def get_player_choice():
    while True:
        choice = input(Fore.CYAN + "Enter your choice (rock/paper/scissors): " + Fore.RESET).lower()
        if choice in ['rock', 'paper', 'scissors']:
            return choice
        print(Fore.RED + "Invalid choice! Please try again." + Fore.RESET)

def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(player, computer):
    if player == computer:
        return "tie"
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        return "player"
    else:
        return "computer"

def play_game():
    print (Fore.GREEN+f"hey i am your game bot : "+Fore.RESET)
    print (Fore.YELLOW+f"whats your name?: "+Fore.RESET)
    name=input()
    
    print(Fore.GREEN + f"{name}, Welcome to Rock, Paper, Scissors!" + Fore.RESET)
    while True:
        player_choice = get_player_choice()
        computer_choice = get_computer_choice()
        
        print(Fore.YELLOW + f"\nYou chose: {player_choice}")
        print(f"Computer chose: {computer_choice}\n" + Fore.RESET)
        
        result = determine_winner(player_choice, computer_choice)
        
        if result == "tie":
            print(Fore.BLUE + "It's a tie!" + Fore.RESET)
        elif result == "player":
            print(Fore.GREEN + "You win!" + Fore.RESET)
        else:
            print(Fore.RED + "Computer wins!" + Fore.RESET)
            
        play_again = input(Fore.CYAN + "\nPlay again? (yes/no): " + Fore.RESET).lower()
        if play_again != 'yes':
            break
            
    print(Fore.GREEN +  " byeee Thanks for playing!" + Fore.RESET)

if __name__ == "__main__":
    play_game()