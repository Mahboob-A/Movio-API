import logging
import jwt

from django.conf import settings
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidSignatureError,
    InvalidTokenError,
)

logger = logging.getLogger(__name__)


class DecodeJWT:
    """Decode JWT Util Class"""

    def get_token(self, request) -> str:
        """Returns the JWT token from header"""

        auth_header = request.META.get("HTTP_AUTHORIZATION", None)

        if auth_header is None:
            return None
        parts = auth_header.split(" ")  # parts ["Bearer", 'token]
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None
        return parts[1]

    def decode_jwt(self, request) -> dict:
        """Decodes a JWT token and returns the payload as a dictionary.
        Args:
                token: The JWT token string.
        Return:
                A dictionary containing the decoded payload or None, detail and message if decoding fails.
        """
        try:

            token = self.get_token(request=request)
            if token is None:
                return (
                    None,
                    "jwt-header-malformed",
                    "The JWT Authorization Header is missing or header is malformed.",
                )

            jwt_signing_key = settings.JWT_SIGNING_KEY
            payload = jwt.decode(jwt=token, key=jwt_signing_key, algorithms=["HS256"])

            detail = "jwt-decode-success"
            message = "JWT Token is valid."

            return (
                payload,
                detail,
                message,
            )  # payload has additional user details. see Auth Service's CustomTokenObtainPairSerializer
        except ExpiredSignatureError as e:
            return (
                None,
                "jwt-signature-expired",
                "The JWT Signature is expired. Renew the JWT Token.",
            )
        except (DecodeError, InvalidSignatureError, InvalidTokenError) as e:
            return (None, "jwt-decode-error", "The JWT Token could not be verified")
        except Exception as e:
            return (
                None,
                "jwt-general-exception",
                "Some error occurred during decoding the JWT token.",
            )


jwt_decoder = DecodeJWT()
