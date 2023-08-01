from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__, static_url_path='/static')

# Load the model from the pickle file
with open('pipe.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the form data from the request
        batting_team = request.form['batting_team']
        bowling_team = request.form['bowling_team']
        city = request.form['city']
        current_score = float(request.form['current_score'])
        balls_left = float(request.form['balls_left'])
        wickets_left = float(request.form['wickets_left'])
        current_rr = float(request.form['current_rr'])
        last_five = float(request.form['last_five'])

        # Process the data and make the prediction using the loaded model
        x1 = {
        "batting_team": batting_team,
        "bowling_team": bowling_team,
        "city": city,
        "current_score": current_score,
        "balls_left": balls_left,
        "wickets_left": wickets_left,
        "crr": current_rr,
        "last_five": last_five
            }
        # Convert the dictionary to DataFrame
        d = pd.DataFrame([x1])
        prediction = model.predict(d)
        prediction_value = float(prediction[0])
        prediction_value = np.round(prediction_value,2)
        # Return the prediction as JSON response
        return jsonify({'prediction': prediction_value})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
