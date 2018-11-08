from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/config', methods=['POST', 'GET'])
def config():
    if request.method == 'POST':
        pass
    else:
        tenant = request.args.get('tenant')
        integration_type = request.args.get('integration_type')
        pass


