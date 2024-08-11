import os

import glob

from flask import Flask, render_template, request, redirect, url_for



app = Flask(__name__)



def find_files(directory, file_types, search_string, exact_match):

    files = []

    for root, dirs, filenames in os.walk(directory):

        for filename in filenames:

            file_path = os.path.join(root, filename)

            file_extension = os.path.splitext(filename)[1].lower()

            

            if file_types and file_extension not in file_types:

                continue

            

            if exact_match:

                if search_string == filename:

                    files.append(file_path)

            else:

                if search_string.lower() in filename.lower():

                    files.append(file_path)

    return files



def export_to_file(files, filename='files_to_delete.txt'):

    with open(filename, 'w') as f:

        for file in files:

            f.write(f"{file}\n")



def delete_files_from_list(filename='files_to_delete.txt'):

    deleted_files = []

    with open(filename, 'r') as f:

        for line in f:

            file_path = line.strip()

            if os.path.exists(file_path):

                os.remove(file_path)

                deleted_files.append(file_path)

    return deleted_files



@app.route('/', methods=['GET', 'POST'])

def index():

    if request.method == 'POST':

        action = request.form.get('action')

        if action == 'find':

            directory = request.form.get('directory', '.')

            file_types = request.form.get('file_types', '').split()

            file_types = [f.lower() if f.startswith('.') else f'.{f.lower()}' for f in file_types]

            search_string = request.form.get('search_string', '')

            exact_match = request.form.get('exact_match') == 'on'

            

            files = find_files(directory, file_types, search_string, exact_match)

            export_to_file(files)

            return render_template('index.html', files=files, action='review')

        elif action == 'delete':

            deleted_files = delete_files_from_list()

            return render_template('index.html', deleted_files=deleted_files, action='deleted')

    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

