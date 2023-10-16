import pandas as pd
import regex as re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

from fastapi import FastAPI
from joblib import load


df = pd.read_csv('/home/mayank/Desktop/learning/spam.csv',encoding = 'ISO-8859-1')
df.head()

df.drop(['Unnamed: 2','Unnamed: 3','Unnamed: 4'],axis=1)


def cleantext(text):
    text = re.sub(r"[W_]",' ',text.lower()).replace('-','')
    words = [word for word in text.split() if word not in ENGLISH_STOP_WORDS]
    new_text = " ".join(words)
    return new_text


vectorizer = TfidfVectorizer()
encoder = LabelEncoder()

df['v1'] = encoder.fit_transform(df['v1'])

X = df['v2'].apply(cleantext)
y = df['v1']

X_train , X_test , y_train , y_test = train_test_split(X,y,test_size = 0.2)


#switcher class for various estimators

class my_classifier(BaseEstimator):
    
    def __init__(self,estimator = None):
        self.estimator = estimator
        
    def fit(self,X,y):
        return self.estimator.fit(X,y)
    
    def predict(self,X):
        return self.estimator.predict(X)
    
    def predict_proba(self,X):
        return self.estimator.predict_proba(X)
    
    def score(self,X,y):
        return self.estimator.score(X,y)
    
params = [{'clf':[LogisticRegression()]},{'clf':[RandomForestClassifier()]},{'clf':[DecisionTreeClassifier()]}]

make_pipeline  = Pipeline([('tfidf',vectorizer),('clf',my_classifier())])

grid = GridSearchCV(make_pipeline,params,cv=5)
grid.fit(X_train,y_train)


y_pred = grid.predict(X_test)
acc = accuracy_score(y_test,y_pred)
print(f'Accuracy score is {acc*100}')


filename = 'model_for_spam'
from joblib import dump
dump(grid,filename)


#Initialize app
app = FastAPI()

#Load model
fname = 'model_for_spam'
model = load(fname)

#Define function for classification

def classify(model,text):
    text = cleantext(text)
    prediction = model.predict([text])[0]
    res = "Ham" if prediction == 0 else 'spam'
    spam_prob = model.predict_proba([text])[0][1]
    return {'label': res , 'spam_probability': spam_prob}


@app.get('/')
def root():
    return "Welcome to Spam Message Classifier API"

@app.get('spam_path/{message}')
async def detect_spam_path(message:str):
    return classify(model,message)
