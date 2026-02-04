import os 
from tensorflow.keras.models import load_model 
import pickle 
import numpy as np 
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from flask import Flask, request, jsonify, render_template
from sklearn.metrics import classification_report

app = Flask(__name__)

## ______________________________________________loading_preprocessor_________________________________________________

BASE_DIR = os.path.dirname(os.path.abspath(__file__ ))
PREPROCESSOR_PATH = os.path.join(BASE_DIR, "models", "preprocessor.pkl")
model_path = r'D:\loan_prediction\models\loan_default_model.keras'


with open(PREPROCESSOR_PATH, "rb") as f:
    preprocessor = pickle.load(f)

print("preprocessor is loading__ succesfully")
model = load_model(model_path, compile=False)
print("Model loaded successfully")


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')
@app.route('/predict' , methods = ["GET"])
def predict_page():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 1. Get form data
        form_data = request.form.to_dict()

        # 2. Convert to DataFrame (VERY IMPORTANT)
        input_df = pd.DataFrame([form_data])

        # 3. Convert numeric columns properly
        num_cols = [
            'Age', 'Income', 'LoanAmount', 'CreditScore',
            'MonthsEmployed', 'NumCreditLines',
            'InterestRate', 'LoanTerm', 'DTIRatio'
        ]

        for col in num_cols:
            input_df[col] = input_df[col].astype(float)
        
        print(input_df,"\n")

        # 4. Preprocess input
        processed_input = preprocessor.transform(input_df)
        print(processed_input)
        # 5. Model prediction
        prediction_prob = model.predict(processed_input)[0][0]
        
        prediction = int(prediction_prob >= 0.5)
        print(prediction_prob,'\n',prediction)
        # 6. Result message
        result = "High Risk (Default)" if prediction == 1 else "Low Risk (No Default)"
        
        return render_template(
            "index.html",
            prediction=result,
            probability=round(prediction_prob * 100, 2)
        )

    except Exception as e:
        return render_template("errorpage.html")


if __name__ =="__main__":
    app.run(debug=True ,host='0.0.0.0' , port = 5000)