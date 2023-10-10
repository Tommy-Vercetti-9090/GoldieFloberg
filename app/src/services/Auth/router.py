from flask import Blueprint

signup_route = Blueprint('CREATE USER', __name__ , url_prefix= "/auth")
# signup_route.before_request(check_bearer)
# signup_route.route('/create', methods=['POST'])(create)