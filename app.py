from flask import Flask, request, render_template
import os
import shutil
import random
import string
import time

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
TEMP_FOLDER = 'temp'
EXPIRATION_TIME = 24 * 60 * 60  # 24 hours in seconds


def generate_random_directory():
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return random_chars


def delete_expired_directories():
    current_time = time.time()
    for dir_name in os.listdir(TEMP_FOLDER):
        dir_path = os.path.join(TEMP_FOLDER, dir_name)
        if os.path.isdir(dir_path):
            last_modified = os.path.getmtime(dir_path)
            if current_time - last_modified >= EXPIRATION_TIME:
                shutil.rmtree(dir_path)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            random_dir = generate_random_directory()
            upload_dir = os.path.join(UPLOAD_FOLDER, random_dir)
            temp_dir = os.path.join(TEMP_FOLDER, random_dir)

            os.makedirs(upload_dir)
            os.makedirs(temp_dir)

            file.save(os.path.join(upload_dir, file.filename))

            return {'directory': random_dir}

        return {'error': 'File not found'}

    return render_template('index.html')


@app.route('/delete/<directory>', methods=['DELETE'])
def delete_directory(directory):
    upload_dir = os.path.join(UPLOAD_FOLDER, directory)
    temp_dir = os.path.join(TEMP_FOLDER, directory)

    if os.path.isdir(upload_dir):
        shutil.rmtree(upload_dir)
    if os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir)

    return {'message': 'Directory deleted'}


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)

    delete_expired_directories()
