from flask import Blueprint

from src.middleware.check_bearer import check_bearer

signup_route = Blueprint('CREATE USER', __name__ , url_prefix= "/auth")
signup_route.before_request(check_bearer)
signup_route.route('/create', methods=['POST'])(sign_up)