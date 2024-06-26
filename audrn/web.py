import streamlit as st
import yt_dlp

def my_hook(d):
    if d['status'] == 'downloading':
        # 진행 상태를 퍼센트로 계산
        p = d['_percent_str']
        m_index = p.find('m')
        percent_index = p.find('%')
        p = p[m_index+1:percent_index]
        st.text(p)
        progress_bar.progress(float(p)/100, "Downloading...")
    if d['status'] == 'finished':
        st.success('다운로드 완료!')
        st.video('videos/downloaded_video.mkv')

st.title('YouTube 동영상 다운로더')

# 사용자로부터 YouTube URL 입력받기
video_url = st.text_input('YouTube URL을 입력해주세요.')

# 동영상 다운로드 버튼
if st.button('동영상 다운로드'):
    if not video_url:
        st.error('URL을 입력해주세요.')
    else:
        # youtube-dl 옵션 설정
        ydl_opts = {
            'format': 'best[height=720]/best',
            'outtmpl': 'videos/downloaded_video.mkv',  # 다운로드 파일 이름
            'progress_hooks': [my_hook],  # 진행 상태 콜백 함수 설정
        }
        
        # 동영상 다운로드 시도
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            progress_bar = st.progress(0, text="Downloading...")
            try:
                ydl.download([video_url])
                st.success('다운로드 완료!')
                st.video('videos/downloaded_video.mkv')
            except Exception as e:
                st.error('다운로드 중 오류 발생: {}'.format(e))
