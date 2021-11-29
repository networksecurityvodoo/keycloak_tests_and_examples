import csv
import requests


#### Open CSV 
file = open("dbdump01.csv", "r")
csv_reader = csv.reader(file)

#### Put content of the CSV File into a List
list_from_CSV= []
for row in csv_reader:
    list_from_CSV.append(row)

##Debug: Examples for printing the Value of a specific Entry

#print ("Number of Entries:"+ str(len(list_from_CSV)))                   ## Print overall Number of Rows in CSV
#print (lists_from_CSV[0])                                              ## First Entry
#print(list_from_CSV[((len(list_from_CSV))-1)])                         ## Last Entry


#### Iterate over File 
for i in list_from_CSV:
    print(i)


