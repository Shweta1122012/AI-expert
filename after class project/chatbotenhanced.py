print ("hello i am ai bot whats your name?")
name=input()
print(f"hello {name} nice to meet you")
print("how are you feeling today(good/bad)?")
feeling=input().lower()
if feeling=="good":
    print("thats great to hear")
elif feeling=="bad":
    print("i am sorry to hear that")
else:
    print("i am not sure what you mean but i hope you have a good day")
print("do you want to hear a joke(yes/no)?")
joke_response=input().lower()
if joke_response=="yes":
    print("why did the scarecrow win an award? because he was outstanding in his field!")
elif joke_response=="no":
    print("no worries, maybe next time!")
else:
    print("i am not sure what you mean")
print("do you want to play a game(yes/no)?")
game_response=input().lower()
if game_response=="yes":
    print("great! let's play a guessing game. I'm thinking of a number between 1 and 5. Can you guess it?")
    import random
    number=random.randint(1,5)
    guess=int(input())
    if guess==number:
        print("wow! you guessed it right!")
    else:
        print(f"sorry, the correct number was {number}. better luck next time!")
else:
    print("no worries, maybe next time!")
print(f"bye {name} it was nice talking to you today")