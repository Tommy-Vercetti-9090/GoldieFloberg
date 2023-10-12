from flask import Blueprint
from .handler import create_profile
from src.middleware.check_auth import check_auth

create_profile_route = Blueprint(
    'CREATE-PROFILE', __name__, url_prefix="/user")
create_profile_route.before_request(check_auth)
create_profile_route.route('/create-profile', methods=['POST'])(create_profile)
