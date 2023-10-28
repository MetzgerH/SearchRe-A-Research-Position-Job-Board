from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from app.Controller.forms import OpeningForm
from app.Model.models import Professor, Student, Opening
from config import Config
from flask_login import login_required, current_user

from app import db

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'

@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@login_required
@bp_routes.route('/createopening/', methods=['GET', 'POST'])
def createopening():
    if (current_user.is_anonymous) or (current_user.user_type != "Professor"):
        flash('Faculty only (no students)')
        return redirect(url_for('routes.index'))
    oform = OpeningForm()
    if oform.validate_on_submit():
        open = Opening(title =oform.title.data, description=oform.description.data, start=oform.start.data, end=oform.end.data,
                      time_commitment=oform.time_commitment.data)
        open.creator_id = current_user.id #I DONT KNOW WHY I GOTTA DO THIS BUT IT WORKS :)
        for major in oform.majors.data:
            open.majors.append(major)
        for lang in oform.languages.data:
            open.programming_languages.append(lang)
        db.session.add(open)
        db.session.commit()
        flash('Your opening has been posted')
        return redirect(url_for('routes.index'))
    return render_template('createOpening.html', form = oform)

@login_required
@bp_routes.route('/profile', methods=['GET', 'POST'])
def profile():
    if(current_user.user_type == 'Student'):
        return render_template('student_profile.html', student = current_user)
    if(current_user.user_type == 'Professor'):
        return render_template('professor_profile.html',professor = current_user)
    return redirect(url_for('routes.index'))

@login_required
@bp_routes.route('/myopenings/', methods=['GET'])
def myopenings():
    if (current_user.is_anonymous) or (current_user.user_type != "Professor"):
        flash('Faculty only (no students)')
        return redirect(url_for('routes.index'))
    myopen = db.session.query(Opening).filter_by(creator_id = current_user.id).all() #ALSO THIS IS UGLY BUT WORKS :)
    return render_template('myOpenings.html',  myopenings = myopen)

@login_required
@bp_routes.route('/allopenings/', methods=['GET'])
def allopenings():
    if (current_user.is_anonymous):
        flash('Must be logged in to view')
        return redirect(url_for('routes.index'))
    allopen = Opening.query.all()
    return render_template('allOpenings.html',  allopenings = allopen)