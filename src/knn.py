import math
import os
from csv import reader
from freeman import freeman
from pixel_count import pixels_on_row_sample


# nearest neighbours algorithm
# selects k smallest euclidean distances between the train set and the sample
# returns the most frequent one in the k samples
def nearest_neighbours(train_set, sample, k, pixel_count):
    pixel_count_switch = pixel_count

    if pixel_count_switch:
        # print("Vytvarim pro vzorek Pixel count")
        test_sample = pixels_on_row_sample(sample)
    else:
        test_sample = freeman(0, None, sample, True)
        # print("Vytvarim pro vzorek Freemanuv kod")

    neighbours = []
    distances = []
    for row in train_set:
        temp = row[1]
        temp = temp[1: len(temp) - 1]
        temp1 = list(map(int, temp.split(", ")))
        if pixel_count_switch:
            distances.append((row[0], calculate_euclidean_default(temp1, test_sample)))
        else:
            distances.append((row[0], calculate_euclidean_freeman(temp1, test_sample)))

    distances.sort(key=lambda x: x[1])

    for i in range(k):
        neighbours.append(distances[i])

    estimate = []
    for item in neighbours:
        estimate.append(item[0])

    estimated_num = most_frequent(estimate)

    return estimated_num


# euclidean distance for the freeman algorithm
# creates equally long samples and calculates the euclidean distance
# returns euclidean distance
def calculate_euclidean_freeman(sample1, sample2):
    temp1 = list(sample1)
    temp2 = list(sample2)

    distance = 0.0
    temp = max(len(temp1), len(temp2))
    if temp == len(temp1):
        for sample in range(0, temp - len(temp2)):
            temp2.append(0)
    else:
        for sample in range(0, temp - len(temp1)):
            temp1.append(0)

    for mm in range(len(temp1) - 1):
        distance += (temp1[mm] - temp2[mm]) ** 2
    return math.sqrt(distance)


# calculates the euclidean distance
# returns euclidean distance
def calculate_euclidean_default(sample1, sample2):
    distance = 0.0
    for ii in range(len(sample1) - 1):
        distance += (sample1[ii] - sample2[ii]) ** 2

    return math.sqrt(distance)


# opening the filepath file
# returns csv_reader
def open_file(filepath):
    file1 = open(filepath, 'r')
    csv_reader = reader(file1)

    return csv_reader


# loads the test set folder for the num number
# starts the nearest neighbours algorithm depending on what the selected algorithm is
# returns rounded number guess success percentage
def load_num_folders(num, writer, test_set, model, k):
    dir_path = test_set + "\\" + str(num) + "\\"
    test_sample_count = len(os.listdir(dir_path))
    successfully_guessed = 0

    for filename in os.listdir(dir_path):
        pixel_count_switch = False

        model_file = open_file(model)
        first_line = next(model_file)

        if "pixel" in first_line[1]:
            pixel_count_switch = True
        number = nearest_neighbours(model_file, dir_path + filename, k, pixel_count_switch)
        if int(number) == num:
            successfully_guessed += 1

    rounded = (successfully_guessed / test_sample_count) * 100
    rounded = round(rounded, 2)
    print("uspesnost odhadu pro cislo " + str(num) + " je: " + str(rounded) + "%")
    writer.writerow([str(num), str(rounded)])

    return rounded


# returns the most frequent item in the list
def most_frequent(List):
    return max(set(List), key=List.count)
