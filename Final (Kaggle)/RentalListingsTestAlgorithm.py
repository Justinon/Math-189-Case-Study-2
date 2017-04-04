#!/usr/bin/env python

"""RentailListingsTestAlgorithm.py: Outputs to a csv file the generated probabilities of a test dataset."""

import pandas as pd
from scipy import stats

#############################
__author__ = "Justin Glommen"
__date__ = "4/2/17"
#############################

trainData = pd.read_json("train.json")
testData = pd.read_json("test.json")

# Initialize empty dictionaries
probabilityDataFrame = {'low': {}, 'medium': {}, 'high': {}, 'listing_id': {},}
# Variables for dataframes
trainLowInterestDistribution = {}
trainMedInterestDistribution = {}
trainHighInterestDistribution = {}

# Sample distributions to insert into dataframes
trainLowInterestNumFeatureList = {}
trainMedInterestNumFeatureList = {}
trainHighInterestNumFeatureList = {}
trainLowInterestNumPhotosList = {}
trainMedInterestNumPhotosList = {}
trainHighInterestNumPhotosList = {}
trainLowInterestNumBedroomsList = {}
trainMedInterestNumBedroomsList = {}
trainHighInterestNumBedroomsList = {}
trainLowInterestListingIdList = {}
trainMedInterestListingIdList = {}
trainHighInterestListingIdList = {}
trainLowInterestPriceList = {}
trainMedInterestPriceList = {}
trainHighInterestPriceList = {}

# Test features to analyze
testNumFeatureList = {}
testNumPhotosList = {}
testNumBedroomsList = {}
testListingIdList = {}
testPriceList = {}


## Create the sample distribution of different interest_level rental prices
# Create the list of index to prices and number of features
for index,row in trainData.iterrows():
    interestLevel = row['interest_level']
    if interestLevel == 'low':
        trainLowInterestPriceList[index] = row['price']
        trainLowInterestNumFeatureList[index] = len(row['features'])
        trainLowInterestNumPhotosList[index] = len(row['photos'])
        trainLowInterestListingIdList[index] = row['listing_id']
        trainLowInterestNumBedroomsList[index] = row['bedrooms']
    elif interestLevel == 'medium':
        trainMedInterestPriceList[index] = row['price']
        trainMedInterestNumFeatureList[index] = len(row['features'])
        trainMedInterestNumPhotosList[index] = len(row['photos'])
        trainMedInterestListingIdList[index] = row['listing_id']
        trainMedInterestNumBedroomsList[index] = row['bedrooms']
    elif interestLevel == 'high':
        trainHighInterestPriceList[index] = row['price']
        trainHighInterestNumFeatureList[index] = len(row['features'])
        trainHighInterestNumPhotosList[index] = len(row['photos'])
        trainHighInterestListingIdList[index] = row['listing_id']
        trainHighInterestNumBedroomsList[index] = row['bedrooms']

# Convert dictionaries to Series
trainMedInterestPriceList = pd.Series(trainMedInterestPriceList)
trainLowInterestPriceList = pd.Series(trainLowInterestPriceList)
trainHighInterestPriceList = pd.Series(trainHighInterestPriceList)
trainLowInterestNumPhotosList = pd.Series(trainLowInterestNumPhotosList)
trainMedInterestNumPhotosList = pd.Series(trainMedInterestNumPhotosList)
trainHighInterestNumPhotosList = pd.Series(trainHighInterestNumPhotosList)
trainLowInterestNumBedroomsList = pd.Series(trainLowInterestNumBedroomsList)
trainMedInterestNumBedroomsList = pd.Series(trainMedInterestNumBedroomsList)
trainHighInterestNumBedroomsList = pd.Series(trainHighInterestNumBedroomsList)
trainLowInterestNumFeatureList = pd.Series(trainLowInterestNumFeatureList)
trainMedInterestNumFeatureList = pd.Series(trainMedInterestNumFeatureList)
trainHighInterestNumFeatureList = pd.Series(trainHighInterestNumFeatureList)
trainLowInterestListingIdList = pd.Series(trainLowInterestListingIdList)
trainMedInterestListingIdList = pd.Series(trainMedInterestListingIdList)
trainHighInterestListingIdList = pd.Series(trainHighInterestListingIdList)

# Do the same process on the testSet; congregate useable data
for index,row in testData.iterrows():
    testPriceList[index] = row['price']
    testNumFeatureList[index] = len(row['features'])
    testNumPhotosList[index] = len(row['photos'])
    testListingIdList[index] = row['listing_id']
    testNumBedroomsList[index] = row['bedrooms']

testPriceList = pd.Series(testPriceList)
testNumPhotosList = pd.Series(testNumPhotosList)
testNumBedroomsList = pd.Series(testNumBedroomsList)
testNumFeatureList = pd.Series(testNumFeatureList)
testListingIdList = pd.Series(testListingIdList)

# Create the dataframes of interest_level distributions of prices
# We will use these distributions to generate the pValues
d = {
    'price': trainLowInterestPriceList,
    'photos': trainLowInterestNumPhotosList,
    'features': trainLowInterestNumFeatureList,
    'listing_id': trainLowInterestListingIdList,
    'bedrooms': trainLowInterestNumBedroomsList,
}
trainLowInterestDistribution = pd.DataFrame(d)
d = {
    'price': trainMedInterestPriceList,
    'photos': trainMedInterestNumPhotosList,
    'features': trainMedInterestNumFeatureList,
    'listing_id': trainMedInterestListingIdList,
    'bedrooms': trainMedInterestNumBedroomsList,
}
trainMedInterestDistribution = pd.DataFrame(d)
d = {
    'price': trainHighInterestPriceList,
    'photos': trainHighInterestNumPhotosList,
    'features': trainHighInterestNumFeatureList,
    'listing_id': trainHighInterestListingIdList,
    'bedrooms': trainHighInterestNumBedroomsList,
}
trainHighInterestDistribution = pd.DataFrame(d)

# Here's the actual dataset to analyze
d = {
    'price': testPriceList,
    'photos': testNumPhotosList,
    'features': testNumFeatureList,
    'listing_id': testListingIdList,
    'bedrooms': testNumBedroomsList,
}
testDistribution = pd.DataFrame(d)

# Demonstration of what was done above
print("Low Interest Rentals:\n", trainLowInterestDistribution.head())
print("Medium Interest Rentals:\n", trainMedInterestDistribution.head())
print("High Interest Rentals:\n", trainHighInterestDistribution.head())
print("Test Distribution:\n", testDistribution.head())


# Now, we generate pValues by calling stats.percentileofscore and doing a two-tailed result
# Then we store the pValues into the pValue dictionaries we just created
for index, row in testDistribution.iterrows():
    pValCounter = 0
    pValLowSum = 0
    pValMedSum = 0
    pValHighSum = 0
    for column, items in testDistribution.iteritems():
        if column == 'listing_id':
            continue
        pValCounter += 1
        pValLow = 0
        pValMed = 0
        pValHigh = 0
        percentileLow = stats.percentileofscore(trainLowInterestDistribution[column], row[column])
        percentileMed = stats.percentileofscore(trainMedInterestDistribution[column], row[column])
        percentileHigh = stats.percentileofscore(trainHighInterestDistribution[column], row[column])

        # This step is finding the pValue using the quantile of the distribution
        if percentileLow <= 50:
            pValLow = (percentileLow*2)/100
        elif percentileLow > 50:
            pValLow = ((100 - percentileLow)*2)/100

        if percentileMed <= 50:
            pValMed = (percentileMed*2)/100
        elif percentileMed > 50:
            pValMed = ((100 - percentileMed)*2)/100

        if percentileHigh <= 50:
            pValHigh = (percentileHigh*2)/100
        elif percentileHigh > 50:
            pValHigh = ((100 - percentileHigh)*2)/100

        # If price pVal is super high, then reflect that in probabilities generated
        # Typically high priced houses have low-medium interest
        if column == 'price':
            if pValLow <= .05 or pValMed <= .05 or pValHigh <= .05:
                pValLow = .999999
                pValMed = .25
                pValHigh = .05

        # Does not include any insignificant pValues in the probability generation.
        # If the difference between the maximum and minimum pValues is less than 20%,
        # then the difference is not significant.
        maxPVal = max([pValLow, pValMed, pValHigh])
        minPVal = min([pValLow, pValMed, pValHigh])
        if maxPVal - minPVal <= .2:
            pValCounter -= 1
            continue

        # Algorithm for probabilities of interest takes the average of the pValues as a sort of hypothesis test
        pValLowSum += pValLow
        pValMedSum += pValMed
        pValHighSum += pValHigh

    # If all pValues were too similar, then we say they have equal probability
    if pValCounter == 0:
        pValLowAverage = .33
        pValMedAverage = .33
        pValHighAverage = .33
    else:
        # The average for each category pValue is taken, and then all are normalized to sum to one
        pValLowAverage = pValLowSum / pValCounter
        pValMedAverage = pValMedSum /pValCounter
        pValHighAverage = pValHighSum / pValCounter

    pValSum = pValLowAverage + pValMedAverage + pValHighAverage

    # Forming the final probabilities based on the pValues
    lowProbability = pValLowAverage/pValSum
    medProbability = pValMedAverage/pValSum
    highProbability = pValHighAverage/pValSum

    probabilityDataFrame['low'][index] = lowProbability
    probabilityDataFrame['medium'][index] = medProbability
    probabilityDataFrame['high'][index] = highProbability
    probabilityDataFrame['listing_id'][index] = row['listing_id']

probabilityDataFrame = pd.DataFrame(probabilityDataFrame)

# Arrange order of columns for CSV file
cols = probabilityDataFrame.columns.tolist()
reorderedCols =[1,0,3,2]
cols = [cols[i] for i in reorderedCols]
probabilityDataFrame = probabilityDataFrame[cols]
probabilityDataFrame.to_csv("testProbabilities.csv", index=False)

print("Probabilities:\n", probabilityDataFrame.head())