import streamlit as st
import openai
import os
import shutil

import lib

AUDIO_FILE_PATH = "./audio.mp3"
STORAGE_PATH = "./storage"


def find_ffmpeg_directory():
    current_dir = os.getcwd()  # 現在のディレクトリを取得

    while True:
        if os.path.isdir(os.path.join(current_dir, 'ffmpeg')):
            return os.path.join(current_dir, 'ffmpeg')  # ffmpegディレクトリが見つかった場合、パスを返す

        # 親ディレクトリに移動
        current_dir = os.path.dirname(current_dir)

        # ルートディレクトリに到達した場合、ループを終了
        if current_dir == os.path.dirname(current_dir):
            break

    return None  # ffmpegディレクトリが見つからなかった場合、Noneを返す


def main():
    import os

    # ディレクトリの検索を実行
    ffmpeg_dir = find_ffmpeg_directory()

    if ffmpeg_dir:
        print(f"ffmpegディレクトリが見つかりました: {ffmpeg_dir}")
    else:
        print("ffmpegディレクトリが見つかりませんでした。")
    st.write(f"ffmpeg_dir: {ffmpeg_dir}")

    summary_prompt = ''
    audio_text = ''
    api_flag = False

    st.title('Audio Summary')

    if st.button("Reset", key="reset"):
        if os.path.exists(STORAGE_PATH):
            shutil.rmtree(STORAGE_PATH)
        if os.path.exists(AUDIO_FILE_PATH):
            os.remove(AUDIO_FILE_PATH)

    open_ai_api_key: str = st.text_input(label="Open AI API Key (required)", type="password")

    if st.button("Register Open AI API Key", key="api_key") and open_ai_api_key:
        st.success("Open AI API Key is set.", icon="✅")
        if (api_flag is False):
            os.environ['OPENAI_API_KEY'] = open_ai_api_key
            openai.api_key = open_ai_api_key
        api_flag = True

    audio_url: str = st.text_input(label="Audio URL (required)")

    if audio_url:
        st.success("Audio URL is set.", icon="✅")
        if st.button("Get Audio File", key="get_audio_file"):
            # https://voicy.jp/channel/1819/558826
            with st.spinner(text="Get Audio Data..."):
                lib.get_audio_file(audio_url)

    summary_prompt = st.selectbox(
        label="Choice Prompt (required)",
        options=[
            "テキストの内容を300字程度で要約してください。",
            "テキストの内容を5~10の項目に分けて要約してください",
            "テキストの内容を500字程度で要約してください。",
            "テキストの内容を1000字程度で要約してください。",
        ]
    )

    if audio_url and os.path.exists(AUDIO_FILE_PATH):
        st.success("Get Audio Data.", icon="✅")
        audio_file = open(AUDIO_FILE_PATH, 'rb')
        audio_bytes = audio_file.read()

        st.audio(audio_bytes, format='audio/mp3')
        st.download_button(label="Download Audio File", data=audio_bytes, file_name="audio.mp3", mime="audio/mp3")

        if st.button("Get Summary Text", key="get_summary_text"):
            with st.spinner(text="Convert Audio Text..."):
                audio_text = lib.get_audio_text(AUDIO_FILE_PATH)
            if audio_text:
                st.success("Convert Audio Text.", icon="✅")
                with st.expander("Audio Text"):
                    st.write(audio_text)
                with st.spinner(text="Get Summary Text..."):
                    summary_text = lib.get_summary_text(audio_text, summary_prompt)
                if summary_text:
                    st.success("Get Summary Text.", icon="✅")
                    st.write(summary_text)


if __name__ == "__main__":
    main()
