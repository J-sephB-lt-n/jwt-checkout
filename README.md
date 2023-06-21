# Checking out JSON Web Tokens (JWTs)

Me investigating how JSON Web Tokens (JWTs) work using a bare-bones python [Flask](https://github.com/pallets/flask) app and [PyJWT](https://github.com/jpadilla/pyjwt)

For an introduction to the theory of JWTs, you can't do better than https://jwt.io

To deploy my app locally, run this code in terminal:

```bash
flask --app jwt_checkout run
```

Then, you can interact with the deployed app using commands in your browser:

**log in with incorrect password**:
    
        http://localhost:5000/login?username=joe&password=incorrectpassword&lifetime=30

**log in with correct credentials (this will save a JWT to your browser cookies, with token expiration controlled by parameter 'lifetime')**:
    
        http://localhost:5000/login?username=joe&password=secure1234&lifetime=30

**check status of the current token in your browser cookies**:
    
        http://localhost:5000/token_status

# Notes 

The layout (folder structure) of this project I took from https://flask.palletsprojects.com/en/2.3.x/patterns/packages/