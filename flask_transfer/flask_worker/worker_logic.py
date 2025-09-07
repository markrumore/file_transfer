import os
import json
from flask import abort
import sys 
from datetime import datetime
import hashlib

import scripts.utils as s3_utils
from .worker_logger import create_logger

CURRENT_FILE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DEFAULT_LOCAL_MODEL_DIR = os.path.join(CURRENT_FILE_PATH, 'models', '')

logger = create_logger(__name__)




def model_formatter(nlp):
    """
    Formats SpaCy TextCat output to Gateway Classifier Format

    Args:
        nlp (SpaCy Pipeline): Must hace a trained TextCat in the pipeline

    Returns (callable): function that returns formatted textcat output
    """
    def get_results(text):
        doc = nlp(text)
        results = [{'value': v, 'score': s} for (v, s) in doc.cats.items()]
        return results
    return get_results


def filter_min_confidence(results, min_confidence=0.1):
    try:
        return list(filter(lambda i: i['score'] > min_confidence, results))
    except Exception:
        results


def filter_max_classes(results, max_classes=3):
    if not isinstance(max_classes, int):
        return results
    if len(results) > max_classes:
        return results[:max_classes]
    return results


class Worker:

    def __init__(self, url, route, model_mapping={}):
        self.url = url
        logger.info(f'Initializing using URL:{url}')
        self.route = route
        logger.info(f'Initializing using route: {route}')
        logger.info(f"S3 bucket for downloading models : "
                    f"{s3_utils.DEFAULT_S3_BUCKET}")
        self.model_mapping = {} 
        self.models_in_s3 = []
        self.local_models = []
        logger.info(f'Loaded models: {list(model_mapping)}')

    def worker_put_request(self):
        """
        Generate the body for the PUT request to the gateway.

        Format:
        {
            "url": "http://anything.com/worker",
            "route": "classes",
            "models": [
                {
                    "id": "fake_classify",
                    "description": "A fake model that randomly returns classes",
                },
            ]
        }

        Returns:
            dict: the request body dict
        """
        # base request
        models_info = list()
        for model in self.model_mapping:
            models_info.append({
                'id': model,
                'description': self.model_mapping[model]['description']
            })

        # format request
        request = {
            'url': self.url,
            'route': self.route,
            'models': models_info
        }

        # add models here
        logger.info(f'Returning models: {[d["id"] for d in request["models"]]}')
        return request

    def handle_request(self, request):
        """
        Logic for handling a request (i.e. passing to model)

        Args:
            request (dict): the request to be handled

        Returns:
            dict: the response in the correct format
        """

        request_in_time = datetime.now()

        # determine which model to use
        outputs = list()
        for model_name in request['classes']:

            # checking if the model is present in loaded models list
            if model_name not in self.model_mapping:

                # checking if the model is present in s3 models list
                self.models_in_s3 = \
                    [ f.split('/')[1].split('.')[0] for f in 
                      s3_utils.scrape_bucket() ]
                
                if model_name not in self.models_in_s3 and \
                    model_name not in os.listdir(DEFAULT_LOCAL_MODEL_DIR):
                
                    abort(404, f'No such model: {model_name}')
                
                else:

                    # downloading the model if present in s3
                    try:
                        model = model_formatter(s3_utils.LazyModel(model_name))
                        self.model_mapping[model_name] = {
                            'model': model,
                            'description': s3_utils.get_description(model_name)
                        }
                        logger.info(
                            f'Loaded models: {list(self.model_mapping)}'
                        )
                    except Exception as e:
                        logger.error(
                            f'Unable to load model {model_name}: {str(e)}'
                        )

            model = self.model_mapping[model_name]['model']
            output = model(request['text'])
            output = sorted(output, key=lambda i: i['score'], reverse=True)
            output = filter_min_confidence(output, request['min_confidence'])
            output = filter_max_classes(output, request['max_classes'])
            outputs.append({'type': model_name, 'result': output})
        response = {
            'text': request['text'],
            'classes': outputs,
        }

        logger.info(f"text hash: {hashlib.sha256(response['text'].encode()).hexdigest()}")

        logger.info(f'st: {request_in_time}, en: {datetime.now()}, '\
             f'dur: {(datetime.now() - request_in_time).total_seconds()*1000}ms')

        logger.info(f'Classes detected: {response["classes"]}')

        return response
