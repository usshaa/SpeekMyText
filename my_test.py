from TTS.api import TTS

# Initialize the TTS model with your trained model
tts = TTS(model_name="tts_models/en/ek1/tacotron2")

def text_to_speech(text, output_file):
    # Generate speech and save it to a file
    tts.tts_to_file(text, file_path=output_file)

# Example usage
text_to_speech("Hello, this is a test of the custom TTS model.", "output.wav")
