from flask_restx import fields


def get_services_put_body(api):
    """
    Registers a model to the input api and returns the model

    The model is for the body of a PUT to /services/

    Example:
    {
        "url": "http://somewhere.org/classes/",
        "route": "classes",  <-- NOTE this refers to the ds_gateway route
        "models": [
            {
                "id": "fake_classify",
                "description": "A fake model that randomly returns classes",
            },
        ]
    }

    Args:
        api (flask_restx.api): The api that will handle the request

    Returns:
        flask_restx.model: The model registered to the api
    """
    services_put_body = api.model(
        'services_put_body',
        {
            "url": fields.String(
                description="http://somewhere.org/classes/",
                example="classes",
            ),
            "route": fields.String(
                description="The route served by the worker",
                example="classes",
            ),
            "models": fields.List(
                fields.Nested(
                    api.model(
                        'models_desc_request',
                        {
                            "id": fields.String(
                                description="Unique identifier for model",
                                example="en_core_web_intent_2020-03-15",
                            ),
                            "description": fields.String(
                                description="A brief description of the model",
                                example="An intent classification model trained on common crawl",
                            ),
                        }
                    )
                ),
            ),
        }
    )
    return services_put_body
