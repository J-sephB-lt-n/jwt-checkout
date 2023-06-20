import datetime
import flask
import random
import jwt
from jwt_checkout import app

JWT_SECRET_KEY = "my_precious"  # need to put this in .env or something
app.config[
    "SEND_FILE_MAX_AGE_DEFAULT"
] = 0  # stop browser from caching the results of requests to this flask app


@app.route("/login", methods=["GET"])
def login():
    username = flask.request.args.get("username")
    password = flask.request.args.get("password")
    token_lifetime = int(flask.request.args.get("lifetime"))

    if username == "joe" and password == "secure1234":
        encoded_token = jwt.encode(
            {
                "iss": "my_authorization_server",
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
JWT token saved to browser cookies <br>
<br>
-- system state -- <br>
current token:                          {encoded_token} <br>
current token (decoded):                {decoded_token} <br>
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
JWT Token retrieved from cookies: "{encoded_token}" <br>
Token is valid <br>
<br>
-- system state -- <br>
current token:                          {encoded_token} <br>
current token (decoded):                {decoded_token} <br>
number of seconds before token expires: {(decoded_token["exp"]-int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())):,.0f} <br>
        """,
            200,
        )
    except Exception as e:
        return (
            f"""
JWT Token retrieved from cookies: "{encoded_token}" <br>
Token is INVALID - access denied <br>

<br>
Token error is: "{e}"        
""",
            403,
        )
