from flask_pymongo import PyMongo
from apscheduler.schedulers.background import BackgroundScheduler

mongo = PyMongo()
scheduler = BackgroundScheduler()