# jwt-checkout

Me investigating how JSON-Web-Tokens (JWTs) work using a bare-bones Flask app

To deploy the app locally, run this code in terminal:

```bash
flask --app jwt_checkout run
```

Then, you can interact with the deployed app using commands in your browser:

log in with incorrect password:
    DEPLOYED_APP_ADDESS_HERE/login?username=joe&password=incorrectpassword&lifetime=30

log in with correct credentials (this will give you a JWT):
    DEPLOYED_APP_ADDESS_HERE/login?username=joe&password=secure1234&lifetime=45

check status of a given token:
    DEPLOYED_APP_ADDESS_HERE/token_status?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJqb2UiLCJleHAiOjE2ODcyNzM4Mzd9.HKKfEuK8Orn53ZEp-uQz8AmUW-g4QAoh5fC7DxlhLUE

# Notes 

The layout (folder structure) of this project I took from https://flask.palletsprojects.com/en/2.3.x/patterns/packages/