import logging
import os
import app.placemats.data.ncbi_client as ncbi
from app.placemats.util import kwargs_from_environ
from app.placemats.consumer.consumer import BaseConsumer
from app.placemats.stores.task_queue_config import widgets_task_queue
import time

logger = logging.getLogger(__name__)


class WidgetsTaskConsumer(BaseConsumer):

    def __init__(self) -> None:
        super().__init__(widgets_task_queue())

    def consume_one(self, task_info: dict):
        pass


if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    ncbi.configure_client(**kwargs_from_environ({
        'NCBI_EMAIL': 'email',
        'NCBI_API_KEY': 'api_key',
    }))
    while True:
        try:
            WidgetsTaskConsumer().consume_forever()
        except KeyboardInterrupt:
            logger.info('Ctrl-C received. Exiting...')
            break
        except:
            logger.error('Error while running consumer forever. Sleeping and will try again.')
            time.sleep(10)
            continue
