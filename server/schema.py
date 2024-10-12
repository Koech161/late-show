from marshmallow import fields, Schema


class GuestSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    occupation = fields.Str(required=True) 

class EpisodeSchema(Schema):
    id = fields.Int(required=True)
    date = fields.DateTime(required=True)
    number = fields.Int(required=True)

class AppearanceSchema(Schema):
    id = fields.Int(dump_only=True)
    rating = fields.Int(required=True)
    episode_id = fields.Int(required=True)
    guest_id = fields.Int(required=True)

    episode = fields.Nested(EpisodeSchema, only=('date','id', 'number'), dump_only=True)
    guest= fields.Nested(GuestSchema, only=('id', 'name', 'occupation'), dump_only=True)

class EpisodesDetails(Schema):
    id =fields.Int(required=True)
    date = fields.DateTime(required=True)
    number = fields.Int(required=True)
    appearance = fields.List(fields.Nested(AppearanceSchema, only=('episode_id', 'guest', 'guest_id', 'id', 'rating')))   