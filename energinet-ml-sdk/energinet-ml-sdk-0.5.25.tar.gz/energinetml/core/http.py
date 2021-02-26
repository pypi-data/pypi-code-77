import fastapi
import uvicorn

from energinetml.settings import PACKAGE_REQUIREMENT

from .predicting import PredictionController


def create_app(model, trained_model, model_version=None):
    """
    :param energinetml.Model model:
    :param energinetml.TrainedModel trained_model:
    :param typing.Optional[str] model_version:
    :rtype: fastapi.FastAPI
    """
    controller = PredictionController(
        model=model,
        trained_model=trained_model,
        model_version=model_version,
    )

    async def predict_http_endpoint(
            request: controller.request_model,
            response: fastapi.Response):
        """
        TODO Write me!
        TODO /docs not working?
        """
        response.headers['X-sdk-version'] = str(PACKAGE_REQUIREMENT)

        return controller.predict(request)

    # -- Setup app -----------------------------------------------------------

    app = fastapi.FastAPI(
        title=model.name,
        description=(
            'Model version %s' % model_version
            if model_version
            else None
        )
    )
    app.router.add_api_route(
        path='/predict',
        methods=['POST'],
        endpoint=predict_http_endpoint,
        response_model=controller.response_model,

        # TODO:
        summary='Predict using the model',
        description='TODO',
    )

    return app


def run_predict_api(model, trained_model, host, port, model_version=None):
    """
    :param energinetml.Model model:
    :param energinetml.TrainedModel trained_model:
    :param str host:
    :param int port:
    :param typing.Optional[str] model_version:
    """
    app = create_app(
        model=model,
        trained_model=trained_model,
        model_version=model_version,
    )

    uvicorn.run(app, host=host, port=port)
