from flask import Flask
from views import views

app = Flask(__name__)
app.register_blueprint(views)
app.secret_key = ':LKJMWV(*$TH:KLN'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

