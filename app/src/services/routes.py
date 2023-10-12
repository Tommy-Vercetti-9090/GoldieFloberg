from .Auth.router import (
    signup_route,
    otp_verify_route,
    login_route
)
from .Profile.router import (
    create_profile_route
)


async def register_endpoints(app):
    # AUTH
    app.register_blueprint(signup_route)
    app.register_blueprint(login_route)
    app.register_blueprint(otp_verify_route)

    # PROFILE
    app.register_blueprint(create_profile_route)
