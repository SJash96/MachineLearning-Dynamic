from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from functions import readCSV, readLiveCSV, writeLiveCSV, convertData, printMetatdata, splitXY_train, trainOnCLassifier, predictions, accuracyCalc
from os import system
from time import sleep
import atexit

def main():
    Proto_le = LabelEncoder()
    Label_le = LabelEncoder()
    data = readCSV()
    convtd_data = convertData(data, Proto_le, Label_le)
    printMetatdata(convtd_data)
    X_Train, Y_Train = splitXY_train(convtd_data)
    classifier = trainOnCLassifier(X_Train, Y_Train)
    
    while True:
        try:
            atexit.register(liveLoop, Proto_le, Label_le, classifier, Y_Train, True)
        except KeyboardInterrupt:
            print("Exiting Application")
        liveLoop(Proto_le, Label_le, classifier)

def liveLoop(Proto_le, Label_le, classifier, Y_Train = None, exiting = False):
    liveData = readLiveCSV()
    convtd_live_data = convertData(liveData, Proto_le)
    #printMetatdata(convtd_live_data)
    results, label_Keys = predictions(convtd_live_data, classifier, Proto_le, Label_le, exiting)
    if exiting:
        system('cls')
        #convtd_results = convertData(results, Proto_le, Label_le)
        #X_Test, Y_Test = splitXY_train(convtd_results)
        #accuracyCalc(Y_Test, Y_Train, label_Keys)
        writeLiveCSV(results)
    else:
        sleep(1)
        system('cls')


if __name__ == "__main__":
    main()