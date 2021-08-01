import csv

inputList = []

# Reading input
min_sup = input("Enter minimum support")

itemSet, locationSet, yearSet, productSet, locSet = set(), set(), set(), set(), set()
filteredItemSet, filteredItemLocationSet = [],[]
# Temporary set for reference if items not present
regionSet = set()
regionSet.add("New York")
regionSet.add("Vancouver")
regionSet.add("Chicago")
regionSet.add("Toronto")
inventorySet = set()
inventorySet.add("Computer")
inventorySet.add("Camera")
inventorySet.add("Phone")
inventorySet.add("Printer")



# Creating a text file in write mode
text_file = open("Iceberg-Cube-Results.txt", "w")


def BUC(inputList,dimension):
    with open("Product_Sales_Data_Set.csv", "r+", encoding='utf-8-sig') as fin:
        if dimension == 1:
            for r in csv.DictReader(fin, delimiter=','):
                itemSet.add(r["Item"])
            text_file.write("\n(Item) Cuboid:\n\n")
            text_file.write("{0:1}{1:18}{2}".format("","Item", "Sales_Units"))
            text_file.write("\n----------------------------------\n")
            fin.seek(0)
            for item in itemSet:
                fin.seek(0)
                total = sum(int(r["Sales_Units"]) for r in csv.DictReader(fin, delimiter=',') if r["Item"] == item)
                if total >= int(min_sup):
                    text_file.write("{0:23}{1}".format(item, total))
                    text_file.write("\n")
                    filteredItemSet.append(item) # A list is created and all the satified items are appended
            fin.seek(0)
            text_file.write("\n\n")

            # Recursion call with filtered items
            BUC(filteredItemSet,2) # sending only items which are satisfied in filteredItemSet(Apriori Property)
            # Recursion call with filtered items

        elif dimension == 2:
            for r in csv.DictReader(fin, delimiter=','):
                locationSet.add(r["Location"])
            text_file.write("\n(Item, Location) Cuboid:\n\n")
            tempSet = inventorySet.difference(inputList)
            text_file.write("-" * (len(regionSet) * 14 + 20)) # Dynamically writing dash ("-") according to length
            text_file.write("\n")
            text_file.write("{0}{1}".format(" " * len(regionSet) * 10,"Location"))
            text_file.write("\n")
            text_file.write("{0:20}".format(""))
            text_file.write("-"*len(regionSet)*14)
            text_file.write("\n")
            text_file.write("{0:20}".format("Item"))
            for area in regionSet:
                text_file.write("{0:15}".format(area))
            text_file.write("{0}{1}{2}".format("\n", "-" * (len(regionSet) * 14 + 20), "\n"))
            fin.seek(0)
            for item in inputList:
                fin.seek(0)
                text_file.write("{0:9}".format(item))

                for region in locationSet:
                    fin.seek(0)
                    total = sum(int(r["Sales_Units"]) for r in csv.DictReader(fin, delimiter=',') if r["Item"] == item and r["Location"] == region)
                    if total >= int(min_sup):

                        # Dictionary object is created to preserve the item and location relation
                        item_location = {"item": "",
                                         "location": ""}

                        text_file.write("{0:15}".format(total))
                        item_location["item"] = item
                        item_location["location"] = region
                        filteredItemLocationSet.append(item_location) # new Dictionary, which satisfies the condition is appended into list
                    else:
                        text_file.write("{0:15}".format(" "))
                text_file.write("\n")
            for x in tempSet:
                text_file.write("{0:9}{1}".format(x, "\n"))
            text_file.write("\n\n")

            # Recursion call with List of Dictionary(contains items and locations)
            BUC(filteredItemLocationSet, 3) # sending only items which are satisfied in filteredItemLocationSet(Apriori Property)
            # Recursion call with List of Dictionary(contains items and locations)

        elif dimension == 3:
            for r in csv.DictReader(fin, delimiter=','):
                yearSet.add(r["Year"])
            text_file.write("\n(Item, Location, Year) Cuboids:\n\n")
            fin.seek(0)
            for product in inputList:
                productSet.add(product["item"])
                locSet.add(product["location"])
            tempSet = inventorySet.difference(productSet)
            for year in yearSet:
                text_file.write("-" * (len(regionSet) * 14 + 20))
                text_file.write("\n")
                text_file.write("{0}{1} = {2}{3}".format(" " * len(regionSet) * 7, "Year", year,"\n"))
                text_file.write("-" * (len(regionSet) * 14 + 20))
                text_file.write("\n")
                text_file.write("{0}{1}".format(" " * len(regionSet) * 10, "Location"))
                text_file.write("\n")
                text_file.write("{0:20}".format(""))
                text_file.write("-" * len(regionSet) * 14)
                text_file.write("\n")
                text_file.write("{0:20}".format("Item"))
                for area in regionSet:
                    text_file.write("{0:15}".format(area))
                text_file.write("{0}{1}{2}".format("\n", "-" * (len(regionSet) * 14 + 20), "\n"))
                fin.seek(0)
                for item in productSet:
                    fin.seek(0)
                    text_file.write("{0:9}".format(item))

                    for region in locSet:
                        fin.seek(0)
                        total = sum(int(r["Sales_Units"]) for r in csv.DictReader(fin, delimiter=',') if
                                    r["Item"] == item and r["Location"] == region and
                                    r["Year"] == year)
                        if total >= int(min_sup):
                            text_file.write("{0:15}".format(total))
                        else:
                            text_file.write("{0:15}".format(" "))
                    text_file.write("\n")
                for x in tempSet:
                    text_file.write("{0:9}{1}".format(x, "\n"))
                text_file.write("\n\n\n")


BUC(inputList,1)
print("Iceberg-Cube-Results.txt file is created.")
print("Data in Iceberg-Cube-Results file satifies minimum support of {}.".format(min_sup))



