from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from Twitter import GetOnlineTweets
from Twitter import NormalizeDataSet
from Twitter import PredictClassification
from Twitter import TrainMultinomialNB
from Twitter import TrainSVM

rawFilePath = 'DataSet/Raw/'
normalizedFilePath = 'DataSet/Normalized/'
NBClassifierFileName = 'NB.pkl'
SVMClassifierFileName = 'SVM.pkl'
rawUserFilePath = 'DataSet/User/Raw/'
normalizedUserFilePath = 'DataSet/User/Normalized/'


def index(request):
    context = {
        'title': 'Dashboard',
        'labelCount': 0,
    }
    return render(request, 'Twitter/index.html', context)


def getTrainingData(request):
    context = {
        'title': 'Get Training Data'
    }
    return render(request, 'Twitter/getTrainingData.html', context)


def handle_uploaded_file(path, files):
    for file in files:
        with open(path + str(file), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)


def uploadDataSet(request):
    files = request.FILES.getlist('dataSetFiles')
    handle_uploaded_file(rawFilePath, files)
    return HttpResponseRedirect('/twitter/normalizeData')


def normalizeData(request):
    context = {
        'title': 'Normalize Data Set'
    }
    return render(request, 'Twitter/normalizeData.html', context)


def normalizeDataSet(request):
    #print("balllllllle"+request.POST)
    NormalizeDataSet.normalizeJSONData(rawFilePath, normalizedFilePath, request.POST)
    return HttpResponseRedirect('/twitter/trainClassifier')


def reduceData(request):
    return HttpResponse("This is reduce data url")


def trainClassifier(request):
    context = {
        'title': 'Train Classifier'
    }
    return render(request, 'Twitter/trainClassifier.html', context)


def trainNB(request):
    accuracy = TrainMultinomialNB.trainNB(normalizedFilePath, NBClassifierFileName)
    context = {
        'title': 'Train Classifier',
        'accuracy': accuracy
    }
    return render(request, 'Twitter/trainClassifier.html', context)


def trainSVM(request):
    accuracy = TrainSVM.trainSVM(normalizedFilePath, SVMClassifierFileName)
    context = {
        'title': 'Train Classifier',
        'accuracy': accuracy
    }
    return render(request, 'Twitter/trainClassifier.html', context)


def trainMultinomialNBClassifier(request):
    return HttpResponse("This is train multinomialNB classifier")


def trainSVMClassifier(request):
    return HttpResponse("This is train SVM Classifier")


def getTestData(request):
    context = {
        'title': 'Get User Data'
    }
    return render(request, 'Twitter/getTestData.html', context)


def getUserData(request):
    print(request.POST['username'])
    count = GetOnlineTweets.getUserTweets(rawUserFilePath, 'temp.json', request.POST['username'], '', 100)
    return HttpResponseRedirect('/twitter/normalizeUserData')


def normalizeUserData(request):
    context = {
        'title': 'Normalize Data Set',
        'UserData': 1,
    }
    return render(request, 'Twitter/normalizeUserData.html', context)


def normalizeUserDataSet(request):
    NormalizeDataSet.normalizeJSONData(rawUserFilePath, normalizedUserFilePath, request.POST)
    return HttpResponseRedirect('/twitter/predictInterest')


def predictInterest(request):
    context = {
        'title': 'Predict Interest'
    }
    return render(request, 'Twitter/predictInterest.html', context)


def predictNB(request):
    label = PredictClassification.predict(normalizedUserFilePath, 'NB.pkl')
    context = {
        'title': 'Predict Interest',
        'predictedLabel': label,
    }
    return render(request, 'Twitter/predictedAnswer.html', context)


def predictSVM(request):
    label = PredictClassification.predict(normalizedUserFilePath, 'SVM.pkl')
    context = {
        'title': 'Predict Interest',
        'predictedLabel': label,
    }
    return render(request, 'Twitter/predictedAnswer.html', context)
