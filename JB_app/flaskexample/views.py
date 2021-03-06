from flask import request
from flask import render_template
from flaskexample import app
import pandas as pd
import joblib
from functions import status_to_words, raw_cleaning, get_grams, contributing_words

text_clf = joblib.load("models/text_clf_all.pkl")
#keywords = pd.read_csv("keywords_min.csv", index_col=0)
keywords = pd.read_csv("keywords_all_titleoff_100.csv", index_col=0)

@app.route('/')
@app.route('/index')
def enter():
    return render_template("input.html")

@app.route('/input')
def enter_description():
    return render_template("input.html")

@app.route('/output')
def model_result():
    #pull 'description' from input field and store it
    description = [request.args.get('description')]
    if len(description[0]) < 20:
        return render_template("error.html")
    try:
        cleaned = raw_cleaning(description, False)
        cleaned_grams = get_grams(description, False)
        #cleaned_words = list(set(cleaned.iloc[0].split()))
        prediction = text_clf.predict_proba(cleaned)
        output = pd.DataFrame()
        output['jobtitle'] = text_clf.classes_
        output['probability'] = prediction[0]
        contri_words = contributing_words(cleaned_grams, keywords)
        output = output.sort_values(by='probability', ascending=False)
    
        return render_template("output.html", title1=output.iloc[0,0],
                         title2=output.iloc[1,0],
                         title3=output.iloc[2,0],
                         title4=output.iloc[3,0],
                         title5=output.iloc[4,0],
                         title6=output.iloc[5,0],
                         title7=output.iloc[6,0],
                         score1=round(output.iloc[0,1],2),
                         score2=round(output.iloc[1,1],2),
                         score3=round(output.iloc[2,1],2),
                         score4=round(output.iloc[3,1],2),
                         score5=round(output.iloc[4,1],2),
                         score6=round(output.iloc[5,1],2),
                         score7=round(output.iloc[6,1],2),
                         words1=contri_words[output.iloc[0,0]],
                         words2=contri_words[output.iloc[1,0]])
    except:
        return render_template("error.html")
