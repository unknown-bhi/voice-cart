from app.core.config import settings
from livekit import api
from datetime import timedelta


def generate_livekit_token(user_id : str, room_name :str):

    token = api.AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)

    token.with_identity(user_id).with_ttl(timedelta(minutes=15)).with_name(user_id)

    token.with_grants(api.VideoGrants(
        room_join=True,
        room =room_name,
        can_publish=True,
        can_subscribe=True,
    
        
    ))
    jwt_token =token.to_jwt()

    return jwt_token