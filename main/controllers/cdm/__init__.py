# from flask import Blueprint

# cdm_bp = Blueprint("cdm", __name__, url_prefix="/cdm_api")

# API_CATEGORY = "Cdm"

# swagger에서 Cdm 하나만 보이는게 불편하다.
# 분리하는게 나을 것 같다.

from main.controllers.cdm.person import person_bp
from main.controllers.cdm.visit import visit_bp
from main.controllers.cdm.concept import *
from main.controllers.cdm.search import *

cdm_bp = [person_bp, visit_bp]
