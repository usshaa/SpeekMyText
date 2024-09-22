document.getElementById('generate_btn').addEventListener('click', function () {
    const text = document.getElementById('text').value;
    const voiceSample = document.getElementById('voice_sample').files[0];

    if (!text || !voiceSample) {
        alert('Please provide both text and a voice sample.');
        return;
    }

    const formData = new FormData();
    formData.append('text', text);
    formData.append('voice_sample', voiceSample);

    fetch('/generate_speech', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
          document.getElementById('play_btn').disabled = false;
          document.getElementById('download_btn').disabled = false;

          // Set audio player source to play the generated audio
          const audioPlayer = document.getElementById('audio_player');
          audioPlayer.src = data.audio_url;

          // Set download link
          document.getElementById('download_btn').onclick = function () {
              window.location.href = data.download_url;
          };

          // Play audio when play button is clicked
          document.getElementById('play_btn').onclick = function () {
              audioPlayer.play();
          };
      })
      .catch(error => console.error('Error:', error));
});
