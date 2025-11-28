#GroceryStoreSim.py
#Name: Blake Green
#Date:11/24/25
#Assignment: Lab 11

import simpy
import random

eventLog = []
waitingShoppers = []
idleTime = 0

def shopper(env, id):
    arrive = env.now
    items = random.randint(5, 20)
    shoppingTime = items / 2
    yield env.timeout(shoppingTime)
    waitingShoppers.append((id, items, arrive, env.now))

def checker(env):
    global idleTime
    while True:
        if len(waitingShoppers) == 0:
            idleTime = idleTime + 1
            yield env.timeout(1)
        else:
            customer = waitingShoppers.pop(0)
            items = customer[1]
            checkoutTime = (items / 10) + 1
            yield env.timeout(checkoutTime)
            eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))

def customerArrival(env):
    num = 0
    while True:
        num = num + 1
        env.process(shopper(env, num))
        yield env.timeout(2)

def processResults():
    totalWait = 0
    total = 0
    totalItems = 0
    totalShopping = 0
    maxWait = 0

    for e in eventLog:
        waitTime = e[4] - e[3]
        shoppingTime = e[3] - e[2]
        items = e[1]

        totalWait = totalWait + waitTime
        totalItems = totalItems + items
        totalShopping = totalShopping + shoppingTime

        if waitTime > maxWait:
            maxWait = waitTime

        total = total + 1

    if total > 0:
        print("Number of shoppers:", total)
        print("Average items purchased:", totalItems / total)
        print("Total idle time:", idleTime)
        print("Average wait time:", totalWait / total)
        print("Average shopping time:", totalShopping / total)
        print("Max wait time:", maxWait)

def main():
    env = simpy.Environment()
    env.process(customerArrival(env))
    i = 0
    while i < 5:
        env.process(checker(env))
        i = i + 1
    env.run(until=180)
    print("Shoppers still waiting:", len(waitingShoppers))
    processResults()

main()

