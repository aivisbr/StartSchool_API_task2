import os
from flask import Flask, render_template, request, jsonify
from stt_converter import transcribe_audio, download_audio
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB max limit

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        transcription_text = ""
        
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            result = transcribe_audio(filepath)
            if result:
                transcription_text = result.text
            
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
                
        elif 'url' in request.form and request.form['url'] != '':
            url = request.form['url']
            temp_path = download_audio(url, save_path=os.path.join(app.config['UPLOAD_FOLDER'], 'temp_url_audio.mp3'))
            
            if temp_path:
                result = transcribe_audio(temp_path)
                if result:
                    transcription_text = result.text
                
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            else:
                return jsonify({'error': 'Failed to download audio from URL'}), 400
        else:
             return jsonify({'error': 'No file or URL provided'}), 400

        return jsonify({'transcription': transcription_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
