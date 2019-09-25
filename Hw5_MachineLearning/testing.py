import subprocess
import sys

#insert your files here
# algorithimsToTest = ["congress_nbc.py"]
algorithimsToTest = ["congress_nbc.py", "congress_dec.py"]
# nameOfTestingDataFile = "congress_test.csv"
# algorithimsToTest = ["congress_nbc.py", "congress_nbc_extra_credit.py" ,  "congress_dec.py", "congress_pc.py", "congress_apriori.py" ]
nameOfTestingDataFile = "strippedTraining.csv"

democrat = "Democrat"
republican = "Republican"
yea = "Yea"
nay = "Nay"

trainingPeopleParty = []
##file input
for line in open("congress_train.csv", 'r').read().split("\n"):
    if len(line) != 0:
        for vote in line.split(","):
            if vote == republican or vote == democrat:
                trainingPeopleParty.append(democrat if vote == democrat else republican)

for file in algorithimsToTest:
    cmd = ("python " + file + " congress_train.csv " + nameOfTestingDataFile)
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    count = 0
    index = 0
    for line in output.stdout:
        outputLine = str(line.strip())
        testingParty = outputLine[2:outputLine.index(',')]
        if testingParty == trainingPeopleParty[index]:
            count += 1
        index += 1
    print("%s num matches: %d\tPercent: %s" % (file,count, str(((100 * count) / (len(trainingPeopleParty))))))