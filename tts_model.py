from TTS.api import TTS

# Initialize the TTS model
tts = TTS(model_name="tts_models/en/ek1/tacotron2")

def generate_speech(text, voice_sample_path, output_audio_path):
    # Generate speech using the TTS model
    tts.tts_to_file(text, speaker_wav=voice_sample_path, file_path=output_audio_path)
