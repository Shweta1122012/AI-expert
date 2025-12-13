import time
import sys

lyrics = [
    "Tera mera afsana poora hoya naa jaana",
    "Pal-pal jeena muhaal mera tere bina",
    "Yeh saaray nashe bekaar teri aankhon ke siwa",
    "Ghar nahi jaata main bahar",
    "Rehta tera intezaar",
    "Mere khwabon mein aa naa kar ke solah singhaar",
    "Main ab kyun hosh mein aata nahi?",
    "Sukoon yeh dil kyun paata nahi?",
    "Kyun torrun khud se jo thay waaday",
    "Ke ab yeh ishq nibhaana nahi",
    "Main morhun tumse jo yeh chehra",
    "Dobara nazar milana nahi",
    "Yeh duniya jaane mera dard",
    "Tujhe yeh nazar kyun aata nahi",
    "Soneya yun tera sharmana meri jaan naa lele",
    "Kaan ke peeche zulf chhupana meri jaan kya kehne",
    "Zalima tauba tera nakhra iske waar kya kehne",
    "Thaam ke baithe dil ko ghaayal kahin haar naa baithe",
    "Teri nazrein mujhse kya kehti hain",
    "Inn mein wafa behti hai",
    "Thodi-thodi si raazi, thodi si khafa rehti hain",
    "Log hain zaalim bade inn mein jafa dekhi hai",
    "Yeh duniya teri nahi main ne tujh mein haya dekhi hai"
]

timings = [3, 3, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2]

typing_speed = 0.04  # Adjust typing effect speed here

for line, delay in zip(lyrics, timings):
    for char in line:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(typing_speed)
    print()
    time.sleep(delay)
