import csv
import math

min_sup = float(input("Enter minimum support"))
min_conf = float(input("Enter minimum confidence"))

min_sup_count = math.ceil(min_sup * 14)
L1 = []
outlookSet, tempSet, humiditySet, windySet, ptSet = set(), set(), set(), set(), set()
body = {"item": "",
        "count": ""}
transactionList = []
afterSupportList = []
confidence = 0

# Creating a text file in write mode
text_file = open("Rules.txt", "w")

def dataInitialization():
    file = open("Play_Tennis_Data_Set.csv", "r+", encoding='utf-8-sig')
    csv_f = csv.reader(file)
    next(file)
    for row in csv_f:
        transactionList.append(row)

    with open("Play_Tennis_Data_Set.csv", "r+", encoding='utf-8-sig') as fin:
        for r in csv.DictReader(fin, delimiter=','):
            outlookSet.add(r["Outlook"])
            tempSet.add(r["Temperature"])
            humiditySet.add(r["Humidity"])
            windySet.add(r["Windy"])
            ptSet.add(r["PlayTennis"])
        fin.close()
    sortedoutlookSet = sorted(outlookSet)
    sortedtempSet = sorted(tempSet)
    sortedhumiditySet = sorted(humiditySet)
    sortedwindySet = sorted(windySet)
    sortedptSet = sorted(ptSet)

    for out in sortedoutlookSet:
        itemSet = []
        countKey = 0
        file.seek(0)
        for row in transactionList:
            if out in row:
                countKey += 1
        itemSet.append(out)
        body = {"item": itemSet, "count": countKey}
        if countKey >= min_sup_count:
            L1.append(body)

    for temp in sortedtempSet:
        itemSet = []
        countKey = 0
        for row in transactionList:
            if temp in row:
                countKey += 1
        itemSet.append(temp)
        body = {"item": itemSet, "count": countKey}
        if countKey >= min_sup_count:
            L1.append(body)

    for humidity in sortedhumiditySet:
        itemSet = []
        countKey = 0
        for row in transactionList:
            if humidity in row:
                countKey += 1
        itemSet.append(humidity)
        body = {"item": itemSet, "count": countKey}
        if countKey >= min_sup_count:
            L1.append(body)

    for wind in sortedwindySet:
        itemSet = []
        countKey = 0
        for row in transactionList:
            if wind in row:
                countKey += 1
        itemSet.append(wind)
        body = {"item": itemSet, "count": countKey}
        if countKey >= min_sup_count:
            L1.append(body)

    for pt in sortedptSet:
        itemSet = []
        countKey = 0
        for row in transactionList:
            if pt in row:
                countKey += 1
        itemSet.append(pt)
        body = {"item": itemSet, "count": countKey}
        if countKey >= min_sup_count:
            L1.append(body)
    return L1

# This module joins item sets and filters minimum support
def join(L_k, kitems):
    joinList = []
    for firstObj in L_k:
        subSet = set()
        multiListFirst = firstObj["item"]
        for x in multiListFirst:
            subSet.add(x)
        for secondObj in L_k:
            tempsubSet = set()
            finalsubSet = set()
            for x in subSet:
                finalsubSet.add(x)
            multiListSecond = secondObj["item"]
            if (multiListFirst == multiListSecond):
                continue
            for x in multiListSecond:
                tempsubSet.add(x)
            tempsubSet = tempsubSet.difference(subSet)
            for x in tempsubSet:
                finalsubSet.add(x)
            if finalsubSet not in joinList and (len(finalsubSet) == kitems):
                joinList.append(finalsubSet)
    return joinList

# This module calculates csupport count for formed generated itemsets
def countItemSets(L_k):
    countIncludedList = []
    for itemsets in L_k:
        count = 0
        for transactions in transactionList:
            if len(itemsets.difference(set(transactions))) == 0:
                count += 1
        body = {"item": list(itemsets), "count": count}
        if count >= min_sup_count:
            countIncludedList.append(body)
    return countIncludedList

# This module calculates confidence of each generated association rule and filters with the given input confidence value
def calculateConfidence(supportList):
    counter = 1
    finalList = []
    text_file.write("User Input:\n")
    text_file.write("-----------\n")
    text_file.write("{0}: {1}\n".format("Support", min_sup))
    text_file.write("{0}: {1}\n\n".format("Confidence", min_conf))
    text_file.write("Rules:\n")
    text_file.write("-----------\n")
    rightString = ""
    for support in supportList:
        dataSupport = round((support["count"]/14),2)
        dataItemSet = set(support["item"])
        for item in dataItemSet:
            totalCount = 0
            leftCount = 0
            temporarySet = set()
            leftCountAlternate = 0
            temporarySet.add(item)
            differenceSet = dataItemSet.difference(temporarySet)
            leftItemCategory = identifyCategory(item)
            for transactions in transactionList:
                if len(temporarySet.difference(set(transactions))) == 0:
                    leftCount += 1
                if len(differenceSet.difference(transactions)) == 0:
                    leftCountAlternate += 1
                if len(set(dataItemSet).difference(set(transactions))) == 0:
                    totalCount += 1
            confidence = round(totalCount/leftCount, 2)
            confidenceleftAlternate = round(totalCount / leftCountAlternate, 2)
            if confidence >= min_conf: # Association rule
                text_file.write("Rule#{0}: \n{{{1}={2}}} => ".format(counter, leftItemCategory, item ))
                text_file.write("{")
                tempStringList = []
                for difference in differenceSet:
                    tempString =  identifyCategory(difference) + "=" + difference
                    tempStringList.append(tempString)
                    rightString = ",".join(tempStringList)
                text_file.write(rightString)
                text_file.write("}")
                text_file.write("\n")
                text_file.write("(Support={}, Confidence={})".format(dataSupport, confidence))
                text_file.write("\n\n\n")
                counter += 1
            if confidenceleftAlternate >= min_conf and len(dataItemSet) > 2: # Reverse Association rule
                tempStringList = []
                text_file.write("Rule#{0}: \n{{{1}}} => ".format(counter, rightString))
                text_file.write("{{{1}={2}}}".format(counter, leftItemCategory, item))
                text_file.write("\n")
                text_file.write("(Support={}, Confidence={})".format(dataSupport, confidenceleftAlternate))
                text_file.write("\n\n\n")
                counter += 1
        if len(dataItemSet) > 3:
            counter = largeItemSets(dataItemSet, dataSupport, counter)



# returns category when keyword is given in input
def identifyCategory(receiveItem):
    leftCategory = ""
    if receiveItem in outlookSet:
        leftCategory = "Outlook"
    elif receiveItem in tempSet:
        leftCategory = "Temperature"
    elif receiveItem in humiditySet:
        leftCategory = "Humidity"
    elif receiveItem in windySet:
        leftCategory = "Windy"
    elif receiveItem in ptSet:
        leftCategory = "PlayTennis"
    return leftCategory


def largeItemSets(receiveddataItemSet, receivedSupport, receivedCounter):
    count = 0
    checkList = []
    for individual in receiveddataItemSet:

        setCount = 0
        diffCount = 0
        altCount = 0
        largeConfidence = 0
        largeAltConf = 0
        rule = ""

        for innerIndividual in receiveddataItemSet:
            thirdSet = set()
            if individual == innerIndividual:
                continue
            thirdSet.add(individual)
            thirdSet.add(innerIndividual)
            if sorted(thirdSet) in checkList:
                continue
            checkList.append(sorted(thirdSet))
            largeDiffSet = receiveddataItemSet.difference(thirdSet)
            for transactionCheck in transactionList:
                if len(thirdSet.difference(set(transactionCheck))) == 0:
                    setCount += 1
                if len(set(largeDiffSet).difference(set(transactionCheck))) == 0:
                    altCount += 1
                if len(set(receiveddataItemSet).difference(set(transactionCheck))) == 0:
                    diffCount += 1
            largeConfidence = round(diffCount / setCount, 2)
            largeAltConf = round(diffCount / altCount, 2)
            if largeConfidence >= min_conf: # Association rule
                tempStringListla = []
                for difference in largeDiffSet:
                    tempString = identifyCategory(difference) + "=" + difference
                    tempStringListla.append(tempString)
                    rule = ",".join(tempStringListla)
                count += 1
                text_file.write("Rule#{0}: \n{{{1}}} => ".format(receivedCounter, rule))
                tempStringListla = []
                for subla in thirdSet:
                    tempString = identifyCategory(subla) + "=" + subla
                    tempStringListla.append(tempString)
                    rule = ",".join(tempStringListla)
                text_file.write("{{{0}}}".format(rule))
                # text_file.write("{{{1}={2}}}".format(counter, leftItemCategory, item))
                text_file.write("\n")
                text_file.write("(Support={}, Confidence={})".format(receivedSupport, largeConfidence))
                text_file.write("\n\n\n")
                receivedCounter += 1
            if largeAltConf >= min_conf: # Reverse Association rule
                tempStringListla = []
                for subla in thirdSet:
                    tempString = identifyCategory(subla) + "=" + subla
                    tempStringListla.append(tempString)
                    rule = ",".join(tempStringListla)
                count += 1
                text_file.write("Rule#{0}: \n{{{1}}} => ".format(receivedCounter, rule))
                tempStringListla = []
                for difference in largeDiffSet:
                    tempString = identifyCategory(difference) + "=" + difference
                    tempStringListla.append(tempString)
                    rule = ",".join(tempStringListla)
                text_file.write("{{{0}}}".format(rule))
                # text_file.write("{{{1}={2}}}".format(counter, leftItemCategory, item))
                text_file.write("\n")
                text_file.write("(Support={}, Confidence={})".format(receivedSupport, largeAltConf))
                text_file.write("\n\n\n")
                receivedCounter += 1
    return receivedCounter





if (min_sup < 0 or min_sup > 1) and (min_conf < 0 or min_conf > 1):
    print("minimum support and minimum confidence should be between 0 and 1")
elif min_sup < 0 or min_sup > 1:
    print("minimum support value should be fractional value lying between 0 amd 1")
elif min_conf < 0 or min_conf > 1:
    print("minimum Confidence value should be fractional value lying between 0 amd 1")
else:
    L1 = dataInitialization()
    joinList = join(L1,2)
    kitems = 3
    while True: # Looping till the itemsets returned are null
        countList = countItemSets(joinList)
        if len(countList) == 0:
            break
        afterSupportList = countList
        joinList = join(countList, kitems)
        kitems += 1
    calculateConfidence(afterSupportList) # Checking for minimum confidence and filtering item sets
    print("Rules Written to Rules.txt file")


