from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file 
from flask_login import current_user, login_manager, login_required, login_user, logout_user 
from werkzeug.security import generate_password_hash, check_password_hash 
from website import DB 
from .models import * 
import os 
from werkzeug.utils import secure_filename 
from io import BytesIO

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('login.html')
