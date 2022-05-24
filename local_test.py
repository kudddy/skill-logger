from flask import Flask, request
from flask_json import FlaskJSON, as_json
from flask import abort
from plugins.inputer import inputter


class FlaskApp:
    def __init__(self):
        pass

    @staticmethod
    def create_flask_app():
        app = Flask(__name__)
        app.config['JSON_AS_ASCII'] = False

        # @as_json
        @app.route("/", methods=['POST'])
        def post():
            try:
                data = request.form if request.form else request.json
                res = inputter(data)
                if request.method == "POST":
                    return res
            except Exception as e:
                print(e)
                abort(404)

        @app.route("/health_status", methods=['GET'])
        def health():
            return "status ok"

        FlaskJSON(app)
        return app

    def run(self, host: str = '0.0.0.0', port: int = 8080):
        self.create_flask_app().run(host=host, port=port, debug=False)


app = FlaskApp()

app.run()
