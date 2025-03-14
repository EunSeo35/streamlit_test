import streamlit as st
import pyaudio
import numpy as np
import wave
import io

# 오디오 설정
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # 샘플링 레이트 (Hz)
CHUNK = 1024  # 버퍼 크기
RECORD_SECONDS = 5  # 녹음 시간

def main():
    st.title("🎙️ PyAudio 테스트 앱")
    
    # PyAudio 객체 생성
    audio = pyaudio.PyAudio()

    # 오디오 스트림 열기
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, frames_per_buffer=CHUNK)

    st.write("🔴 마이크 입력을 실시간으로 받아오고 있습니다...")

    if st.button("🎤 녹음 시작"):
        frames = []
        st.write("녹음 중...")

        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        # 녹음 종료
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        st.success("✅ 녹음 완료!")

        # 오디오 데이터를 numpy 배열로 변환하여 시각화
        np_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        st.line_chart(np_data)

        # 오디오 데이터를 BytesIO에 저장 (재생 기능 추가)
        audio_buffer = io.BytesIO()
        wf = wave.open(audio_buffer, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        # 녹음된 오디오 재생
        st.audio(audio_buffer.getvalue(), format="audio/wav")

if __name__ == "__main__":
    main()
