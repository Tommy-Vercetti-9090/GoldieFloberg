from .Auth.router import (
    signup_route,
    # otp_verify_route,
    # resend_otp_route,
    # login_route,
    # forget_pass_route,
    # reset_pass_route,
    # logout_route,
)

async def register_endpoints(app):
    ##AUTH
    app.register_blueprint(signup_route)

    ##PROFILE
    