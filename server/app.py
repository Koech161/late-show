from flask import Flask, request,  make_response
from flask_migrate import Migrate
from utilis import db
from models.episode import Episode
from models.appearance import Appearance
from models.guest import Guest
from flask_restful import Api, Resource
from schema import GuestSchema
from schema import AppearanceSchema
from schema import EpisodeSchema
from schema import EpisodesDetails
from marshmallow import ValidationError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


migrate = Migrate(app, db)
db.init_app(app)
api=Api(app)
# instanciate schemas
guest_schema = GuestSchema()
episode_schema = EpisodeSchema()
appearance_schema = AppearanceSchema()
guests_schema = GuestSchema(many=True)
episodes_schema = EpisodeSchema(many=True)
episode_details = EpisodesDetails()

class Episodes(Resource):
    def get(self):
        episodes = Episode.query.all()
        if episodes:

            return make_response(episodes_schema.dump(episodes),200)
        else:
            return {'error': 'Episodes not found.'},404
        
class EpisodeByID(Resource): 
   
    def get(self,id):
        episode = Episode.query.get(id)

        if episode:
            return make_response(episode_details.dump(episode), 200)
        
        else:
            return {'error': 'Episode not found'}, 204
        
    def delete(self, id):
        episode = Episode.query.get(id)
        if episode:
            try:
                db.session.delete(episode) 
                db.session.commit()
                return {'message': 'Episode deleted successfuly'},204
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)},500
        else:
            return  {'error': 'Episode not found'}, 404

        
class Guests(Resource):
    def get(self):
        guests = Guest.query.all()
        if guests:
            return make_response(guests_schema.dump(guests))
        else:
            return {'error': 'Guests not found'}, 204

class Appearances(Resource):
    def post(self):
        json = request.json
        try: 
            validated_appearance = appearance_schema.load(json)
        except ValidationError as e:
            return {'errors': e.messages}, 400
        episode = Episode.query.get(validated_appearance['episode_id'])
        guest = Guest.query.get(validated_appearance['guest_id'])
        if not episode or not guest:
            return {'error': 'Episode or Guest not found'}, 404
        appearance  = Appearance(
            rating = validated_appearance['rating'],
            episode_id = validated_appearance['episode_id'],
            guest_id = validated_appearance['guest_id']
        )    
        try:
            db.session.add(appearance)  
            db.session.commit()
            
        
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500           
        response_data = appearance_schema.dump(appearance)
        response_data['episode'] = {
            'date': episode.date.strftime('%m/%d/%y'),
            'id': episode.id,
            'number': episode.number
        }
        response_data['guest'] = {
            'id': guest.id,
            'name': guest.name,
            'occupation': guest.occupation
        }
        return response_data, 201
api.add_resource(Episodes, '/episodes')
api.add_resource(EpisodeByID, '/episodes/<int:id>')
api.add_resource(Guests, '/guests')
api.add_resource(Appearances, '/appearances') 
if __name__ == '__main__':
    app.run(port=5555,debug=True)


