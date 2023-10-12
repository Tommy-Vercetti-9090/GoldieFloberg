from flask import request, current_app
from bson.objectid import ObjectId
from utils.response import CustomErrorHandler, CustomSuccessHandler
from src.model.profile_model import Profile
from utils.validators.profile_validation import CreateProfile


def create_profile():
    data = request.json
    print('dataaaa', data)
    try:
        app = current_app
        profile_schema = CreateProfile()
        data = profile_schema.load(data)
        data.update({
            "user_id": request.user_id,
            "createdAt": ObjectId().generation_time,
            "updatedAt": ObjectId().generation_time,
        })
        Profile(data)()
        profile_id = (
            app.db["Profile"]
            .insert_one(
                data
            )
            .inserted_id
        )
        profile = list(app.db["Profile"]
                       .aggregate([
                           {
                               "$match": {
                                   "_id": profile_id
                               }
                           },
                           {
                               "$lookup": {
                                   "from": "User",
                                   "localField": "user_id",
                                   "foreignField": "_id",
                                   "as": "user",
                               },
                           },
                           {
                               "$unwind": {
                                   "path": "$user"
                               }
                           },
                           {
                               "$project": {
                                   "name": 1,
                                   "phone": 1,
                                   "dob": 1,
                                   "preferred_name": 1,
                                   "user": {
                                       "_id": 1,
                                       "email": 1,
                                       "user_type": 1,
                                   },
                               }
                           }
                       ])
                       )[0]
        app.db["User"].update_one({
            "_id": request.user_id,
        },
            {
            "$set": {
                "is_profile_completed": True
            }
        }
        )

        return CustomSuccessHandler(profile, "Profile created Successfully", 200)
    except Exception as e:
        return CustomErrorHandler({"message": "Profile already created"}, 500)\
            if e.code == 11000 else CustomErrorHandler(e.args[0], 500)
