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
print(f"bye {name} it was nice talking to you today")