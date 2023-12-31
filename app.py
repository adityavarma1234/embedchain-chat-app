from flask import Flask, request, jsonify, Response
from flask_cors import CORS  # Import CORS
from werkzeug.utils import secure_filename
import os
from embedchain import App


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp' 

os.environ["OPENAI_API_KEY"] = "YOURAPI_KEY" # need to set up billing for this
embedchain = App()

# Configure CORS to allow requests from your frontend URL
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# Function to handle file uploads
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'txt'}

def data_type_of_file(filename):
    file_type = {'pdf': 'pdf_file', 'txt': 'text'}
    return file_type.get(filename.rsplit('.', 1)[1].lower())

@app.route('/')
def home():
    return 'Chat Application Backend'


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Integrate the file with embedchain here using embedchain.add()
        # Example: embedchain.add(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        embedchain.add(os.path.join(app.config['UPLOAD_FOLDER'], filename), data_type=data_type_of_file(filename))
        return jsonify({"message": "File uploaded and integrated with embedchain successfully"})
    return Response("{'error': 'Invalid file format'}", status=400, mimetype='application/json')

# app.py
@app.route('/api/chat', methods=['POST'])
def chat_with_bot():
    user_input = request.json.get('user_input')

    # Use embedchain.query() to interact with the bot
    bot_response = embedchain.query(user_input)

    return jsonify({"bot_response": bot_response})


if __name__ == '__main__':
    app.run(debug=True)