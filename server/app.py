from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource, abort

from models import db, Guest, Episode, Appearance

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Home(Resource):
    
    def get(self):
        return {"message": "Welcome to the Guest Appearances API!"}, 200
    


# Get Episodes
class Episodes(Resource):
    
    def get(self):
        episodes = Episode.query.all()
        
        response_dict_list = [ 
            {
                "id": episode.id,
                "date": episode.date,
                "number": episode.number
                } for episode in episodes]
        
        response = make_response(
            response_dict_list,
            200
        )
        
        return response
    
    
# Episode by id
class EpisodeById(Resource):
    def get(self, id):
        episode = Episode.query.filter_by(id=id).first()
        
        if episode:
            response = make_response(episode.to_dict(), 200)
        else:
            response = make_response("Episode not found", 404)
            
        return response
    
    
# Get Guests
class Guests(Resource):
    def get(self):
        guests = Guest.query.all()
        
        response_dict_list = [ 
            {
                "id": guest.id,
                "name": guest.name,
                "occupation": guest.occupation
                } for guest in guests]
        
        response = make_response(
            response_dict_list,
            200
        )
        
        return response
    
# Post appearances
class PostAppearances(Resource):
    def post(self):
        # new_appearance = Appearance(
        #     rating=request.json.get('rating'),
        #     episode_id=request.json.get('episode_id'),
        #     guest_id=request.json.get('guest_id')
        # )
        
        # db.session.add(new_appearance)
        # db.session.commit()
        
        # response = make_response(new_appearance.to_dict(), 201)
        
        data = request.get_json()

        # Validate required fields
        rating = data.get("rating")
        episode_id = data.get("episode_id")
        guest_id = data.get("guest_id")

        errors = []
        if not (rating and episode_id and guest_id):
            errors.append("Missing required fields: rating, episode_id, guest_id")
        if rating is not None and (rating < 1 or rating > 5):
            errors.append("Rating must be between 1 and 5")

        # Check if the referenced Episode and Guest exist
        episode = Episode.query.get(episode_id)
        guest = Guest.query.get(guest_id)
        if not episode:
            errors.append("Episode not found")
        if not guest:
            errors.append("Guest not found")

        if errors:
            return make_response(jsonify({"errors": errors}), 400)

        # Create new Appearance if validation passes
        new_appearance = Appearance(
            rating=rating,
            episode_id=episode_id,
            guest_id=guest_id
        )
        db.session.add(new_appearance)
        db.session.commit()

        # Prepare response
        response_dict = {
            "id": new_appearance.id,
            "rating": new_appearance.rating,
            "guest_id": new_appearance.guest_id,
            "episode_id": new_appearance.episode_id,
            "episode": {
                "id": episode.id,
                "date": episode.date,
                "number": episode.number
            },
            "guest": {
                "id": guest.id,
                "name": guest.name,
                "occupation": guest.occupation
            }
        }

        return make_response(jsonify(response_dict), 201)
    
    
api.add_resource(Home, '/')
api.add_resource(Episodes, '/episodes')
api.add_resource(EpisodeById, '/episodes/<int:id>')
api.add_resource(Guests, '/guests')
api.add_resource(PostAppearances, '/appearances')

if __name__ == '__main__':
    app.run(port=5555, debug=True)