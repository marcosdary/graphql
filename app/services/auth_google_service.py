from authlib.integrations.starlette_client import OAuth

from app.core.config import settings

oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.CLIENT_GOOGLE_ID,
    client_secret=settings.CLIENT_GOOGLE_SECRET_ID,
    server_metadata_url=(
        settings.URL_GOOGLE_METADATA
    ),
    client_kwargs={
        "scope": "openid email profile"
    }
)