from flask_restx import fields

def get_body(api):
    """
    Registers a model to the input api and returns the model

    Args:
        api (flask_restx.api): The api that will handle the request

    Returns:
        flask_restx.model: The model registered to the api
    """

    body = {
        "a": fields.String(
            required=True,
            description="First string",
            example="Example A",
        ),
        "b": fields.String(
            required=True,
            description="Second string",
            example="Example B",
        ),
        "c": fields.List(
            fields.String(
                example="x"
            ),
            required=True,
            description="List of types",
        ),
    }
    return api.model('body', body)

def get_post_response(api):
    """
    Registers a model to the input api and returns the model

    Args:
        api (flask_restx.api): The api that will handle the request
    Returns:
        flask_restx.model: The model registered to the api
    """
    post_response = api.model(
        'post_response',
        {
            "c": fields.List(fields.Nested(
                api.model(
                    'type_results',
                    {
                        "type": fields.String(
                            description="Type",
                            example="x",
                        ),
                        "result": fields.List(
                            fields.Nested(
                                api.model(
                                    'result',
                                    {
                                        "score": fields.Float(
                                            description="Score",
                                            example=0.75
                                        ),
                                    }
                                )
                            )
                        )
                    }
                )
            )),
            "a": fields.String(
                description="First string",
                example="Example A",
            ),
            "b": fields.String(
                description="Second string",
                example="Example B",
            ),
        }
    )
    return post_response
