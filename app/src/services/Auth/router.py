from flask import Blueprint
from .handler import sign_up
from src.middleware.check_bearer import check_bearer

signup_route = Blueprint('CREATE USER', __name__, url_prefix="/auth")
signup_route.before_request(check_bearer)
signup_route.route('/signup', methods=['POST'])(sign_up)
