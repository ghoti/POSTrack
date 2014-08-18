__author__ = 'ghoti'
from flask import Flask

app = Flask(__name__)

from postrack.views import index
from postrack.views import starbasedetail
from postrack.views import system