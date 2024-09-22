import os
import torch
import torchaudio
from flask import Flask, render_template, request, redirect, url_for, send_file
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voice
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/audio_files/'
app.config['MAX_CONTENT_PATH'] = 10 * 1024 * 1024  # 10MB max upload

# Tortoise TTS model initialization
tts = TextToSpeech()

# Homepage Route - Displays the UI form
@app.route('/')
def index():
    return render_template('index.html')

# Upload voice samples and process the text-to-speech synthesis
@app.route('/generate', methods=['POST'])
def generate():
    if 'voice_samples' not in request.files or request.form['text'] == '':
        return redirect(url_for('index'))
    
    # Save the uploaded voice samples
    uploaded_files = request.files.getlist('voice_samples')
    custom_voice_folder = os.path.join('tortoise/voices', 'custom_voice')
    os.makedirs(custom_voice_folder, exist_ok=True)

    for i, file in enumerate(uploaded_files):
        filename = secure_filename(f'custom_voice_{i}.wav')
        file_path = os.path.join(custom_voice_folder, filename)
        file.save(file_path)

    # Load the voice samples and generate speech
    text = request.form['text']
    voice_samples, conditioning_latents = load_voice('custom_voice')
    preset = request.form.get('preset', 'fast')

    # Generate the speech with the custom voice
    gen = tts.tts_with_preset(text, voice_samples=voice_samples, conditioning_latents=conditioning_latents, preset=preset)

    # Save generated audio
    audio_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'generated_audio.wav')
    torchaudio.save(audio_file_path, gen.squeeze(0).cpu(), 24000)

    return render_template('result.html', audio_file='generated_audio.wav')

# Route to download the generated audio
@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
