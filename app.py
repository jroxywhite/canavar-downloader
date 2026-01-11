from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# İndirilen dosyaların geçici olarak tutulacağı yer
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    format_type = request.form.get('format')
    
    # yt-dlp ayarları
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
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
        # En yüksek kalite MP4 kombinasyonu
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            
            # MP3 dönüşümü sonrası dosya adını güncelle
            if format_type == 'mp3':
                filename = os.path.splitext(filename)[0] + '.mp3'
            
            # Dosyayı kullanıcıya gönder
            return send_file(filename, as_attachment=True)
            
    except Exception as e:
        return f"Hata oluştu: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)