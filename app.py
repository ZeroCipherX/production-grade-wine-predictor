from flask import Flask, render_template, request, jsonify
import os
from mlflow.models import predict
import numpy as np
from src.productiongradewinepredictor.pipeline.prediction_pipeline import PredictionPipeline
import requests
from dotenv import load_dotenv

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise RuntimeError("Set MISTRAL_API_KEY in .env")

app = Flask(__name__)  # initializing a flask app

@app.route("/ai_sommelier", methods=["POST"])
def ai_sommelier():
    score = request.json.get("score")
    prompt = f"A wine has a quality score of {score}. Briefly explain what this means for taste and market value. Max 50 words and dont use any dashes."
    resp = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MISTRAL_API_KEY}"
        },
        json={
            "model": "mistral-tiny",
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=10
    )
    return jsonify(resp.json()), resp.status_code

# end point / api / route
@app.route('/',methods=['GET'])  # route to display the home page
def homePage():
    return render_template("index.html")


@app.route('/train',methods=['GET'])  # route to train the pipeline
def training():
    os.system("python main.py")
    return "Training Successful!" 


@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            fixed_acidity =float(request.form['fixed_acidity'])
            volatile_acidity =float(request.form['volatile_acidity'])
            citric_acid =float(request.form['citric_acid'])
            residual_sugar =float(request.form['residual_sugar'])
            chlorides =float(request.form['chlorides'])
            free_sulfur_dioxide =float(request.form['free_sulfur_dioxide'])
            total_sulfur_dioxide =float(request.form['total_sulfur_dioxide'])
            density =float(request.form['density'])
            pH =float(request.form['pH'])
            sulphates =float(request.form['sulphates'])
            alcohol =float(request.form['alcohol'])
       
         
            data = [fixed_acidity,volatile_acidity,citric_acid,residual_sugar,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,pH,sulphates,alcohol]
            data = np.array(data).reshape(1, 11)
            
            obj = PredictionPipeline()
            predict = obj.predict(data)

            # Grabs the number, rounds it to 1 decimal place, and makes it a clean string
            clean_prediction = round(float(predict[0]), 1)
            return render_template('results.html', prediction = clean_prediction)

        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'

    else:
        return render_template('index.html')

if __name__ == "__main__":
	
	app.run(host="0.0.0.0", port = 8080)
     

