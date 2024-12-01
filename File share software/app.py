from flask import Flask, request, send_from_directory, render_template_string, redirect, url_for, flash
import os

app = Flask(__name__)

# Directory where files will be stored/uploaded
UPLOAD_FOLDER = 'uploaded_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key'  # For flashing messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash("No file part", "danger")
            return redirect(request.url)
        
        file = request.files['file']
        
        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash("No selected file", "danger")
            return redirect(request.url)
        
        # Save the file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        flash("File uploaded successfully", "success")
        return redirect(url_for('index'))  # Redirect to the same page to show the updated list

    # HTML for file upload form and file list
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File Upload and Management</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
    </head>
    <body>
        <div class="container">
            <h1>Upload and Manage Files</h1>
            
            <!-- Flash messages for notifications -->
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert {{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <form method="post" enctype="multipart/form-data">
                <div class="file-input-wrapper">
                    <button type="button" class="file-input-btn">Choose File</button>
                    <input type="file" name="file">
                </div>
                <input type="submit" value="Upload">
            </form>
            
            <div class="file-list">
                <h2>Uploaded Files</h2>
                <ul>
                    {% for filename in files %}
                        <li>
                            <span><a href="{{ url_for('download_file', filename=filename) }}">{{ filename }}</a></span>
                            <form method="post" action="{{ url_for('delete_file', filename=filename) }}" style="display:inline;">
                                <button type="submit" class="delete-btn">Delete</button>
                            </form>
                        </li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </body>
    </html>
    ''', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(f"File '{filename}' deleted successfully", "success")
    except Exception as e:
        flash(f"Failed to delete file: {str(e)}", "danger")
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
