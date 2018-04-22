
class Login(Resource):
    #@app.route('/', methods=['POST'])
    def post(self):
        POST_USERNAME = request.authorization["username"]
        POST_PASSWORD = request.authorization["password"]
        if auth.login(POST_USERNAME, POST_PASSWORD):
            auth.update_user_login(POST_USERNAME)
            usr = user_connector.get_user(POST_USERNAME)

            return jsonify(
                status=200,
                message="User logged in.",
                auth_token=usr.generate_auth_token().decode('ascii') + ":unused"
            )
        else:

            return jsonify(
                status=400,
                message="User not logged in."
            )
    def get(self):
        return jsonify(
            status=200,
            message="You are at the homepage"
        )
