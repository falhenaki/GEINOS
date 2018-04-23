from app.core.user import auth

def validateCreds(request):
    if request.authorization:
        if request.authorization["username"]:
            username = request.authorization["username"]
        if request.authorization["password"]:
            password = request.authorization["password"]
        else:
            password = ""
        return auth.login(username,password)