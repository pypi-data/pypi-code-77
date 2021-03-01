from requests_futures.sessions import FuturesSession

from google.protobuf.json_format import MessageToDict

from arize.bounded_executor import BoundedExecutor
from arize.types import ModelTypes
from arize.model import (
    Prediction,
    Actual,
    FeatureImportances,
    BulkPrediction,
    BulkActual,
    BulkFeatureImportances,
)
from arize.__init__ import __version__


class Client:
    """
    Arize API Client to report model predictions and actuals to Arize AI platform
    """

    def __init__(
        self,
        api_key: str,
        organization_key: str,
        uri="https://api.arize.com/v1",
        max_workers=8,
        max_queue_bound=5000,
        retry_attempts=3,
        timeout=200,
    ):
        """
        :params api_key: (str) api key associated with your account with Arize AI
        :params organization_key: (str) organization key in Arize AI
        :params max_workers: (int) number of max concurrent requests to Arize. Default: 20
        :max_queue_bound: (int) number of maximum concurrent future objects being generated for publishing to Arize. Default: 5000
        """
        self._retry_attempts = retry_attempts
        self._uri = uri + "/log"
        self._bulk_url = uri + "/bulk"
        self._api_key = api_key
        self._organization_key = organization_key
        self._timeout = timeout
        self._session = FuturesSession(
            executor=BoundedExecutor(max_queue_bound, max_workers)
        )

    def log_prediction(
        self,
        model_id: str,
        model_type: ModelTypes,
        model_version: str,
        prediction_id: str,
        prediction_label,
        prediction_score=None,
        features=None,
        time_overwrite=None,
    ):
        """Logs a prediction to Arize via a POST request. Returns :class:`Future` object.
        :param model_id: (str) Unique identifier for a given model
        :param model_type: (ModelTypes) Declares what model type this prediction is for. Binary, Numeric, Categorical, Score_Categorcal.
        :param model_version: (str) Field used to group together a subset of predictions and actuals for a given model_id.
        :param prediction_id: (str) Unique string identifier for a specific prediction. This value is used to match a prediction to an actual label in the Arize platform.
        :param prediction_label: (one of bool, str, float, int) The predicted value for a given model input.
        :param prediction_score: (float) Optional predicted score for the predicted_label of classification model. If present, the prediction_label must be of type str.
        :param features: (str, <value>) Optional dictionary containing human readable and debuggable model features. Keys must be str, values one of str, bool, float, long.
        :param time_overwrite: (int) Optional field with unix epoch time in seconds to overwrite timestamp for prediction. If None, prediction uses current timestamp.
        :rtype : concurrent.futures.Future
        """

        pred = Prediction(
            organization_key=self._organization_key,
            prediction_id=prediction_id,
            model_id=model_id,
            model_type=model_type,
            model_version=model_version,
            prediction_label=prediction_label,
            prediction_score=prediction_score,
            features=features,
            time_overwrite=time_overwrite,
        )
        pred.validate_inputs()
        return self._post(record=pred._build_proto(), uri=self._uri, indexes=None)

    def log_actual(
        self, model_id: str, model_type: ModelTypes, prediction_id: str, actual_label
    ):
        """Logs an actual to Arize via a POST request. Returns :class:`Future` object.
        :param model_id: (str) Unique identifier for a given model
        :param model_type: (ModelTypes) Declares what model type this prediction is for. Binary, Numeric, Categorical, Score_Categorcal.
        :param prediction_id: (str) Unique string identifier for a specific prediction. This value is used to match a prediction to an actual label in the Arize platform.
        :param actual_label: (one of bool, str, float, int) The actual true value for a given model input. This actual will be matched to the prediction with the same prediction_id as the one in this call.
        :rtype : concurrent.futures.Future
        """
        actual = Actual(
            organization_key=self._organization_key,
            model_id=model_id,
            model_type=model_type,
            prediction_id=prediction_id,
            actual_label=actual_label,
        )
        actual.validate_inputs()
        return self._post(record=actual._build_proto(), uri=self._uri, indexes=None)

    def log_shap_values(
        self,
        model_id: str,
        prediction_id: str,
        shap_values: {},
    ):
        """Logs SHAP feature importance values for a given prediction to Arize via a POST request. Returns :class:`Future` object.
        :param model_id: (str) Unique identifier for a given model.
        :param prediction_id: (str) Unique string identifier for a specific prediction. This value is used to match a prediction to the SHAP values supplied in this request in the Arize platform.
        :param shap_values: (str, float) Dictionary containing human readable and debuggable model features keys, along with SHAP feature importance values. Keys must be str, while values must be float.
        :rtype : concurrent.futures.Future
        """

        fi = FeatureImportances(
            organization_key=self._organization_key,
            prediction_id=prediction_id,
            model_id=model_id,
            feature_importances=shap_values,
        )
        fi.validate_inputs()
        return self._post(record=fi._build_proto(), uri=self._uri, indexes=None)

    def log_bulk_shap_values(self, model_id: str, prediction_ids, shap_values):
        """Logs a collection of SHAP feature importance value sets with Arize via a POST request. Returns list<:class:`Future`> object.
        :param model_id: (str) Unique identifier for a given model
        :param prediction_ids: 1-D Pandas Dataframe or Series with string elements. Each element corresponding to a unique string identifier for a specific prediction. Each element corresponds to the SHAP values of the same index.
        :param shap_values: 1-D Pandas Dataframe or Series. The SHAP value sets for a set of predictions. SHAP value sets are correspond to the prediction ids with the same index.
        :rtype : list<concurrent.futures.Future>
        """

        feature_importances = BulkFeatureImportances(
            organization_key=self._organization_key,
            model_id=model_id,
            prediction_ids=prediction_ids,
            feature_importances=shap_values,
        )
        feature_importances.validate_inputs()
        return self._post_bulk(
            records=feature_importances._build_proto(), uri=self._bulk_url
        )

    def log_bulk_predictions(
        self,
        model_id: str,
        model_version: str,
        model_type: ModelTypes,
        prediction_ids,
        prediction_labels,
        prediction_scores=None,
        features=None,
        feature_names_overwrite=None,
        time_overwrite=None,
    ):
        """Logs a collection of predictions with Arize via a POST request. Returns list<:class:`Future`> object.
        :param model_id: (str) Unique identifier for a given model
        :param model_type: (ModelTypes) Declares what model type this prediction is for. Binary, Numeric, Categorical, Score_Categorcal.
        :param model_version: (str) Field used to group together a subset of predictions and actuals for a given model_id.
        :param prediction_ids: 1-D Pandas Dataframe or Series with string elements. Each element corresponding to a unique string identifier for a specific prediction. These values are needed to match latent actual labels to their original prediction labels. Each element corresponds to feature values of the same index.
        :param prediction_labels: 1-D Pandas Dataframe or Series. The predicted values for a given model input. Values are associates to the ids in the same index.
        :param prediction_scores: 1-D Pandas Dataframe or Series. The predicted scores for the corresponding predicted_label of classification model. If present, elements in prediction_labels must be of type str. Values are associates to the labels in the same index.
        :param features: Optional 2-D Pandas Dataframe containing human readable and debuggable model features. Dataframes columns (df.columns) should contain feature names and must have same number of rows as prediction_ids and prediction_labels. N.B. np.nan values are stripped from the record and manifest on our platform as a missing value (not 0.0 or NaN)
        :param feature_names_overwrite: Optional list<str> that if present will overwrite features.columns values. Must contain the same number of elements as features.columns.
        :param time_overwrite: (list<int>) Optional list with same number of elements as prediction_labels field with unix epoch time in seconds to overwrite timestamp for each prediction. If None, prediction uses current timestamp.
        :rtype : list<concurrent.futures.Future>
        """
        preds = BulkPrediction(
            organization_key=self._organization_key,
            model_id=model_id,
            model_type=model_type,
            model_version=model_version,
            prediction_ids=prediction_ids,
            prediction_labels=prediction_labels,
            prediction_scores=prediction_scores,
            features=features,
            feature_names_overwrite=feature_names_overwrite,
            time_overwrite=time_overwrite,
        )
        preds.validate_inputs()
        return self._post_bulk(records=preds._build_proto(), uri=self._bulk_url)

    def log_bulk_actuals(
        self, model_id: str, model_type: ModelTypes, prediction_ids, actual_labels
    ):
        """Logs a collection of actuals with Arize via a POST request. Returns list<:class:`Future`> object.
        :param model_id: (str) Unique identifier for a given model
        :param model_type: (ModelTypes) Declares what model type this prediction is for. Binary, Numeric, Categorical, Score_Categorcal.
        :param prediction_ids: 1-D Pandas Dataframe or Series with string elements. Each element corresponding to a unique string identifier for a specific prediction. These values are needed to match latent actual labels to their original prediction labels. Each element corresponds to feature values of the same index.
        :param actual_labels: 1-D Pandas Dataframe or Series. The actual true values for a given model input. Values are associates to the labels in the same index.
        :rtype : list<concurrent.futures.Future>
        """
        actuals = BulkActual(
            organization_key=self._organization_key,
            model_id=model_id,
            model_type=model_type,
            prediction_ids=prediction_ids,
            actual_labels=actual_labels,
        )
        actuals.validate_inputs()
        return self._post_bulk(records=actuals._build_proto(), uri=self._bulk_url)

    def _post_bulk(self, records, uri):
        return [self._post(r, uri, k) for k, r in records.items()]

    def _post(self, record, uri, indexes):
        payload = MessageToDict(message=record, preserving_proto_field_name=True)
        resp = self._session.post(
            uri,
            headers={
                "Authorization": self._api_key,
                "Grpc-Metadata-sdk-version": __version__,
                "Grpc-Metadata-sdk": "py",
            },
            timeout=self._timeout,
            json=payload,
        )
        if indexes is not None and len(indexes) == 2:
            resp.starting_index = indexes[0]
            resp.ending_index = indexes[1]
        return resp
