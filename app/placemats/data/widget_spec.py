import logging
from collections import namedtuple
from app.placemats.data.widget_spec_types import *
from typing import List

logger = logging.getLogger(__name__)

WidgetSpec = namedtuple('WidgetSpec',
                        ['spec_type', 'widget_type', 'name', 'description', 'arguments', 'idempotency_key'])


def widget_specs_for_term(term) -> List[WidgetSpec]:
    return [
        build_spec(AUTHOR_ADJACENCY,
                   'adj_matrix',
                   'Author collaborations surrounding "{}"'.format(term),
                   'Displays the top-100 (by number of publications) authors and shows the frequency of '
                   'collaboration for each pair.',
                   [term]),
    ]


def build_spec(spec_type, widget_type, name, description, arguments):
    idempotency_key = '_'.join([spec_type, widget_type, str(arguments)])
    return WidgetSpec(spec_type,
                      widget_type,
                      name,
                      description,
                      arguments,
                      idempotency_key)
