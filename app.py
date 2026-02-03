import os 
import tensorflow as tf 
from tensorflow.keras.models import load_model 
import pickle 
import numpy as np 
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

## ______________________________________________loading_preprocessor_________________________________________________

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREPROCESSOR_PATH = os.path.join(BASE_DIR, "models", "preprocessor.pkl")
model_path = os.path.join(BASE_DIR, "models", "loan_default_model.keras")

with open(PREPROCESSOR_PATH, "rb") as f:
    preprocessor = pickle.load(f)

print("preprocessor is loading__ succesfully")


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


if __name__ =="__main__":
    app.run(debug=True ,host='0.0.0.0' , port = 5000)