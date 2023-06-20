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
                "iss": username,
                "exp": (
                    datetime.datetime.now(tz=datetime.timezone.utc)
                    + datetime.timedelta(seconds=token_lifetime)
                ),
            },
            JWT_SECRET_KEY,
            algorithm="HS256",
        )
        decoded_token = jwt.decode(encoded_token, JWT_SECRET_KEY, algorithms=["HS256"])
        return (
            f"""
Correct credentials passed <br>
<br>
-- system state -- <br>
current token:                          {encoded_token} <br>
current token (decoded):                {decoded_token} <br>
number of seconds before token expires: {(decoded_token["exp"]-int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())):,.0f} <br>
        """,
            200,
        )
    return (
        f"""
INCORRECT credentials supplied. Access denied. <br>
""",
        403,
    )


@app.route("/token_status", methods=["GET"])
def token_status():
    token_str: str = flask.request.args.get("token")
    try:
        decoded_token = jwt.decode(token_str, JWT_SECRET_KEY, algorithms=["HS256"])
        return (
            f"""
Token is valid <br>
<br>
-- system state -- <br>
current token:                          {token_str} <br>
current token (decoded):                {decoded_token} <br>
number of seconds before token expires: {(decoded_token["exp"]-int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())):,.0f} <br>
        """,
            200,
        )
    except Exception as e:
        return (
            f"""
Token is INVALID - access denied <br>
<br>
Token error is: "{e}"        
""",
            403,
        )
