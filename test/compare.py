#!/usr/bin/env python3

from sys import argv

if len(argv) < 2: raise Exception("Expecting name of results file as an argument")

correctResults= [
'1,head,1,5,0.000000',
'2,head,1,5,3420.009862',
'3,head,1,4,3420.498875',
'4,back,1,5,0.000000',
'5,back,1,4,0.000000',
'6,back,1,3,0.000000',
'7,Markham,1,1,13709.506679'
]

actualResults = []
for r in open(argv[1]): actualResults.append(r)

for i in range(len(correctResults)):
    if correctResults[i] not in actualResults[i]:
        print(correctResults[i])
        print(actualResults[i])
        exit(1)
exit(0)