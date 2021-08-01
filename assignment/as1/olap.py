import csv


columns = ['Country', 'Time_Year', 'Time_Quarter', 'Car_Manufacturer', 'Sales_Units']

def CarSalesDataSetFirstSorting():
    carSalesData = open('Car_Sales_Data_Set.csv', encoding='utf-8-sig')
    csv_reader = csv.DictReader(carSalesData, delimiter=',')
    sortedlist = sorted(csv_reader, key=lambda row: row['Country'])
    WriteToCSV("Car_Sales_Data_Set_First_Sorting.csv", sortedlist)


def CarSalesDataSetSecondSorting():
    carSalesDataSort1 = open('Car_Sales_Data_Set_First_Sorting.csv')
    csv_reader = csv.DictReader(carSalesDataSort1, delimiter=',')
    sortedlist = sorted(csv_reader, key=lambda row: (row['Country'], row['Time_Year']))
    WriteToCSV("Car_Sales_Data_Set_Second_Sorting.csv", sortedlist)

def CarSalesDataSetThirdSorting():
    carSalesDataSort1 = open('Car_Sales_Data_Set_Second_Sorting.csv')
    csv_reader = csv.DictReader(carSalesDataSort1, delimiter=',')
    sortedlist = sorted(csv_reader, key=lambda row: (row['Country'], row['Time_Year'], row['Time_Quarter']))
    WriteToCSV("Car_Sales_Data_Set_Third_Sorting.csv", sortedlist)


def WriteToCSV(fileName, SortedList):
    csvfile = open(fileName, 'w', newline='')
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()
    writer.writerows(SortedList)

def ReadInput():
    print("List of OLAP Queries to obtain aggregated sales units")
    print("1  : Total Overall Sales ")
    print("2  : Country wise Overall Sales    (Country)")
    print("3  : Year wise sales  (Time_Year)")
    print("4  : Sales in particular year and Quarter     (Time_Quarter -Time_Year)")
    print("5  : Sales by Manufacturer    (Car_Manufacturer) ")
    print("6  : Sales in Country and Year    (Country, Time_Year)")
    print("7  : Sales in Country and  Quarter of Year    (Country, Time_Quarter -Time_Year)")
    print("8  : Sales of Car Manufacturer in Country     (Country, Car_Manufacturer)")
    print("9  : Sales of Car Manufacturer in a Year  (Time_Year, Car_ Manufacturer)")
    print("10 : Sales of Car Manufacturer in a Quarter of a Year  (Time_Quarter -Time_Year, Car_Manufacture)")
    print("11 : Sales of Car Manufacturer in a country in particular year    (Country, Time_Year, Car_Manufacturer)")
    print("12 : Sales of Car Manufacturer in a country in particular Quarter of year     (Country, Time_Quarter-Time_Year, Car_Manufacturer))")
    userInput = input("Enter a Value between 1 and 12 to perform respective OLAP Query")
    InputProcessing(userInput)


def InputProcessing(userInput):
    with open("Car_Sales_Data_Set_Third_Sorting.csv", "r+") as fin:
        countrySet, yearSet, quarterSet, manufacturerSet = set(),set(),set(),set()
        for r in csv.DictReader(fin, delimiter=','):
            countrySet.add(r["Country"])
            yearSet.add(r["Time_Year"])
            quarterSet.add(r["Time_Quarter"])
            manufacturerSet.add(r["Car_Manufacturer"])
        countrySet = sorted(countrySet)
        yearSet = sorted(yearSet)
        quarterSet = sorted(quarterSet)
        manufacturerSet = sorted(manufacturerSet)
        fin.seek(0)
        if userInput == '1':
            total = sum(int(r["Sales_Units"]) for r in csv.DictReader(fin, delimiter=','))
            print()
            print("Overall Sales in both countries in both years\n")
            print("Sales_Units")
            print("------------")
            print("{0:2}{1}".format("",total))

        elif userInput == '2':
            print()
            print("The Overall Sales in a particular Country\t(Country)\n")
            print("{0:23}{1}".format("Country", "Sales_Units"))
            print("----------------------------------")
            for region in countrySet:
                fin.seek(0)
                Total = sum(int(r["Sales_Units"]) for r in csv.DictReader(fin, delimiter=',') if r["Country"] == region)
                print('{0:25}{1}'.format(region,Total))


        elif userInput == '3':
            print()
            print("The Overall Sales in a particular year\t(Time_Year)\n")
            print("{0:23}{1}".format("Time_Year","Sales_Units"))
            print("----------------------------------")
            for year in yearSet:
                fin.seek(0)
                Total = sum(int(r["Sales_Units"]) for r in csv.DictReader(fin, delimiter=',') if r["Time_Year"] == year)
                print("{0:2}{1:23}{2}".format("", year,Total))


        elif userInput == '4':
            print()
            print("The Sales in particular Quarter of a year\t(Time_Quarter -Time_Year)\n")
            print("{0:33}{1}".format("Time_Quarter-Time_Year","Sales_Units"))
            print("--------------------------------------------")
            for year in yearSet:
                fin.seek(0)
                for quarter in quarterSet:
                    fin.seek(0)
                    Total = sum(int(r["Sales_Units"]) for r in csv.DictReader(fin, delimiter=',') if (r["Time_Year"] == year) and (r["Time_Quarter"] == quarter))
                    print("{0:7}{1}-{2:28}{3}".format("",quarter, year, Total))


        elif userInput == '5':
            print()
            print("The Overall Sales of Particular Manufacturer\t(Car_ Manufacturer)\n")
            print("{0:25}{1}".format("Car_Manufacturer","Sales_Units"))
            print("------------------------------------")
            for car in manufacturerSet:
                fin.seek(0)
                Total = sum(int(r["Sales_Units"]) for r in csv.DictReader(fin, delimiter=',') if r["Car_Manufacturer"] == car)
                print("{0:5}{1:24}{2}".format("",car,Total))


        elif userInput == '6':
            print()
            print("The Sales of a Country in particular year\t(Country, Time_Year)\n")
            print("{0:25}{1:22}{2}".format("Country","Time_Year","Sales_Units"))
            print("-----------------------------------------------------------")
            for country in countrySet:
                fin.seek(0)
                for year in yearSet:
                    fin.seek(0)
                    Total = sum(int(r["Sales_Units"]) for r in csv.DictReader(fin, delimiter=',') if (r["Country"] == country) and (r["Time_Year"] == year))
                    print("{0:27}{1:23}{2}".format(country, year, Total))

        elif userInput == '7':
            print()
            print("The Sales of a Country in particular Quarter of a year\t(Country, Time_Quarter -Time_Year)\n")
            print("{0:23}{1:28}{2}".format("Country","Time_Quarter-Time_Year","Sales_Units"))
            print("------------------------------------------------------------------")
            for country in countrySet:
                fin.seek(0)
                for year in yearSet:
                    fin.seek(0)
                    for quarter in quarterSet:
                        fin.seek(0)
                        Total = sum(int(r["Sales_Units"]) for r in csv.DictReader(fin, delimiter=',') if (r["Country"] == country) and (r["Time_Year"] == year) and (r["Time_Quarter"] == quarter))
                        print("{0:30}{1}-{2:23}{3}".format(country, quarter, year,  Total))


        elif userInput == '8':
            print()
            print("The Sales of Car Manufacturer in a country\t(Country, Car_Manufacturer)\n")
            print("{0:21}{1:25}{2}".format("Country","Car_Manufacturer","Sales_Units"))
            print("-------------------------------------------------------------")
            for country in countrySet:
                fin.seek(0)
                for car in manufacturerSet:
                    fin.seek(0)
                    Total = sum(int(r["Sales_Units"]) for r in csv.DictReader(fin, delimiter=',') if (r["Country"] == country) and (r["Car_Manufacturer"] == car))
                    print("{0:27}{1:23}{2}".format(country, car, Total))



        elif userInput == '9':
            print()
            print("The Sales of Car Manufacturer in a year\t(Time_Year, Car_ Manufacturer)\n")
            print("{0:20}{1:27}{2}".format("Time_Year","Car_Manufacturer","Sales_Units"))
            print("-----------------------------------------------------------")
            for year in yearSet:
                fin.seek(0)
                for car in manufacturerSet:
                    fin.seek(0)
                    Total = sum(int(r["Sales_Units"]) for r in csv.DictReader(fin, delimiter=',') if (r["Time_Year"] == year) and (r["Car_Manufacturer"] == car))
                    print("{0:2}{1:25}{2:24}{3}".format("",year, car, Total))


        elif userInput == '10':
            print()
            print("The Sales of a Car Manufacuturer in particular Quarter of a year\t(Time_Quarter -Time_Year, Car_ Manufacture)\n")
            print("{0:30}{1:27}{2}".format("Time_Quarter-Time_Year", "Car_Manufacturer", "Sales_Units"))
            print("---------------------------------------------------------------------")
            for year in yearSet:
                fin.seek(0)
                for quarter in quarterSet:
                    fin.seek(0)
                    for car in manufacturerSet:
                        fin.seek(0)
                        Total = sum(int(r["Sales_Units"]) for r in csv.DictReader(fin, delimiter=',') if (r["Time_Year"] == year) and (r["Time_Quarter"] == quarter) and (r["Car_Manufacturer"] == car))
                        print("{0:7}{1}-{2:28}{3:23}{4}".format("",quarter, year, car, Total))


        elif userInput == '11':
            print()
            print("The Sales of a Car Manufacuturer in particular year for each country\t(Country, Time_Year, Car_ Manufacturer)\n")
            print()
            for country in countrySet:
                print("{0:20}{1} = {2}".format("","Country",country))
                print("----------------------------------------------------------------------")
                print("{0:30}{1:27}{2}".format("Time_Quarter-Time_Year", "Car_Manufacturer", "Sales_Units" ))
                print("----------------------------------------------------------------------")
                fin.seek(0)
                for year in yearSet:
                    fin.seek(0)
                    for car in manufacturerSet:
                        fin.seek(0)
                        Total = sum(int(r["Sales_Units"]) for r in csv.DictReader(fin, delimiter=',') if
                                    (r["Country"] == country) and (r["Time_Year"] == year) and (
                                                r["Car_Manufacturer"] == car))
                        print("{0:7}{1:29}{2:26}{3}".format("", year, car, Total))

                print()
                print()


        elif userInput == '12':
            print()
            print("The Sales of a Car Manufacuturer in particular Quarter of a year for each country\t(Country, Time_Quarter-Time_Year, Car_ Manufacturer)\n")
            print()
            for country in countrySet:
                print("{0:23}{1} = {2}".format("", "Country", country))
                print("-----------------------------------------------------------------")
                print("{0:28}{1:20}{2}".format("Time_Quarter-Time_Year", "Quarter", "Car_Manufacturer", "Sales_Units"))
                print("-----------------------------------------------------------------")
                fin.seek(0)
                for year in yearSet:
                    fin.seek(0)
                    for quarter in quarterSet:
                        fin.seek(0)
                        for car in manufacturerSet:
                            fin.seek(0)
                            Total = sum(int(r["Sales_Units"]) for r in csv.DictReader(fin, delimiter=',') if
                                      (r["Country"] == country) and (r["Time_Year"] == year) and (
                                                r["Time_Quarter"] == quarter) and (r["Car_Manufacturer"] == car))
                            print("{0:7}{1}-{2:18}{3:25}{4}".format("", year, quarter, car, Total))

                print()
                print()



CarSalesDataSetFirstSorting()
print("...First Sorting Done, New File Created with name Car_Sales_Data_Set_First_Sorting.csv............\n")
CarSalesDataSetSecondSorting()
print("...Second Sorting Done, New File Created with name Car_Sales_Data_Set_Second_Sorting.csv............\n")
CarSalesDataSetThirdSorting()
print("...Third Sorting Done, New File Created with name Car_Sales_Data_Set_Third_Sorting.csv............\n")
print()
ReadInput()

