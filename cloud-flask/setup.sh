# ==== #
# note #
# ==== #
# this script is no longer used for the setup and user data

#!/bin/bash

# variables
bucket_name="zipped-website"
zipped_file_name="random-flask.zip"
server_domain="$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"



# all the potentially necessary updates and installs
sudo yum update -y
sudo yum install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
sudo yum install aws-cli -y



# ================= #
# configuring nginx #
# ==================#
# so that instead of visiting `domain.com:5000` we could visit `domain.com`

# we look for this property in nginx.conf, since we have to change it
if ! grep -q "server_names_hash_bucket_size" /etc/nginx/nginx.conf; then
    # adding a line if it doesn't exist (so far it's alway been this case)
    sudo sed -i '/^http {/a server_names_hash_bucket_size 128;' /etc/nginx/nginx.conf
else
    # changing it if it does
    sudo sed -i 's/server_names_hash_bucket_size.*/server_names_hash_bucket_size 128;/' /etc/nginx/nginx.conf
fi

# putting the stuff below into an additional config element that will be used for port forwarding
# notice the 5000, that's where our flask app will be running
sudo tee /etc/nginx/conf.d/flask_app.conf > /dev/null <<EOF
server {
    listen 80;
    server_name $server_domain;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# restarting nginx
sudo systemctl restart nginx



# ====================== #
# configuring our webapp #
# ====================== #

# creating a place for the flask app to live
mkdir app

# copying the zipped website into it
aws s3 cp s3://$bucket_name/$zipped_file_name /app

# going into that directory and unzipping the zip
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
