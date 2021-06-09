import csv
import os
import sys
from _csv import reader

import gui as GUI
from pixel_count import pixels_on_row
from freeman import freeman
from knn import load_num_folders


# Checks if the train set and test set folder exists
# Launches training and classification when it does
def check_files(train_set, test_set, parameter_algo, classifier_algo, model_name):
    if os.path.exists(train_set):
        if os.path.exists(test_set):
            print("Spoustim parametrizacni algoritmus " + parameter_algo)
            file = open(model_name + '.csv', 'w', newline='')
            writer = csv.writer(file)
            if parameter_algo == "pixel_count":
                writer.writerow(["number", "pixel code"])
            if parameter_algo == "freeman":
                writer.writerow(["number", "freeman code"])

            for i in range(10):
                train(i, writer, train_set, parameter_algo)

            print(model_name + ".csv byl vytvoren")
            classify(parameter_algo, classifier_algo, test_set, model_name)

    else:
        print("Nespravna cesta k testovaci nebo trenovaci mnozine")
        sys.exit(-1)


# Launches the parameter parametrization algorithm
def train(num, writer, train_set, parameter):
    dir_path = train_set + "\\" + str(num) + "\\"
    print("Ukladam kody pro cislo " + str(num))
    for filename in os.listdir(dir_path):
        if parameter == "freeman":
            freeman(num, writer, dir_path + filename, False)
        if parameter == "pixel_count":
            pixels_on_row(num, writer, dir_path + filename)


# Displays the classification success percentage
# If the file does not exist it starts the classification
def classify(parameter, classifier, test_set, model):
    if os.path.isfile(parameter + "_" + classifier + "_percentage.csv"):
        print("Soubor s uspesnosti klasifikace " + classifier + " parametrizacniho algoritmu " + parameter + " jiz "
                                                                                                             "existuje, zobrazuji vysledky")
        file1 = open(parameter + "_" + classifier + "_percentage.csv", 'r')
        csv_reader = reader(file1)

        for row in csv_reader:
            print(row)

    else:
        print("Vysledky uspesnosti klasifikace nenalezeny, klasifikuji")
        print("Operace muze trvat velmi dlouho")
        file = open(parameter + "_" + classifier + "_percentage.csv", 'w', newline='')
        writer = csv.writer(file)
        writer.writerow(["cislo", "procento uspesnosti odhadu"])
        success_percentage = 0

        if classifier == "knn":
            print("Klasifikace pomoci algoritmu " + classifier + " s k = " + 5)
            for g in range(0, 10):
                print("Klasifikace mnoziny cisla " + str(g))
                success_percentage += load_num_folders(g, writer, test_set, model + ".csv", 5)

        if classifier == "minimal_distance":
            print("Klasifikace pomoci algoritmu " + classifier)
            for g in range(0, 10):
                print("Klasifikace mnoziny cisla " + str(g))
                success_percentage += load_num_folders(g, writer, test_set, model + ".csv", 1)

        writer.writerow(["prumerne procento uspesnosti je " + str((success_percentage / 10)) + "%"])


# Extracts the command line arguments
def get_arguments():
    train_set = None
    test_set = None
    parameter_algo = None
    classifier_algo = None
    model_name = None

    if len(sys.argv) > 2:
        try:
            train_set = sys.argv[1]
            print(train_set)
            test_set = sys.argv[2]
            print(test_set)
            parameter_algo = sys.argv[3]
            print(parameter_algo)
            classifier_algo = sys.argv[4]
            print(classifier_algo)
            model_name = sys.argv[5]
            print(model_name)
        except:
            print("Prosím zadejte parametry ve tvaru")
            print("cesta_k_trenovaci_mnozine cesta_k_testovaci_mnozine parametrizacni klasifikacni nazev_modelu")
            print("Parametrizacni algoritmy: freeman nebo pixel_count")
            print("Klasifikacni algoritmy: knn nebo minimal_distance")

        if parameter_algo != "freeman":
            if parameter_algo != "pixel_count":
                print("Prosim zadejte validni parametrizacni algoritmus - freeman nebo pixel_count")
                sys.exit(-1)

        if classifier_algo != "knn":
            if classifier_algo != "minimal_distance":
                print("Prosim zadejte validni klasifikacni algoritmus - knn nebo minimal_distance")
                sys.exit(-1)

        check_files(train_set, test_set, parameter_algo, classifier_algo, model_name)

    else:
        try:
            model_name = sys.argv[1]
            print("Spoustim klasifikaci s GUI pro model: " + model_name)
        except:
            print("Prosím zadejte parametry ve tvaru")
            print("nazev_modelu")
            sys.exit(-1)

        GUI.create_gui(model_name)


# Starts the get_arguments function
if __name__ == '__main__':
    get_arguments()
