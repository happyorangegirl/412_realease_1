from rest_utilities import (VRARestEx, VROApiExtension)
from validation_controllers import ValidationController
from validators import (ValidatorBase, VROActionValidator, VROAPIValidator, VRARestValidator)
from validation_fixtures import (ValidationFixtureBase)

import logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Set default logging handler to avoid "No handler found" warnings.
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass