from flask import Flask
from webui import webui_blueprint
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(webui_blueprint)

# In order to make cross-origin requests -- i.e., requests that originate from a different protocol,
# IP address, domain name, or port -- you need to enable Cross Origin Resource Sharing (CORS).
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    app.run(debug=True)
