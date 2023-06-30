from yt_dlp import YoutubeDL
import openai
import os
import time
from dotenv import load_dotenv
from llama_index import StorageContext, StringIterableReader, GPTVectorStoreIndex, load_index_from_storage

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


def get_audio_file(url: str):
    """get audio file from url

    Args:
        url (str): access url

    Returns:
        result (str): result of download audio file
    """

    option = {
        'outtmpl': './audio.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    ydl = YoutubeDL(option)
    ydl.download([url])


def get_audio_text(file_path: str) -> str:
    audio_file = open(file_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]


def convert_vector(audio_text: str) -> list:
    storage_path = "./storage"
    try:
        storage_context = StorageContext.from_defaults(persist_dir=storage_path)
        index = load_index_from_storage(storage_context)
    except Exception:
        documents = StringIterableReader().load_data(texts=[audio_text])
        index = GPTVectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=storage_path)

    return index


def get_summary_text(vector_index):
    query = "テキストの内容を5~10の項目に分けて要約してください"

    query_engine = vector_index.as_query_engine()
    response = query_engine.query(query)
    return response.response


def main():
    start = time.time()
    url = 'https://voicy.jp/channel/2448/558827'
    get_audio_file(url)
    transcript = get_audio_text("./audio.mp3")
    # print(f"transcript: {transcript}")
    vector_index = convert_vector(transcript)
    summary_text = get_summary_text(vector_index)
    print(f"summary_text: {summary_text}")
    print(f"実行時間: {time.time() - start}")


if __name__ == "__main__":
    main()
