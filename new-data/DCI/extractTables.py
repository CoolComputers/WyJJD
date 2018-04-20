import re, os
toParse = raw_input("what file do you want parsed?")
year = raw_input("what is the file prepend?(year)")
#year = '2015'
#oParse = "./"+year+"/tabula-2015UCR-mini.csv"

if not os.path.isfile(toParse):
    print("file not found")
else:
    parseFile = open(toParse, "r")

    tableName=""
    dumpFile=""
    for line in parseFile:
        if re.match("^//", line):
            try:
                dumpFile.close()
            except Exception as e:
                print("close err")
            tableName=line[2:]
            print("found table name: "+tableName)
            dumpFile = open("./"+year+"/clean/"+year+"-"+tableName+".csv", "a+")
        else:
            dumpFile.write(line)
    dumpFile.close()
    parseFile.close()
