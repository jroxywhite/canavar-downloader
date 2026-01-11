from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Render/Linux ortamı için en güvenli yazma alanı
DOWNLOAD_FOLDER = '/tmp/downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    format_type = request.form.get('format')
    
    # YouTube bot engelini aşmak ve düzgün indirme yapmak için ayarlar
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'format_sort': ['ext:mp4:m4a'],
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        }
    }

    if format_type == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        # En uyumlu MP4 formatı
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Video bilgilerini al ve indir
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            
            # MP3 ise uzantıyı düzelt
            if format_type == 'mp3':
                filename = os.path.splitext(filename)[0] + '.mp3'
            
            # Dosyayı kullanıcıya gönder
            return send_file(filename, as_attachment=True)
            
    except Exception as e:
        print(f"KRİTİK HATA: {str(e)}")
        return f"Dönüştürme sırasında bir hata oluştu: {str(e)}", 500

if __name__ == '__main__':
    # Render'ın atadığı portu kullan
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
