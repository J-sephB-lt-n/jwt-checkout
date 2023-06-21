import datetime
import flask
import os
import jwt
from jwt_checkout import app

# in production, fetch secret key from environment #
JWT_SECRET_KEY = os.environ.get("SECRET_KEY", default="dev_secret_key")

# stop browser from caching the results of requests to this flask app #
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


@app.route("/login", methods=["GET"])
def login():
    username = flask.request.args.get("username")
    password = flask.request.args.get("password")
    token_lifetime = int(flask.request.args.get("lifetime"))

    if username == "joe" and password == "secure1234":
        encoded_token = jwt.encode(
            {
                "iss": "my_authorization_server_name",
                "sub": username,
                "exp": (
                    datetime.datetime.now(tz=datetime.timezone.utc)
                    + datetime.timedelta(seconds=token_lifetime)
                ),
                "roles": ["reader", "writer", "admin"],
            },
            JWT_SECRET_KEY,
            algorithm="HS256",
        )
        decoded_token = jwt.decode(encoded_token, JWT_SECRET_KEY, algorithms=["HS256"])
        response = flask.make_response()
        response.status_code = 200
        response.set_cookie(
            key="jwt_token",
            value=encoded_token,
            # also set secure=True if using https
        )
        response.response = f"""
Correct credentials passed <br>
Saved the following JSON-Web-Token (JWT) to browser cookies: <br>
<br>
Encoded token:                          {encoded_token} <br>
Decoded body of token:                  {decoded_token} <br>
number of seconds before token expires: {(decoded_token["exp"]-int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())):,.0f} <br>
        """
        return response

    return (
        f"""
INCORRECT credentials supplied. Access denied. <br>
""",
        403,
    )


@app.route("/token_status", methods=["GET"])
def token_status():
    encoded_token = flask.request.cookies.get("jwt_token")
    try:
        decoded_token = jwt.decode(encoded_token, JWT_SECRET_KEY, algorithms=["HS256"])
        return (
            f"""
JWT Token retrieved from cookies <br>
Token is valid <br>
<br>
Encoded token:                          {encoded_token} <br>
Decoded body of token:                  {decoded_token} <br>
number of seconds before token expires: {(decoded_token["exp"]-int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())):,.0f} <br>

        """,
            200,
        )
    except Exception as e:
        return (
            f"""
JWT Token retrieved from cookies <br>
Token is invalid <br>
ACCESS DENIED <br>
<br>
Token error is: "{e}"
""",
            403,
        )
