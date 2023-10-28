from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from app.Controller.auth_forms import ProfRegistration, StudentRegistration, LoginForm
from app.Model.models import Professor, Student, User
from config import Config
from flask_login import current_user, login_user, login_required, logout_user

from app import db

bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER 

# @bp_auth.route('/register', methods=['GET', 'POST'])
# def register():

@bp_auth.route('/registerprof', methods=['GET','POST'])
def registerprof():
    rpform = ProfRegistration()
    if rpform.validate_on_submit():
        prof = Professor(username=rpform.username.data, email=rpform.email.data, first_name=rpform.first_name.data, last_name=rpform.last_name.data,
                         phone_number=rpform.phone.data, user_type = "Professor")
        prof.set_password(rpform.password.data)
        db.session.add(prof)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('routes.index'))
    return render_template('registerProf.html', form = rpform)

@bp_auth.route('/registerstudent', methods=['GET','POST'])
def registerstudent():
    spform = StudentRegistration()
    if spform.validate_on_submit():
        stu = Student(username=spform.username.data, email=spform.email.data, first_name=spform.first_name.data, last_name=spform.last_name.data,
                      student_id=spform.student_id.data, majors=spform.majors.data, programming_languages=spform.languages.data,
                      phone_number=spform.phone.data, gpa=spform.gpa.data,graduation_date=spform.graduation_date.data,
                      research_history=spform.research_history.data, user_type = "Student")
        stu.set_password(spform.password.data)
        db.session.add(stu)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('routes.index'))
    return render_template('registerStudent.html', form = spform)

@bp_auth.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    lform = LoginForm()
    if lform.validate_on_submit():
        user = User.query.filter_by(username = lform.username.data).first()
        if (user is None) or (user.check_password(lform.password.data)==False):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember = lform.remember_me.data)
        return redirect(url_for('routes.index'))
    return render_template('login.html', form =lform )

@bp_auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))