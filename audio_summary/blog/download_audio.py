from yt_dlp import YoutubeDL


def get_audio_file(url: str):
    ydl_opts = {
        'outtmpl': './audio.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }
    ydl = YoutubeDL(ydl_opts)
    ydl.download([url])


def main():
    get_audio_file("https://voicy.jp/channel/2627/559190")


if __name__ == '__main__':
    main()
