from quart import Quart, request, Response
import json
from database import Database

app = Quart(__name__)


@app.route('/config', methods=['POST', 'GET'])
async def config():
    if request.method == 'POST':
        data = await request.get_json(force=True)
        status = await db.push(data)
        if status:
            return Response(status=201, mimetype='application/json')
        else:
            return Response(status=400, mimetype='application/json')

    else:
        tenant = request.args.get('tenant')
        integration_type = request.args.get('integration_type')
        result = await db.query(tenant=tenant, integration_type=integration_type)
        if result:
            response = Response(json.dumps(result), status=200, mimetype='application/json')
            return response
        else:
            return Response('Document not found', status=404, mimetype='application/json')


if __name__ == '__main__':
    db = Database()
    app.run(debug=True)
