from flask_restx import fields


def get_entities_body(api):
    """
    Registers a model to the input api and returns the model

    The model is for the body of a POST to /entities/

    Example:
    {
        "text": "A specific name like James could be an entity",
        "entities": ["name"],
        "min_confidence": 0.1,
        "min_length": 2
    }

    Args:
        api (flask_restx.api): The api that will handle the request

    Returns:
        flask_restx.model: The model registered to the api
    """
    entities_body = {
        "text": fields.String(
            required=True,
            description="The text from which entities will be extracted",
            example="A specific name like James could be an entity",
        ),
        "entities": fields.List(
            fields.String(
                example="name"
            ),
            required=True,
            description="The type(s) of entities to be detected",
        ),
        "min_confidence": fields.Float(
            required=False,
            description="The minimum acceptable level of confidence for entities",
            example=0.1,
            default=0,
        ),
        "min_length": fields.Integer(
            required=False,
            description="The minimum acceptable number of characters for returned entities",
            example=2,
            default=1,
        ),
    }
    return api.model('entities_body', entities_body)


def get_entities_post_response(api):
    """
    Registers a model to the input api and returns the model

    The model is for the response of a POST to /entities/

    Example:
    {
        "entities": [
            {
                "type": "name",
                "result": [
                    {
                        "value": "James",
                        "score": 0.75,
                        "start_char": 2,
                        "end_char": 9
                    }
                ]
            }
        ],
        "text": "A specific name like James could be an entity"
    }

    Args:
        api (flask_restx.api): The api that will handle the request
    Returns:
        flask_restx.model: The model registered to the api
    """
    entities_post_response = api.model(
        'entities_post_response',
        {
            "entities": fields.List(fields.Nested(
                api.model(
                    'entities_type_results',
                    {
                        "type": fields.String(
                            description="The entity type",
                            example="name",
                        ),
                        "result": fields.List(
                            fields.Nested(
                                api.model(
                                    'entities_result',
                                    {
                                        "value": fields.String(
                                            description="The entitity",
                                            example="James"
                                        ),
                                        "score": fields.Float(
                                            description="The confidence value for the entity",
                                            example=0.75,
                                        ),
                                        "start_char": fields.Integer(
                                            description="The character where an entity begins",
                                            example=2,
                                        ),
                                        "end_char": fields.Integer(
                                            description="The character where an entity ends",
                                            example=9,
                                        ),
                                    }
                                )
                            )
                        )
                    }
                )
            )),
            "text": fields.String(
                description="The text from which entities will be extracted",
                example="A specific name like James could be an entity",
            ),
        }
    )
    return entities_post_response
