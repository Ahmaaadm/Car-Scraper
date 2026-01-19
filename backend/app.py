from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from scraper import IAAScraper
import os
import zipfile
import io
import shutil

app = Flask(__name__)
CORS(app)

@app.route('/')
def health_check():
    return jsonify({'status': 'ok', 'service': 'AutoSnap API'})

@app.route('/api/scrape', methods=['POST'])
def scrape_vehicle():
    """Scrape a single vehicle page and download images"""
    data = request.get_json()
    url = data.get('url', '').strip()

    if not url:
        return jsonify({
            'success': False,
            'error': 'Please provide a vehicle URL'
        }), 400

    if 'iaai.com' not in url or 'vehicle-details' not in url:
        return jsonify({
            'success': False,
            'error': 'URL must be an IAA vehicle details page (e.g., https://ca.iaai.com/vehicle-details/...)'
        }), 400

    scraper = IAAScraper(output_dir="downloads")
    try:
        result = scraper.scrape_vehicle_page(url)
        return jsonify(result)
    finally:
        scraper.close()

@app.route('/api/download/<folder_name>', methods=['GET'])
def download_folder(folder_name):
    """Download a folder as ZIP file"""
    folder_path = os.path.join("downloads", folder_name)

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return jsonify({
            'success': False,
            'error': 'Folder not found'
        }), 404

    # Create ZIP in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath):
                zf.write(filepath, filename)

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'{folder_name}.zip'
    )

@app.route('/api/delete/<folder_name>', methods=['DELETE'])
def delete_folder(folder_name):
    """Delete a folder after download"""
    folder_path = os.path.join("downloads", folder_name)

    if not os.path.exists(folder_path):
        return jsonify({
            'success': False,
            'error': 'Folder not found'
        }), 404

    try:
        shutil.rmtree(folder_path)
        return jsonify({
            'success': True,
            'message': f'Folder {folder_name} deleted'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
