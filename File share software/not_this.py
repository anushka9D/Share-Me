from flask import Flask, request, send_file, render_template_string, send_from_directory, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists('UPLOAD_FOLDER'):
    os.makedirs(UPLOAD_FOLDER)


    
    # HTML for file upload form and file list
    html = '''
    <!doctype html>
    <title>File Upload</title>
    <h1>Upload File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    
    <h1>Download Files</h1>
    <ul>
      {% for filename in files %}
        <li><a href="{{ url_for('download_file', filename=filename) }}">{{ filename }}</a></li>
      {% endfor %}
    </ul>
    ''', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
