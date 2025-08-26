import random
num = random.randint(1,50)
for ettempt in range(1,4):
    user =int(input(f"Please {ettempt} -Enter the number  "))
    if user >num :
        print('num is lesser than guess num')
    elif user < num:
        print ('your guess num is greater ')
    else :
        print ("you won the game ")
        print(f"you won the in {ettempt} - tries ")
    break 
else:
    print(f"sorry you lose the game -the random num is {ettempt}")
        