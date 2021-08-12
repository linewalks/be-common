from flask import Blueprint

auth_bp = Blueprint("cdm", __name__, url_prefix="/cdm_api")

API_CATEGORY = "Cdm"

from main.controllers.cdm.person import *
from main.controllers.cdm.visit import *
from main.controllers.cdm.concept import *
from main.controllers.cdm.search import *
