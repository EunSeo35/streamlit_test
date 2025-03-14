import streamlit as st

st.title("5초 동안 마이크 녹음")

audio_html = """
    <script>
    let chunks = [];
    let recorder;
    let recordingTime = 5000; // 5초
    let audioURL = '';

    async function startRecording() {
        let stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        recorder = new MediaRecorder(stream);
        recorder.ondataavailable = event => chunks.push(event.data);
        recorder.start();

        // 녹음 시간 5초 후 자동 종료
        setTimeout(() => {
            stopRecording();
        }, recordingTime);
    }

    function stopRecording() {
        recorder.stop();
        recorder.onstop = function() {
            let blob = new Blob(chunks, { type: 'audio/wav' });
            audioURL = URL.createObjectURL(blob);
        };
    }

    function playAudio() {
        document.getElementById("audio").src = audioURL;
    }
    </script>

    <button onclick="startRecording()">녹음 시작</button>
    <br>
    <button onclick="playAudio()">듣기</button>
    <br>
    <audio id="audio" controls></audio>
"""

st.components.v1.html(audio_html, height=200)
