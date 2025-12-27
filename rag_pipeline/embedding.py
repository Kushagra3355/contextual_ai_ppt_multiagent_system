from app.dependencies import embed_model as embed_model_factory


def get_embedding_function():
    return embed_model_factory()
