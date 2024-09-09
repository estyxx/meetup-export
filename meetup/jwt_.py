import datetime
from pathlib import Path
from typing import Any

import jwt
import requests

from .env import Env


def generate_jwt(env: Env) -> str:
    payload = {
        "sub": env.MEETUP_COM_AUTHORIZED_MEMBER_ID,
        "iss": env.MEETUP_COM_CLIENT_KEY,
        "aud": "api.meetup.com",
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=1200),
    }

    headers = {
        "kid": env.MEETUP_COM_SIGNING_KEY_ID,
        "typ": "JWT",
        "alg": "RS256",
    }

    private_key = Path(env.MEETUP_COM_PRIVATE_KEY_PATH).read_text()

    token = jwt.encode(payload, private_key, algorithm="RS256", headers=headers)
    return token


def request_access_token(jwt_token: str, env: Env) -> dict[str, Any]:
    url = "https://secure.meetup.com/oauth2/access"

    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt_token,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(
        url,
        data=data,
        headers=headers,
        auth=(env.MEETUP_COM_CLIENT_KEY, env.MEETUP_COM_SECRET),
    )

    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()

        json_response: dict[str, Any] = response.json()
        print(json_response)
        return json_response
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    return {}
