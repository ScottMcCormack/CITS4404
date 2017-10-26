import os

files = {}
os.chdir('..')
print( os.getcwd() )

s = "A_0"

for i in range(1,80):
    s += "\tA_" + str(i)
s += "\tClass\n"

j = 0

with open('data_3_formatted.txt', 'w') as dataFile_1:
    dataFile_1.write(s)

    with open('data_3_formatted_test.txt', 'w') as dataFile_test:
        dataFile_test.write(s)

        with open('data_2.txt', 'r') as dataFile:

            for line in dataFile:
                print(line)
                a = line.split('\t')
                print( len(a) )
                if len(a) == 81:
                    if j%4 == 0:
                        dataFile_test.write(line)
                        j += 1
                    else:
                        dataFile_1.write(line)
                        j += 1
