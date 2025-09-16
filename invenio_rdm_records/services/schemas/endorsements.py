# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
# Copyright (C) 2023 TU Wien.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Schema for record endorsements."""

from marshmallow import Schema, fields, validate, EXCLUDE
from marshmallow.fields import URL
from marshmallow_utils.fields import EDTFDateTimeString, SanitizedUnicode


class ActorItemSchema(Schema):
    """Schema for actor item details (endorsements and reviews)."""
    created = EDTFDateTimeString(dump_only=True)
    url = URL(dump_only=True)
    index = fields.Integer(dump_only=True)


class EndorsementSchema(Schema):
    """Schema for endorsements."""

    class Meta:
        """Meta attributes for the schema."""

        unknown = EXCLUDE

    actor_id = fields.Integer(required=True)
    review_count = fields.Integer()
    actor_name = SanitizedUnicode(required=True)
    endorsement_list = fields.List(fields.Nested(ActorItemSchema), required=True)
    endorsement_count = fields.Integer(validate=validate.Range(min=0))
    review_list = fields.List(fields.Nested(ActorItemSchema), required=True)
