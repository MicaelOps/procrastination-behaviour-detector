import numpy as np
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import pandas as pd
import model_loader

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123456@localhost:5432/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

APP_ENCODING = {'work': 0, 'chrome': 1, 'game': 2, 'social_media': 3, 'other': 4}

model = model_loader.loadModel()


class Base(DeclarativeBase):
    pass


database = SQLAlchemy(app, model_class=Base)


class User(database.Model):
    __tablename__ = "users"
    __table_args__ = {'autoload_with': engine}

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    password: Mapped[str]
    name: Mapped[str]


@app.route('/')
def hello_world():
    return ' This feature is not supported.'


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True)

    username = data['email']
    password = data['password']
    name = data['name']

    if not all([username, password, name]):
        return jsonify({"response": "NO"})

    try:
        user = User.query.filter_by(username=username).first()

        if user:
            return jsonify({"response": "NO"})

        user = User(username=username, name=name, password=password)
        database.session.add(user)
        database.session.commit()
        return jsonify({"response": "YES"})
    except Exception as e:
        database.session.rollback()
        return jsonify({"response": "NO"})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    username = data['email']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:
        return jsonify({"response": "NO"})

    return jsonify({"response": "YES"})


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)

    mouse_clicks = data['mouse_clicks']

    feedback_response = data['feedback_response']
    keys_pressed = data['keys_pressed']
    mouse_travel = data['mouse_travel']
    tabs_changed = data['tabs_changed']
    app_focus_type = data['app_focus_type']
    timestamp = data['timestamp']

    df = pd.DataFrame([{'mouse_clicks': mouse_clicks, 'timestamp': timestamp, 'feedback_response': feedback_response,
                        'keys_pressed': keys_pressed, 'mouse_travel': mouse_travel, 'tabs_changed': tabs_changed,
                        'app_focus_type': app_focus_type}])

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute

    columns = ['mouse_clicks', 'hour', 'minute', 'feedback_response', 'keys_pressed', 'mouse_travel', 'tabs_changed',
               'app_focus_type']
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    x = df[columns].astype(np.float32).to_numpy()

    prediction = model.predict_proba(x)[0][1]

    print('Probability:')
    print(prediction)

    if prediction > 0.7:
        return jsonify({"response": "YES"})
    else:
        return jsonify({"response": "NO"})


if __name__ == '__main__':
    with app.app_context():
        database.reflect()

    if model is not None:
        app.run()
