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
        # En uyumlu MP4 formatı
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Önce bilgi çek, sonra indir
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            
            # MP3 ise uzantıyı garantiye al
            if format_type == 'mp3':
                filename = os.path.splitext(filename)[0] + '.mp3'
            
            # Dosyayı kullanıcıya gönder ve sunucudan temizle (opsiyonel ama güvenli)
            return send_file(filename, as_attachment=True)
            
    except Exception as e:
        print(f"KRİTİK HATA: {str(e)}")
        return f"Dönüştürme sırasında bir hata oluştu: {str(e)}", 500

if __name__ == '__main__':
    # Render'ın atadığı portu kullan, yoksa 10000 kullan
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
