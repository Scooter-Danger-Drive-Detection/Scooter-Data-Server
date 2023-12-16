from flask import Flask, render_template, redirect, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import DataBase

app = Flask(__name__)
app.config['SECRET_KEY'] = '>#s!-R>yAI0M4%dpsQQ>6(!h{ljfIsdPBk`}82[,z|7:SOOHn<^yj6R@xH*fRj@'
login_manager = LoginManager()
login_manager.init_app(app)

database = DataBase()
