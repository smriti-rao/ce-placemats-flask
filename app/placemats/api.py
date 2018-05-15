from flask.views import MethodView
from app.placemats.ncbi_client import egquery
import logging

logger = logging.getLogger(__name__)


class PlacematsApi(MethodView):
    """
    XXX: IGNORE THIS CLASS It's simply here for quick testing, and isn't used for the placemats API
    """
    def __init__(self) -> None:
        super().__init__()
        logger.info('in constructor')

    def get(self, search_terms=None):
        return egquery(term='orchid')
