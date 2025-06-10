# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 TU Wien.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Cached transient field for record endorsements."""
from flask import current_app
from invenio_records.systemfields import SystemField
from invenio_search.proxies import current_search_client
from invenio_search.utils import build_alias_name


class EndorsementField(SystemField):
    """Field for lazy fetching and caching (but not storing) of record endorsements."""

    def _get_record_endorsements(self, record):
        """Get the record's endorsements from either record or aggregation index."""
        endorsements = None

        try:
            # note: this field is dumped into the record's data before indexing
            #       by the search dumper extension "EndorsementsDumperExt"
            res = current_search_client.get(
                index=build_alias_name(record.index._name),
                id=record.id,
                params={"_source_includes": "endorsements"},
            )
            endorsements = res["_source"]["endorsements"]
        except Exception:
            endorsements = None

        return endorsements

    #
    # Data descriptor methods (i.e. attribute access)
    #
    def __get__(self, record, owner=None):
        """Get the persistent identifier."""
        if record is None:
            # returns the field itself.
            return self

        endorsements = record.get("endorsements", None)
        if endorsements:
            return endorsements

        endorsements = self._get_record_endorsements(record)
        record["endorsements"] = endorsements

        return endorsements

    def pre_commit(self, record, **kwargs):
        """Ensure that the endorsements stay transient."""
        record.pop("endorsements", None)

    def pre_dump(self, record, data, **kwargs):
        """Do nothing in particular before a record is dumped."""
        # note: there's no pre/post-dump work being done in the system field because
        #       we only want the endorsements to be dumped into the search engine, which is
        #       done over at the "EndorsementsDumperExt" search dumper extension
        #       putting that logic here would require more research into when a
        #       system field's `pre_dump()` is called
        pass
