import csv
import pprint
import heapq
import scipy.stats.stats
import matplotlib.pyplot
import numpy

matplotlib.pyplot.ioff()

bacteria_abundance = []
with open("OTU.csv", newline="") as csvfile:
    filereader = csv.reader(csvfile, delimiter=",")
    for row in filereader:
        bacteria_abundance.append(row)

count = 0
for row in bacteria_abundance:
    if count == 0:
        count += 1
        continue
    for num in range(1, len(row)):
        row[num] = int(row[num])

nutrition = []
with open("TimeSeries_Metadata.csv", newline="") as csvfile:
    filereader = csv.reader(csvfile, delimiter=",")
    for row in filereader:
        nutrition.append(row)

count = 0
for row in nutrition:
    if count == 0:
        count += 1
        continue
    for num in range(len(row)):
        try:
            row[num] = float(row[num])
        except ValueError:
            pass

gut_nutrition = []
saliva_nutrition = []
gut_samples = []
saliva_samples = []
gut_bacteria_abundance = []
saliva_bacteria_abundance = []

for value in range(len(nutrition)):
    if "gut" in nutrition[value][2]:
        gut_nutrition.append(nutrition[value])
    elif "oral" in nutrition[value][2]:
        saliva_nutrition.append(nutrition[value])

for x in gut_nutrition:
    gut_samples.append(x[0])
for x in saliva_nutrition:
    saliva_samples.append(x[0])

for sample in gut_samples:
    for x in bacteria_abundance:
        if x[0] == sample:
            gut_bacteria_abundance.append(x)
for sample in saliva_samples:
    for x in bacteria_abundance:
        if x[0] == sample:
            saliva_bacteria_abundance.append(x)

nutrition1 = []
for row in nutrition:
    if "<not provided>" not in row:
        nutrition1.append(row)
nutrition = nutrition1

corr_coefs_gut = []
for sample in gut_bacteria_abundance:
    five_highest_ab = heapq.nlargest(5, sample[1:])
    five_highest_nutr = heapq.nlargest(5, sample[4:])
    (corr, p) = scipy.stats.stats.pearsonr(five_highest_ab, five_highest_nutr)
    corr_coefs_gut.append(corr)

matplotlib.pyplot.scatter(numpy.arange(len(corr_coefs_gut)), corr_coefs_gut)
avg = matplotlib.pyplot.plot([numpy.mean(corr_coefs_gut)] * len(corr_coefs_gut))
matplotlib.pyplot.setp(avg, color="r", linewidth=2.0)
matplotlib.pyplot.ylim((-1, 1))
matplotlib.pyplot.xlim((0, len(corr_coefs_gut)))
matplotlib.pyplot.xlabel("Sample")
matplotlib.pyplot.ylabel("Correlation Coefficient")
matplotlib.pyplot.title("Correlation Factor between Top 5 Nutrient Abundance and\nTop 5 Bacteria Abundance in Gut Samples vs. Sample Number")
matplotlib.pyplot.show()

# print(sorted(bacteria_abundance[1][1:], reverse=True)[0:5])
# loc = bacteria_abundance[1].index(44702)
# print(loc)
# print(bacteria_abundance[loc][0])