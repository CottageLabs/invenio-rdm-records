# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 TU Wien.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Search dumpers for access-control information."""

from invenio_records.dictutils import parse_lookup_key
from invenio_records.dumpers import SearchDumperExt

from invenio_notify.proxies import current_endorsement_service


class EndorsementsDumperExt(SearchDumperExt):
    """Search dumper extension for Notify endorsements.

    A pattern replicated from the StatisticsDumperExt, this dumper looks up endorsements
    for a record and dumps them into a field so that they are indexed in the search engine.
    """

    def __init__(self, target_field):
        """Constructor.

        :param target_field: dot separated path where to dump the tokens.
        """
        super().__init__()
        self.keys = parse_lookup_key(target_field)
        self.key = self.keys[-1]

    def dump(self, record, data):
        """Dump the endorsements to the data dictionary."""
        if record.is_draft:
            return

        endorsements = current_endorsement_service.get_endorsement_info(record.id)
        data[self.key] = endorsements

    def load(self, data, record_cls):
        """Keep the download & view endorsements in the data dictionary.

        This is relevant for the "EndorsementField" system field,
        which uses this entry in the record's data.
        """
        pass
