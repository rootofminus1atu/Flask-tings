from flask import Flask, jsonify, request, render_template
from botocore.exceptions import NoCredentialsError
import boto3
import subprocess


BUCKET_NAME = 'zipped-webapp.zip'


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/metadata')
def metadata():
    mac = get_specific_metadata('mac')
    instance_type = get_specific_metadata('instance-type')

    return render_template('metadata.html', mac=mac, instance_type=instance_type)

@app.route('/other')
def other():
    return render_template('other.html')

@app.route('/file-upload')
def file_upload():
    return render_template('file-upload.html')



@app.route('/api/upload', methods=['POST'])
def upload_file_to_s3():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        try:
            s3 = boto3.client('s3')
            s3.upload_fileobj(file, BUCKET_NAME, file.filename)
            return jsonify({'message': 'File uploaded to S3 successfully'})
        except NoCredentialsError:
            return jsonify({'error': 'AWS credentials not found'})
    
    return jsonify({'error': 'Upload failed'})

def get_specific_metadata(key):
    try:
        metadata_value = subprocess.check_output(['curl', '-s', f'http://169.254.169.254/latest/meta-data/{key}'])
        metadata_value = metadata_value.decode('utf-8').strip()
        return metadata_value
    except Exception as e:
        return f":( error occured: {str(e)}"
