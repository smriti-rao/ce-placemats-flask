import logging
from collections import namedtuple
from typing import List

logger = logging.getLogger(__name__)

WidgetSpec = namedtuple('WidgetSpec',
                        ['spec_type', 'widget_type', 'name', 'description', 'arguments', 'idempotency_key'])


def widget_specs_for_term(term) -> List[WidgetSpec]:  # TODO use real data
    return [WidgetSpec('author_adjacency', 'adj_matrix', 'my name', 'my desc', [1, 2, 3], term + 'A')]


def widget_spec(spec_type, widget_type, options=None) -> WidgetSpec:
    raise NotImplementedError()
