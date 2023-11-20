from flask import Flask
from webui import webui_blueprint

app = Flask(__name__)
app.register_blueprint(webui_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
