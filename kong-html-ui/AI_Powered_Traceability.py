import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

OpenApi_Key = "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"
llm = OpenAI(api_token=OpenApi_Key)
pandas_ai = PandasAI(llm, conversational=True, save_charts=True, enable_cache=True)

@app.route('/ask', methods=['POST'])
def upload_file():
    try:
        # Check if the request contains a file and a string
        if 'file' not in request.files or 'string' not in request.form:
            return jsonify({'error': 'Both file and string are required'}), 400

        file = request.files['file']
        prompt = request.form['string']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the uploaded file (you can customize the save location)
        file.save('C:\\Users\\DhavalM1\\Traceability_uploads\\' + file.filename)
        df = pd.read_csv('C:\\Users\\DhavalM1\\Traceability_uploads\\' + file.filename)
        response = pandas_ai.run(df, prompt)

        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
