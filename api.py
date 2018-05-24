from flask import Blueprint
from flask_restful import Api
from control.movies_with_dynamodb import MoviesByYear

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route 
api.add_resource(MoviesByYear,'/movies',endpoint='movies')