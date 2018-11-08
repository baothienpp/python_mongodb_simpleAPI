from flask import Flask, request, jsonify
from database import Database

app = Flask(__name__)


@app.route('/config', methods=['POST', 'GET'])
def config():
    if request.method == 'POST':
        db.push()
    else:
        tenant = request.args.get('tenant')
        integration_type = request.args.get('integration_type')
        result = db.query(tenant=tenant, integration_type=integration_type)
        return result

if __name__ == 'main':
    db = Database()
    app.run()
