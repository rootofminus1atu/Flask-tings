# unused stuff

INTERESTING_META = [
    "ami-id",
    "ami-launch-index",
    "ami-manifest-path",
    "hostname",
    "instance-action",
    "instance-id",
    "instance-life-cycle",
    "instance-type",
    "local-hostname",
    "local-ipv4",
    "mac",
    "profile",
    "public-hostname",
    "public-ipv4",
    "reservation-id",
    "security-groups",
    "system"
]

@app.route('/api/hello', methods=['GET'])
def hello():
    name = request.args.get('name')
    if name:
        return jsonify({'message': f'Hello, {name}!'})
    else:
        return jsonify({'message': 'Hello! Please provide a name parameter.'})
    


@app.route('/api/metadata/<key>', methods=['GET'])
def get_metadata(key):
    try:
        metadata_value = subprocess.check_output(['curl', '-s', f'http://169.254.169.254/latest/meta-data/{key}'])
        metadata_value = metadata_value.decode('utf-8').strip()
        return jsonify({key: metadata_value})
    except Exception as e:
        return jsonify({'error': str(e)})