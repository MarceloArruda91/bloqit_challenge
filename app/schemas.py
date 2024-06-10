from marshmallow import Schema, fields, ValidationError
from app.models import RentSize, RentStatus, LockerStatus


def validate_rent_size(value):
    if value not in RentSize._value2member_map_:
        raise ValidationError("Invalid RentSize.")


def validate_rent_status(value):
    if value not in RentStatus._value2member_map_:
        raise ValidationError("Invalid RentStatus.")


def validate_locker_status(value):
    if value not in LockerStatus._value2member_map_:
        raise ValidationError("Invalid LockerStatus.")


class BloqSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    address = fields.Str(required=True)


class LockerSchema(Schema):
    id = fields.Str(dump_only=True)
    bloq_id = fields.Str(required=True)
    status = fields.Str(required=True, validate=validate_locker_status)
    is_occupied = fields.Bool(required=True)

class LockerSchemaPut(Schema):
    id = fields.Str(dump_only=True)
    bloq_id = fields.Str(dump_only=True)
    status = fields.Str(required=True, validate=validate_locker_status)
    is_occupied = fields.Bool(required=True)


class RentSchema(Schema):
    id = fields.Str(dump_only=True)
    locker_id = fields.Str(dump_only=True)
    weight = fields.Float(required=True)
    size = fields.Str(required=True, validate=validate_rent_size)
    status = fields.Str(required=True, validate=validate_rent_status)


class RentSchemaPut(Schema):
    id = fields.Str(required=True)
    status = fields.Str(required=True, validate=validate_rent_status)


class RentCreateSchema(Schema):
    weight = fields.Float(required=True)
    size = fields.Str(required=True, validate=validate_rent_size)
    locker_id = fields.Str(required=True)
    status = fields.Str(required=True, validate=validate_rent_status)
