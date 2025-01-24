import random

while True:
    X = random.randint(0, 10)
    for i in range(3):
        guess = int(input("Enter your guess (0-10): "))
        if guess < X:
            print("The guessing number is greater than", guess)
        elif guess > X:
            print("The guessing number is less than", guess)
        else:
            print("Congrats, you've won!")
            break
    else:
        print("Sorry, you've lost. The correct number is", X)
    
    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again != "yes":
        print("Thanks for playing!")
        break
