from flask import Flask
from flask_restx import Api, Resource
from elasticapm.contrib.flask import ElasticAPM
import pyfiglet
import os
import requests
from datetime import datetime
import hashlib

from . import worker_classes_api
from . import worker_entities_api
from . import worker_similarities_api
from . import worker_services_api
from . import worker_logic
from .worker_logger import create_logger

logger = create_logger(__name__)

# options: classes, entities, similarities
WORKER_ROUTE = 'classes'
URL = os.getenv('WORKER_URL') or 'http://<worker_ip>:5001'
# TITLE CARD
title = f"{WORKER_ROUTE.title()} Worker API"
version = "1.0"
description = f"A worker that handles {WORKER_ROUTE} type requests."

print(pyfiglet.figlet_format("WRKR", 'roman'))
print(f'{title}')
print(f'Version {version}')


app = Flask(__name__)
ElasticAPM(app)

# environment variable to determine whether to include mock workers
adminkey = os.getenv('ADMINKEY') or '<admin-key>'
gateway_url = os.getenv('GATEWAY_URL') or 'http://<gateway_ip>:5000/worker'

# create worker instance
worker = worker_logic.Worker(url=URL, route=WORKER_ROUTE)

try:
    # submit put to gateway to make service available
    worker_put_request = worker.worker_put_request()
    headers = {'adminkey': adminkey}
    response = requests.put(url=gateway_url, json=worker_put_request, headers=headers)
    response.raise_for_status()
    logger.info(f'Successfully connected to gateway at: {gateway_url}')
except Exception:
    logger.info('Not connecting to gateway')

# Expand the Swagger UI when it is loaded: list or full
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
# Globally enable validating
app.config['RESTX_VALIDATE'] = True
# Enable or disable the mask field, by default X-Fields
app.config['RESTX_MASK_SWAGGER'] = False
# No automatically appended 404 message
app.config['ERROR_404_HELP'] = False

api = Api(app, version=version, title=title, description=str(description),)

# routes
models_ns = api.namespace("models", description="Data Science Models")

if WORKER_ROUTE == 'classes':
    request_body = worker_classes_api.get_classes_body(api)
    post_response = worker_classes_api.get_classes_post_response(api)
elif WORKER_ROUTE == 'entities':
    request_body = worker_entities_api.get_entities_body(api)
    post_response = worker_entities_api.get_entities_post_response(api)
elif WORKER_ROUTE == 'similarities':
    request_body = worker_similarities_api.get_similarities_body(api)
    post_response = worker_similarities_api.get_similarities_post_response(api)
else:
    raise ValueError(f'Invalid WORKER_ROUTE value: {WORKER_ROUTE}')

# responses
services_put_body = worker_services_api.get_services_put_body(api)


@models_ns.route("/")
class Models(Resource):
    """GET a list of all models, and POST to get model handling"""
    @api.expect(request_body)
    @api.marshal_with(post_response)
    @api.response(404, 'No such model')
    def post(self):
        """Request model output handling for something"""

        request_in_time = datetime.now()

        payload = api.marshal(api.payload, request_body)
        response = worker.handle_request(payload)

        logger.info(f"POST text hash: {hashlib.sha256(response['text'].encode()).hexdigest()}")
        logger.info(f'POST REQUEST t: {request_in_time}, en: {datetime.now()}, '\
             f'dur: {(datetime.now() - request_in_time).total_seconds()*1000}ms')
        logger.info(f'POST Classes detected: {response["classes"]}')


        return response

    @api.marshal_with(services_put_body)
    def get(self):
        """Get list of available models for this worker"""

        request_in_time = datetime.now()

        response = worker.worker_put_request()

        logger.info(f'GET REQUEST st: {request_in_time}, en: {datetime.now()}, '\
             f'dur: {(datetime.now() - request_in_time).total_seconds()*1000}ms')

        return response


@app.route('/health', methods=['GET'])
def health():
    return 'Service Up', 200


if __name__ == "__main__":
    app.run(debug=True)
