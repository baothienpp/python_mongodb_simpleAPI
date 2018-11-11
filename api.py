from quart import Quart, request, Response
import json
from database import Database

app = Quart(__name__)


@app.route('/config', methods=['POST', 'GET'])
async def config():
    """

    :return:
    """
    db = app.config['database']
    if request.method == 'POST':
        data = await request.get_json(force=True)
        try:
            status = await db.push(data)
        except Exception as error:
            return Response(str(error), status=400, mimetype='application/json')

        if status:
            return Response('Document created!', status=201, mimetype='application/json')
        else:
            return Response('Cannot create document !', status=400, mimetype='application/json')

    else:
        tenant = request.args.get('tenant')
        integration_type = request.args.get('integration_type')

        try:
            result = await db.query(tenant=tenant, integration_type=integration_type)
        except Exception as error:
            return Response(str(error), status=400, mimetype='application/json')

        if result:
            response = Response(json.dumps(result[0]), status=200, mimetype='application/json')
            return response
        else:
            return Response('Document not found', status=404, mimetype='application/json')


if __name__ == '__main__':
    app.config['database'] = Database('localhost', 'data', 'configuration')
    app.run(debug=True)
