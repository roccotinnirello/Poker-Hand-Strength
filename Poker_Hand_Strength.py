from itertools import combinations


def validCard(card):
    return len(card)==2 and card[0] in "23456789TJQKA" and card[1] in "cshd"


def straightHigh(values):
    values=set(values)
    if 14 in values:
        values.add(1)
    return max((high for high in range(5, 15)
                if set(range(high-4, high+1)).issubset(values)), default=0)


def straightFlushHigh():
    ranks={rank: value for value, rank in enumerate("23456789TJQKA", 2)}
    return max(straightHigh(ranks[card[0]] for card in cards
                           if card and card[1]==suit) for suit in "cshd")


def drawChance(condition):
    # Enumerate the remaining turn/river combinations, with no replacement.
    known=[card for card in cards if card]
    deck=[rank+suit for rank in "23456789TJQKA" for suit in "cshd"
          if rank+suit not in known]
    hits=total=0
    for drawn in combinations(deck, 7-len(known)):
        total+=1
        hits+=bool(condition(known+list(drawn)))
    return hits/total


def fullHouseCards(hand):
    counts=[sum(card[0]==rank for card in hand) for rank in "23456789TJQKA"]
    return max(counts)==3 and sum(count>=2 for count in counts)>=2


def printDraws():
    ranks={rank: value for value, rank in enumerate("23456789TJQKA", 2)}
    reverseRanks={value: rank for rank, value in ranks.items()}
    values={ranks[card[0]] for card in cards if card}
    high=straightHigh(values)
    missingCards=[rank for rank in range(2, 15) if rank not in values
                  and straightHigh(values | {rank})>high]
    if high and missingCards:
        chance=drawChance(lambda hand: straightHigh(ranks[card[0]] for card in hand)>high)
        print(f"You have a straight. Higher straight cards: {', '.join(reverseRanks[x] for x in missingCards)}. Chance of improving: {chance}")
    elif not high and missingCards:
        chance=drawChance(lambda hand: straightHigh(ranks[card[0]] for card in hand)>0)
        print(f"You are one card away from hitting a straight. You need one of the following cards: {', '.join(reverseRanks[x] for x in missingCards)}. Probability to hit straight: {chance}")
    elif not high and cards[5]=="":
        detectThreeStraight()

    for suit in "cshd":
        if sum(card.endswith(suit) for card in cards)==4:
            chance=drawChance(lambda hand: sum(card[1]==suit for card in hand)>=5)
            print(f"You are one card away from a flush. The chance of hitting it is {chance}")


placeInList=0
split1=0
split2=0
canProceed=False
flop=""
suit1=0
suit2=0
suit3=0
bestSet=""
cards=["", "", "", "", "", "", ""]
presence=0
foundStraight=False
foundFlush=False

while canProceed==False:
    choice=str(input("Would you like to calculate pre-flop hand strength with or without taking the flop, river and turn into account? (with or without): "))
    if choice=="without":
        HandStrengths=["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22","AKs", "AKo", "AQs", "AQo", "AJs", "AJo", "ATs", "ATo", "A9s", "A9o","A8s", "A8o", "A7s", "A7o", "A6s", "A6o", "A5s", "A5o", "A4s", "A4o","A3s", "A3o", "A2s", "A2o", "KQs", "KQo", "KJs", "KJo", "KTs", "KTo","K9s", "K9o", "K8s", "K8o", "K7s", "K7o", "K6s", "K6o", "K5s", "K5o","K4s", "K4o", "K3s", "K3o", "K2s", "K2o", "QJs", "QJo", "QTs", "QTo","Q9s", "Q9o", "Q8s", "Q8o", "Q7s", "Q7o", "Q6s", "Q6o", "Q5s", "Q5o","Q4s", "Q4o", "Q3s", "Q3o", "Q2s", "Q2o", "JTs", "JTo", "J9s", "J9o","J8s", "J8o", "J7s", "J7o", "J6s", "J6o", "J5s", "J5o", "J4s", "J4o","J3s", "J3o", "J2s", "J2o", "T9s", "T9o", "T8s", "T8o", "T7s", "T7o","T6s", "T6o", "T5s", "T5o", "T4s", "T4o", "T3s", "T3o", "T2s", "T2o","98s", "98o", "97s", "97o", "96s", "96o", "95s", "95o", "94s", "94o","93s", "93o", "92s", "92o", "87s", "87o", "86s", "86o", "85s", "85o","84s", "84o", "83s", "83o", "82s", "82o", "76s", "76o", "75s", "75o","74s", "74o", "73s", "73o", "72s", "72o", "65s", "65o", "64s", "64o", "63s", "63o", "62s", "62o", "54s", "54o", "53s", "53o", "52s", "52o","43s", "43o", "42s", "42o", "32s", "32o"]
        canProceed=True
    elif choice=="with":
        HandStrengths=["AA", "KK", "QQ", "JJ","AKs", "AQs", "AJs", "KQs", "KJs", "TT", "QJs", "AKo", "ATs", "KTs", "QTs", "JTs", "99", "AQo", "A9s", "KQo", "88", "A8s", "K9s", "Q9s", "T9s", "J9s", "A5s", "AJo", "77", "A7s", "A6s", "KJo", "A4s", "A3s", "QJo", "K8s", "66", "T8s", "J8s", "98s", "A2s", "ATo", "K7s", "Q8s", "KTo", "55", "JTo", "87s", "QTo", "44", "33", "22", "97s", "K6s", "K5s", "K4s", "T7s", "76s", "Q7s",  "K3s", "K2s", "J7s", "86s", "65s", "75s", "Q6s", "54s", "64s", "96s", "Q5s", "Q4s", "Q3s","Q2s", "T9o", "T6s", "A9o", "53s", "J6s", "85s", "J9o", "K9o", "J5s", "43s", "Q9o", "74s", "J4s", "J3s", "J2s", "95s", "63s", "A8o", "52s", "T5s", "T4s", "84s", "42s", "T3s", "T2s", "98o", "T8o", "A5o", "73s", "A7o", "A4o", "32s", "94s", "93s", "J8o", "A3o", "62s", "92s", "K8o", "A6o", "87o", "Q8o", "83s", "A2o", "82s", "97o", "72s", "K7o", "76o", "65o", "T7o", "K6o", "86o", "54o", "K5o", "J7o", "75o", "Q7o", "K4o", "K3o", "96o", "K2o", "64o", "Q6o", "53o", "85o", "T6o", "Q5o", "Q4o", "43o", "Q3o", "74o", "Q2o", "J6o", "63o", "J5o", "95o", "52o", "J4o", "J3o", "42o", "J2o", "84o", "T5o", "T4o", "32o", "T3o", "73o", "T2o", "62o", "94o", "93o", "92o", "83o", "82o", "72o"]
        canProceed=True
    else:
        print("That is not a valid answer. Try again")
canProceed=False

while canProceed==False:
    currentHand=str(input("What hand do you have? (Use format such as AcAs, AsKs (s for spades) or Th9c (for 10 of hearts and 9 of clubs): "))
    if (len(currentHand)==4 and validCard(currentHand[:2])
            and validCard(currentHand[2:]) and currentHand[:2]!=currentHand[2:]):
        canProceed=True
    else:
        print("Please try again, that hand is not correct")

cards[0]=currentHand[:2]
cards[1]=currentHand[2:]

for i in range(len(currentHand)):
    if currentHand[i]=="c" or currentHand[i]=="s" or currentHand[i]=="h" or currentHand[i]=="d" :
        if i>=3:
            split2=currentHand[i]
        else:
            split1=currentHand[i]



if split1==split2:
    rankedHand=currentHand.split(split1)[0]+currentHand.split(split1)[1].split(split2)[0]+"s"
elif currentHand.split(split1)[0]==currentHand.split(split1)[1].split(split2)[0]:
    rankedHand=currentHand.split(split1)[0]+currentHand.split(split1)[1].split(split2)[0]
else:
    rankedHand=currentHand.split(split1)[0]+currentHand.split(split1)[1].split(split2)[0]+"o"

if rankedHand not in HandStrengths:
    rankedHand=rankedHand[1]+rankedHand[0]+rankedHand[2:]
placeInList=HandStrengths.index(rankedHand)

handPercentile=((len(HandStrengths)-placeInList-1)/len(HandStrengths))*100
handPercentile=round(handPercentile, 1)
print("Your hand ranks above ", handPercentile, " percent of starting-hand types in the selected list")

def flopInp():
    canProceed=False
    while canProceed==False:
        flop=str(input("What is the first card of the flop? (Use same formatting as earlier): "))
        if validCard(flop) and flop not in cards:
            cards[2]=flop
            canProceed=True
        else:
            print("Please try again, that card is not correct")
    canProceed=False

    while canProceed==False:
        flop=str(input("What is the second card of the flop? (Use same formatting as earlier): "))
        if validCard(flop) and flop not in cards:
            cards[3]=flop
            canProceed=True
        else:
            print("Please try again, that card is not correct")
    canProceed=False

    while canProceed==False:
        flop=str(input("What is the third card of the flop? (Use same formatting as earlier): "))
        if validCard(flop) and flop not in cards:
            cards[4]=flop
            canProceed=True
        else:
            print("Please try again, that card is not correct")
    canProceed=False


def checkHand():
    print("")
    loopTimes=0
    counter=0
    foundStraight=False
    foundFlush=False
    royalFlush=False
    straightFlush=False
    fourOfAKind=False
    fullHouse=False
    threeOfAKind=False
    twoPair=False
    pair=False
    foundTen = foundJack = foundQueen = foundKing = foundAce = False

    ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    reverseRanks = {v: k for k, v in ranks.items()}
    cardsNum=[""]*7
    suits=[""]*7

    for i in range(len(cards)):
        if cards[i] != "":
            suits[i]=cards[i][1]

    cardsNum=sorted([ranks[card[0]] for card in cards if card])
    rankCount = {ran: cardsNum.count(ran) for ran in cardsNum}
    
    cardsNum=sorted(cardsNum)
    numOfCards={ran: cardsNum.count(ran) for ran in cardsNum}
    numOfSuits={suit: suits.count(suit) for suit in suits}
    foundStraight=bool(straightHigh(cardsNum))
    foundFlush=any(count>=5 for suit, count in numOfSuits.items() if suit)
    straightFlush=straightFlushHigh()
    if straightFlush==14:
        print("You have a royal flush")
    elif straightFlush:
        print("You have a straight flush")
    elif 4 in rankCount.values():
        fourOfAKind=True
        print("You have quads")
    elif 3 in rankCount.values() and sum(count>=2 for count in rankCount.values())>=2:
        fullHouse=True
        print("You have a full house")
    elif foundFlush:
        print("You have a flush")
    elif foundStraight:
        print("You have a straight")
    elif 3 in rankCount.values():
        threeOfAKind=True
        print("You have trips")
    elif list(rankCount.values()).count(2) >= 2:
        twoPair=True
        print("You have a two pair")
    elif 2 in rankCount.values():
        pair=True
        print("You have a pair")
    else: 
        print("You have high card")
        highCard=True

def detectThreeStraight():
    ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    reverseRanks = {v: k for k, v in ranks.items()}
    cardsNum=sorted([ranks[card[0]] for card in cards if card])
    values=set(cardsNum)
    printChance=False
    for high in range(5, 15):
        straightToCheck=list(range(high-4, high+1))
        if high==5:
            straightToCheck[0]=14
        missingCards=set(straightToCheck)-values
        if len(missingCards)==2 and len(cardsNum)==5:
            printChance=True
            print(f"You can get a straight. You need {' and '.join(reverseRanks[x] for x in sorted(missingCards))} to hit a straight from {reverseRanks[straightToCheck[0]]} to {reverseRanks[straightToCheck[4]]}")
    if printChance:
        chanceToHit=drawChance(lambda hand: straightHigh(ranks[card[0]] for card in hand)>0)
        print(f"Chance to get straight: {chanceToHit}")
    return printChance


def evalFlop():
    print("")
    straightCard=0
    possibleStraight=False
    possibleFlush=False
    straightNo=0
    missingCards=[]
    loopTimes=0
    foundFlush=False
    foundStraight=False
    fourOfAKind=False
    fullHouse=False
    threeOfAKind=False
    twoPair=False
    pair=False
    highCard=False
    chanceOfStraight=0
    chanceOfFlush=0
    chanceOfImprove=0
    chanceOfImprove2=0


    ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    reverseRanks = {v: k for k, v in ranks.items()}
    cardsNum=[""]*7
    suits=[""]*7
    for i in range(len(cards)):
        if cards[i] != "":
            suits[i]=cards[i][1]
    cardsNum=sorted([ranks[card[0]] for card in cards if card])
    rankCount = {ran: cardsNum.count(ran) for ran in cardsNum}
    
    numOfCards={ran: cardsNum.count(ran) for ran in cardsNum}
    numOfSuits={suit: suits.count(suit) for suit in suits}
    maxSuit=max(numOfSuits, key=numOfSuits.get)

    foundStraight=bool(straightHigh(cardsNum))
    foundFlush=any(count>=5 for suit, count in numOfSuits.items() if suit)
    straight=False
    flush=False
    printDraws()
    straightFlush=straightFlushHigh()
    if straightFlush==14:
        print("You have a royal flush")
        return
    elif straightFlush:
        print("You have a straight flush")
        return

    if 4 in rankCount.values():
        fourOfAKind=True
        fourNum=next((rank for rank, count in rankCount.items() if count == 4), None)
        fourVal=reverseRanks[fourNum]
    elif 3 in rankCount.values() and sum(count>=2 for count in rankCount.values())>=2:
        fullHouse=True
        houseNum=max(rank for rank, count in rankCount.items() if count == 3)
        houseNum2=max(rank for rank, count in rankCount.items() if count >= 2 and rank != houseNum)
        houseVal=reverseRanks[houseNum]
        houseVal2=reverseRanks[houseNum2]
    elif foundFlush:
        flush=True
    elif foundStraight:
        straight=True
    elif 3 in rankCount.values():
        threeOfAKind=True
        threeNum=next((rank for rank, count in rankCount.items() if count == 3), None)
        threeVal=reverseRanks[threeNum]
    elif list(rankCount.values()).count(2) >= 2:
        twoPair=True
    elif 2 in rankCount.values():
        pair=True
        twoNum=max(rank for rank, count in rankCount.items() if count == 2)
        twoVal=reverseRanks[twoNum]
    else:
        highCard=True
        highestCard=reverseRanks[max(cardsNum)]
        
    
    if fourOfAKind:
        print(f"You currently have quads of {fourVal}. Play aggressive")
    elif threeOfAKind:
        chanceOfImprove= 1 - ((46) / 47) * ((45) / 46)
        print(f"You have trips of {threeVal}. Chance of improving to quads: {chanceOfImprove}")
        chanceOfImprove=drawChance(fullHouseCards)
        print(f"Chance to improve to full house: {chanceOfImprove}")
        if threeNum!=14:
            print(f"Be careful of trips of {reverseRanks[threeNum+1]}")
        if threeVal!=cards[0][0] and threeVal!=cards[1][0]:
            print(f"Be careful of someone holding another {threeVal} to hit quads.")
    elif pair:
        chanceOfImprove = 1 - ((45) / 47) * ((44) / 46)
        chanceOfImprove2 = (2/47) * (1/46)
        print(f"You have a pair of {twoVal}s. Chance of hitting at least trips of this rank: {chanceOfImprove}. Chance of quads: {chanceOfImprove2}")
        if twoNum!=14:    
            print(f"Be careful of pairs of {reverseRanks[twoNum+1]} or higher")
        
        if twoVal!=cards[0][0] and twoVal!=cards[1][0]:
            print(f"Be careful of someone holding another {twoVal} to hit trips.")
    elif highCard:
        chanceOfImprove = 1 - ((44) / 47) * ((43) / 46)
        chanceOfImprove2 = (3/47) * (2/46)
        print(f"Chance of improving high card ({highestCard}) to at least a pair of this rank: {chanceOfImprove}. Chance to improve to trips: {chanceOfImprove2}.")
    elif fullHouse:
        chanceOfImprove=drawChance(lambda hand: any(sum(card[0]==rank for card in hand)==4 for rank in "23456789TJQKA"))
        print(f"You have a full house of {houseVal}s full of {houseVal2}. Chance of improving to quads: {chanceOfImprove}")
    elif twoPair:
        chanceOfImprove=drawChance(fullHouseCards)
        print(f"You have a two pair. Chance of improving to a full house: {chanceOfImprove}")
        print(f"If other players playing aggro, be careful of full houses. ")
    elif straight:
        print("Be careful of higher straights")
    elif flush:
        print("Be careful of higher flushes")
    
def turnInp():
    print("")
    canProceed=False
    while canProceed==False:
        flop=str(input("What is the turn? (Use same formatting as earlier): "))
        if validCard(flop) and flop not in cards:
            cards[5]=flop
            canProceed=True
        else:
            print("Please try again, that card is not correct")
    
def evalTurn():
    print("")
    straightCard=0
    possibleStraight=False
    possibleFlush=False
    straightNo=0
    missingCards=[]
    loopTimes=0
    foundFlush=False
    foundStraight=False
    fourOfAKind=False
    fullHouse=False
    threeOfAKind=False
    twoPair=False
    pair=False
    highCard=False
    chanceOfStraight=0
    chanceOfFlush=0
    chanceOfImprove=0
    chanceOfImprove2=0


    ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    reverseRanks = {v: k for k, v in ranks.items()}
    cardsNum=[""]*7
    suits=[""]*7
    for i in range(len(cards)):
        if cards[i] != "":
            suits[i]=cards[i][1]
    cardsNum=sorted([ranks[card[0]] for card in cards if card])
    rankCount = {ran: cardsNum.count(ran) for ran in cardsNum}
    
    numOfCards={ran: cardsNum.count(ran) for ran in cardsNum}
    numOfSuits={suit: suits.count(suit) for suit in suits}
    maxSuit=max(numOfSuits, key=numOfSuits.get)

    foundStraight=bool(straightHigh(cardsNum))
    foundFlush=any(count>=5 for suit, count in numOfSuits.items() if suit)
    straight=False
    flush=False
    printDraws()
    straightFlush=straightFlushHigh()
    if straightFlush==14:
        print("You have a royal flush")
        return
    elif straightFlush:
        print("You have a straight flush")
        return

    if 4 in rankCount.values():
        fourOfAKind=True
        fourNum=next((rank for rank, count in rankCount.items() if count == 4), None)
        fourVal=reverseRanks[fourNum]
    elif 3 in rankCount.values() and sum(count>=2 for count in rankCount.values())>=2:
        fullHouse=True
        houseNum=max(rank for rank, count in rankCount.items() if count == 3)
        houseNum2=max(rank for rank, count in rankCount.items() if count >= 2 and rank != houseNum)
        houseVal=reverseRanks[houseNum]
        houseVal2=reverseRanks[houseNum2]
    elif foundFlush:
        flush=True
    elif foundStraight:
        straight=True
    elif 3 in rankCount.values():
        threeOfAKind=True
        threeNum=next((rank for rank, count in rankCount.items() if count == 3), None)
        threeVal=reverseRanks[threeNum]
    elif list(rankCount.values()).count(2) >= 2:
        twoPair=True
    elif 2 in rankCount.values():
        pair=True
        twoNum=max(rank for rank, count in rankCount.items() if count == 2)
        twoVal=reverseRanks[twoNum]
    else:
        highCard=True
        highestCard=reverseRanks[max(cardsNum)]
        
    
    if fourOfAKind:
        print(f"You currently have quads of {fourVal}. Play aggressive")
    elif threeOfAKind:
        chanceOfImprove= 1 - ((45) / 46)
        print(f"You have trips of {threeVal}. Chance of improving to quads: {chanceOfImprove}")
        chanceOfImprove=drawChance(fullHouseCards)
        print(f"Chance to improve to full house: {chanceOfImprove}")
        if threeNum!=14:
            print(f"Be careful of trips of {reverseRanks[threeNum+1]}")

        if threeVal!=cards[0][0] and threeVal!=cards[1][0]:
            print(f"Be careful of someone holding another {threeVal} to hit quads.")
    elif pair:
        chanceOfImprove = 1 - ((44) / 46)
        print(f"You have a pair of {twoVal}s. Chance of hitting at least trips of this rank: {chanceOfImprove}")
        if twoNum!=14:    
            print(f"Be careful of pairs of {reverseRanks[twoNum+1]} or higher")
        
        if twoVal!=cards[0][0] and twoVal!=cards[1][0]:
            print(f"Be careful of someone holding another {twoVal} to hit trips.")
    elif highCard:
        chanceOfImprove = 1 - ((43) / 46)
        print(f"Chance of improving high card ({highestCard}) to at least a pair of this rank: {chanceOfImprove}")
    elif fullHouse:
        chanceOfImprove=drawChance(lambda hand: any(sum(card[0]==rank for card in hand)==4 for rank in "23456789TJQKA"))
        print(f"You have a full house of {houseVal}s full of {houseVal2}. Chance of improving to quads: {chanceOfImprove}")
    elif twoPair:
        chanceOfImprove=drawChance(fullHouseCards)
        print(f"You have a two pair. Chance of improving to a full house: {chanceOfImprove}")
        print(f"If other players playing aggro, be careful of full houses. ")
    elif straight:
        print("Be careful of higher straights")
    elif flush:
        print("Be careful of higher flushes")

def riverInp():
    print("")
    canProceed=False
    while canProceed==False:
        flop=str(input("What is the river? (Use same formatting as earlier): "))
        if validCard(flop) and flop not in cards:
            cards[6]=flop
            canProceed=True
        else:
            print("Please try again, that card is not correct")

def finalCheck():
    print("")
    straightCard=0
    possibleStraight=False
    possibleFlush=False
    straightNo=0
    missingCards=[]
    loopTimes=0
    foundFlush=False
    foundStraight=False
    fourOfAKind=False
    fullHouse=False
    threeOfAKind=False
    twoPair=False
    pair=False
    highCard=False
    chanceOfStraight=0
    chanceOfFlush=0
    chanceOfImprove=0
    chanceOfImprove2=0
    straight=False
    flush=False

    ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    reverseRanks = {v: k for k, v in ranks.items()}
    cardsNum=[""]*7
    suits=[""]*7
    for i in range(len(cards)):
        if cards[i] != "":
            suits[i]=cards[i][1]
    cardsNum=sorted([ranks[card[0]] for card in cards if card])
    rankCount = {ran: cardsNum.count(ran) for ran in cardsNum}
    
    numOfCards={ran: cardsNum.count(ran) for ran in cardsNum}
    numOfSuits={suit: suits.count(suit) for suit in suits}
    maxSuit=max(numOfSuits, key=numOfSuits.get)

    foundStraight=bool(straightHigh(cardsNum))
    foundFlush=any(count>=5 for suit, count in numOfSuits.items() if suit)
    straight=False
    flush=False
    straightFlush=straightFlushHigh()
    if straightFlush==14:
        print("You have a royal flush")
        return
    elif straightFlush:
        print("You have a straight flush")
        return

    if 4 in rankCount.values():
        fourOfAKind=True
        fourNum=next((rank for rank, count in rankCount.items() if count == 4), None)
        fourVal=reverseRanks[fourNum]
    elif 3 in rankCount.values() and sum(count>=2 for count in rankCount.values())>=2:
        fullHouse=True
        houseNum=max(rank for rank, count in rankCount.items() if count == 3)
        houseNum2=max(rank for rank, count in rankCount.items() if count >= 2 and rank != houseNum)
        houseVal=reverseRanks[houseNum]
        houseVal2=reverseRanks[houseNum2]
    elif foundFlush:
        flush=True
    elif foundStraight:
        straight=True
        print("You have a straight")
    elif 3 in rankCount.values():
        threeOfAKind=True
        threeNum=next((rank for rank, count in rankCount.items() if count == 3), None)
        threeVal=reverseRanks[threeNum]
    elif list(rankCount.values()).count(2) >= 2:
        twoPair=True
    elif 2 in rankCount.values():
        pair=True
        twoNum=max(rank for rank, count in rankCount.items() if count == 2)
        twoVal=reverseRanks[twoNum]
    else:
        highCard=True
        highestCard=reverseRanks[max(cardsNum)]
        
    if fourOfAKind:
        print(f"You currently have quads of {fourVal}. Play aggressive")
    elif threeOfAKind:
        print(f"You have trips of {threeVal}")
        if threeNum!=14:
            print(f"Be careful of trips of {reverseRanks[threeNum+1]} or full houses")
        if threeVal!=cards[0][0] and threeVal!=cards[1][0]:
            print(f"Be careful of someone holding another {threeVal} to hit quads.")
    elif pair:
        print(f"You have a pair of {twoVal}s")
        if twoNum!=14:
            print(f"Be careful of pairs of {reverseRanks[twoNum+1]} or higher")
        if twoVal!=cards[0][0] and twoVal!=cards[1][0]:
            print(f"Be careful of someone holding another {twoVal} to hit trips.")
    elif highCard:
        print(f"You've got a high card. Chance of other players beating you is high. Fold if there's a raise")
    elif fullHouse:
        print(f"You have a full house of {houseVal}s full of {houseVal2}.")
        print("Be aware of higher full houses")
    elif twoPair:
        print(f"You have a two pair")
        print(f"If other players playing aggro, be careful of full houses. ")
    elif straight:
        print(f"Be careful of higher straights")
    elif flush:
        print("You have a flush")
        print("Be careful of higher flushes")

flopInp()
checkHand()
evalFlop()
turnInp()
checkHand()
evalTurn()
riverInp()
finalCheck()