#!/bin/bash

# variables that the user can change
bucket_name="bucket-name"
zipped_file_name="zipped-webapp.zip"

# an update, just in case
sudo yum update -y



# getting the server name from metadata
server_domain="$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"

# embeding the server name in the nginx conf for the flask app
sed -i "s/server_name _;/server_name $server_domain;/" /etc/nginx/conf.d/flask_app.conf

# restarting nginx
sudo systemctl restart nginx



# copying the zipped website into the app directory
aws s3 cp s3://$bucket_name/$zipped_file_name /app

# going into the app directory and unzipping the zip
cd app
unzip $zipped_file_name



# creating a python virtual environment, to avoid "it works on my machine though" issues
python3 -m venv venv

# activating it
source venv/bin/activate

# installing the necessary packages
pip install -r requirements.txt

# running the flask webapp with gunicorn
gunicorn -w 4 -b 127.0.0.1:5000 run:app