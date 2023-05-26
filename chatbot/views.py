from django.shortcuts import render,redirect
from django.http import HttpResponse
from chatbot.models import information, electricity, Jal_Jeevan_Mission, raised_questions
from django.contrib.auth import authenticate,login
import json
from django.http import JsonResponse
from django.contrib import messages

#ML Imports
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from nltk.corpus import wordnet as wn
from nltk.metrics import edit_distance
from django.views.decorators.csrf import csrf_exempt
import os
import matplotlib.pyplot as plt
from django.conf import settings
#################################################################################################
#                                        Classifier
#################################################################################################

# Define the categories
categories = ['information', 'electricity', 'Jal_Jeevan_Mission']

# Get categorical data
information_data = information.objects.all()
electricity_data = electricity.objects.all()
jal_jeevan = electricity.objects.all()
training_data = []
# Create training data
for i in jal_jeevan:
    training_data.append((i.que, "Jal_Jeevan_Mission"))

for i in electricity_data:
    training_data.append((i.que, "electricity"))

for i in information_data:
    training_data.append((i.que, "information"))

#print(training_data)

'''
# Define the training data
training_data = [
    ("This is an example sentence for category 1", "category1"),
    ("Another sentence for category 1", "category1"),
    ("A sentence belonging to category 2", "category2"),
    ("This sentence belongs to category 3", "category3"),
    # Add more training data as needed
]
'''
# Preprocessing the training data
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
    return " ".join(filtered_tokens)

preprocessed_data = [(preprocess_text(sentence), label) for sentence, label in training_data]

# Create a pipeline for text classification
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', SVC(kernel='linear'))
])

# Set up parameters for grid search
parameters = {
    'tfidf__max_features': (None, 5000, 10000),
    'tfidf__ngram_range': [(1, 1), (1, 2)],
    'clf__C': [1, 10, 100],
}

# Perform grid search with stratified k-fold cross-validation
skf = StratifiedKFold(n_splits=2, shuffle=True, random_state=42)
grid_search = GridSearchCV(pipeline, parameters, cv=skf)
grid_search.fit([sentence for sentence, _ in preprocessed_data], [label for _, label in preprocessed_data])

# Get the best model
best_model = grid_search.best_estimator_



# Classify multiple sentences
def classify_sentences(sentences):
    preprocessed_sentences = [preprocess_text(sentence) for sentence in sentences]
    predicted_categories = best_model.predict(preprocessed_sentences)
    return predicted_categories

# sentences_to_classify = ["My university is very bad what should I do?"]
# predicted_categories = classify_sentences(sentences_to_classify)
# category = None
# for sentence, category in zip(sentences_to_classify, predicted_categories):
#     print("Sentence:", sentence)
#     print("Predicted category:", category)
#     print()
'''
# Example usage
sentences_to_classify = ["This is a sentence to classify", "Another example sentence"]
predicted_categories = classify_sentences(sentences_to_classify)
for sentence, category in zip(sentences_to_classify, predicted_categories):
    print("Sentence:", sentence)
    print("Predicted category:", category)
    print()
'''
#################################################################################################


#################################################################################################
#                         Question finder
#################################################################################################


# define a function to preprocess text
def preprocess(text):
    text = "".join(text)
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens

# define a function to find synonyms of a word
def find_synonyms(word):
    synonyms = set()
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

# define a function to find the best match for a question
def find_best_match(question, sentences):
    question = preprocess(question)
    best_score = 0
    best_sentence = None
    for sentence in sentences:
        sentence = preprocess(sentence)
        score = 0
        for word in question:
            if word in sentence:
                score += 1
            elif len(find_synonyms(word)) > 0:
                synonyms = find_synonyms(word)
                for synonym in synonyms:
                    if synonym in sentence:
                        score += 0.5
        if score > best_score:
            best_score = score
            best_sentence = sentence
    return best_score

# define a function to answer a question
def answer_question(question, text):
    sentences = sent_tokenize(text)
    best_sentence = find_best_match(question, sentences)
    if best_sentence is None:
        return "I'm sorry, I don't know the answer."
    else:
        return best_sentence
    
# ans, score = None, 0
# final_answer = None
# if category == "information":
#     for i in information_data:
#         temp_ans, temp_score =  answer_question(sentences_to_classify, i.que)
#         if temp_score > score:
#             score = temp_score
#             ans = temp_ans
#             final_answer = i.ans
#     if score < len(sentences_to_classify)//4:
#         print("Sorry")

#     else:
#         print(final_answer)
'''
# example usage
text = "The quick brown fox jumps over the lazy dog. The dog is very lazy."
question = "Who is very lazy?"
answer = answer_question(question, text)
print(answer)
'''
#################################################################################################

# Create your views here.
def index(request):
    # return HttpResponse("Home page")
    return render(request,'index.html')

def admin_index(request):
    # return HttpResponse("Home page")
    return render(request,'admin_index.html')

def home_chart():
    exp_vals = [len(electricity_data),len(information_data),len(jal_jeevan)]
    exp_labels = ["Electricity","Information","Jal nigam"]
    plt.axis("equal")
    plt.pie(exp_vals,labels=exp_labels,radius=1.2,autopct="%0.2f%%")
    # Save the pie chart to a file
    image_path = os.path.join(settings.BASE_DIR,"/static/image/data.png")
    try: 
        plt.savefig(image_path)
        print("Success")
    except:
        print("Failed")
home_chart()


def answering_function(sentences_to_classify):
    print("Sentence :: ",sentences_to_classify)
    predicted_categories = classify_sentences(sentences_to_classify)
    category = None
    for sentence, category in zip(sentences_to_classify, predicted_categories):
        print("Sentence:", sentence)
        print("Predicted category:", category)
        print()
        
    ans, score = None, 0
    final_answer = None
    if category == "information":
        for i in information_data:
            temp_score =  answer_question(sentences_to_classify, i.que)
            if temp_score > score:
                score = temp_score
                final_answer = i.ans
        if score < 2 or score < len(sentences_to_classify)//4:
            try:
                raised_questions.objects.get(que=sentences_to_classify)
                return "Sorry! But query is already raised"
            except:
                raised_questions.objects.create(que = sentences_to_classify, dept=category)
                return "Query raised."
        else:
            return final_answer
    if category == "electricity":
        for i in electricity_data:
            temp_score =  answer_question(sentences_to_classify, i.que)
            if temp_score > score:
                score = temp_score
               
                final_answer = i.ans
        if score < 2 or score < len(sentences_to_classify)//4:
            
            try:
                raised_questions.objects.get(que=sentences_to_classify)
                return "Sorry! But query is already raised"
            except:
                raised_questions.objects.create(que = sentences_to_classify, dept=category)
                return "Query raised."
        else:
            return final_answer
    if category == "Jal_Jeevan_Mission":
        for i in jal_jeevan:
            temp_score =  answer_question(sentences_to_classify, i.que)
            if temp_score > score:
                score = temp_score
                final_answer = i.ans
        if score < 2 or score < len(sentences_to_classify)//4:
            
            try:
                raised_questions.objects.get(que=sentences_to_classify)
                return "Sorry! But query is already raised"
            except:
                raised_questions.objects.create(que = sentences_to_classify, dept=category)
                return "Query raised."
        else:
            return final_answer

@csrf_exempt
def answer_it(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        message = data.get('message')
        #message = request.POST.get('message')
        print(message)
        sentences = []
        sentences.append(message)
        ans = answering_function(sentences)
        # Perform your processing logic here based on the message
        # For example, you can pass it to a model or perform any other operations
    
        # Generate a response
        response_data = {
            'status': 'success',
            'message': ans,
        }

        return JsonResponse(response_data)
    
    # If the request method is not POST or it's not an AJAX request, return an error
    response_data = {
        'status': 'error',
        'message': 'Invalid request.',
    }
    return JsonResponse(response_data, status=400)
    
def aboutus(request):
    return render(request,'aboutus.html')

def admin_aboutus(request):
    return render(request,'admin_aboutus.html')

def login(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password=password)

            print("Hi dear")
            if user is not None and user.is_superuser:
                # login(request,user)
                messages.success(request, 'Operation successful!')
                # return HttpResponse("Successful")
                return redirect('gov')
            else:
                return HttpResponse("Failed")
    except:
        pass
    return render(request,'login.html')

def dept(request):
    return render(request,'dept.html')

def raised(request):
    qa = raised_questions.objects.all()
    return render(request,'raised.html',{'qa' : qa})

def gov(request):
    qa = raised_questions.objects.all()
    return render(request,'gov.html',{'qa':qa})

def gov_data(request,depth):
    try:
        if request.method == "POST":
            dept = request.POST.get('dept')
            que = request.POST.get('que')
            ans = request.POST.get('answer')
            if depth == 'information':
                datai = information.objects.create(que = que,ans = ans)
                datai.save()
                # r = raised_questions.objects.get(dept = dept)
                # r.remove()
                print(dept,"i")
            elif depth == 'electricity':
                datae = electricity.objects.create(que = que,ans = ans)
                datae.save()
                print(dept,"e")
            elif depth == 'jal_jeevan_mission':
                dataj = Jal_Jeevan_Mission.objects.create(que = que,ans = ans)
                dataj.save()
                print(dept,'j')
            else:
                print(dept)
            obj = raised_questions.objects.get(que = que)
            obj.delete()
    except:
        pass
    return redirect('gov')

