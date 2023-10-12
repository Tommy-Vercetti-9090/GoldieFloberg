from flask import Blueprint
from .handler import user_signup, user_login, verify_otp
from src.middleware.check_bearer import check_bearer

signup_route = Blueprint('USER-SIGNUP', __name__, url_prefix="/auth")
signup_route.before_request(check_bearer)
signup_route.route('/signup', methods=['POST'])(user_signup)

otp_verify_route = Blueprint('VERIFY-OTP', __name__, url_prefix="/auth")
otp_verify_route.before_request(check_bearer)
otp_verify_route.route('/verify-otp', methods=['POST'])(verify_otp)


login_route = Blueprint('USER-LOGIN', __name__, url_prefix="/auth")
login_route.before_request(check_bearer)
signup_route.route('/login', methods=['POST'])(user_login)
