from flask_restx import fields


def get_classes_body(api):
    """
    Registers a model to the input api and returns the model

    The model is for the body of a POST to /classes/

    Example:
    {
        "text": "I wonder what this sentence is about",
        "classes": ["topic", "subtopic"],
        "min_confidence": 0.1,
        "max_classes": 3
    }

    Args:
        api (flask_restx.api): The api that will handle the request

    Returns:
        flask_restx.model: The model registered to the api
    """
    classes_body = {
        "text": fields.String(
            required=True,
            description="The text to be classified",
            example="I wonder what this sentence is about",
        ),
        "classes": fields.List(
            fields.String(
                example="intent"
            ),
            required=True,
            description="The type(s) of classification to be performed",
        ),
        "min_confidence": fields.Float(
            required=False,
            example=0.1,
            default=0,
        ),
        "max_classes": fields.Integer(
            required=False,
            example=3,
            default=10,
        ),
    }
    return api.model('classes_body', classes_body)


def get_classes_post_response(api):
    """
    Registers a model to the input api and returns the model

    The model is for the response of a POST to /classes/

    Example:
    {
        "classes": [
            {
                "type": "topic",
                "result": [
                    {
                        "value": "new",
                        "score": 0.75
                    }
                ]
            }
        ],
        "text": "I wonder what this sentence is about"
    }

    Args:
        api (flask_restx.api): The api that will handle the request
    Returns:
        flask_restx.model: The model registered to the api
    """
    classes_post_response = api.model(
        'classes_post_response',
        {
            "classes": fields.List(fields.Nested(
                api.model(
                    'classes_type_results',
                    {
                        "type": fields.String(
                            description="The class type",
                            example="intent",
                        ),
                        "result": fields.List(
                            fields.Nested(
                                api.model(
                                    'classes_result',
                                    {
                                        "value": fields.String(
                                            description="The class",
                                            example="new"
                                        ),
                                        "score": fields.Float(
                                            description="The confidence value for the class",
                                            example=0.75
                                        ),
                                    }
                                )
                            )
                        )
                    }
                )
            )),
            "text": fields.String(
                description="The text to be classified",
                example="I wonder what this sentence is about",
            ),
        }
    )
    return classes_post_response
