# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
# Copyright (C) 2023 TU Wien.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Schema for record endorsements."""

from marshmallow import Schema, fields

class EndorsementItemSchema(Schema):
    reviewer_id = fields.Int(required=True)
    reviewer_name = fields.Str(required=True)
    endorsement_count = fields.Int(required=True)
    review_count = fields.Int(required=True)
    endorsement_urls = fields.List(fields.Url(), required=True)

class EndorsementsSchema(Schema):
    endorsements = fields.List(fields.Nested(EndorsementItemSchema), required=True)
