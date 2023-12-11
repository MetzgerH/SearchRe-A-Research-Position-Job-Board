from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from app.Controller.forms import OpeningForm, ApplicationForm, FilterForm
from app.Model.models import Application, Professor, Student, Opening
from config import Config
from flask_login import login_required, current_user

from app import db

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'

@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
def index():
    if (current_user.is_anonymous):
        return render_template('index.html')
    if (current_user.user_type == "Student"):
        return redirect(url_for('routes.studenthome'))
    if (current_user.user_type == "Professor"):
        return redirect(url_for('routes.profhome'))
    return render_template('index.html')

@login_required
@bp_routes.route('/studenthome', methods=['GET'])
def studenthome():
    if (current_user.is_anonymous) or (current_user.user_type != "Student"):
        flash('Cannot access student home as non-student.')
        return redirect(url_for('routes.index'))
    return render_template('student_home.html')

@login_required
@bp_routes.route('/profhome', methods=['GET'])
def profhome():
    if (current_user.is_anonymous) or (current_user.user_type != "Professor"):
        flash('Cannot access faculty home as non-faculty.')
        return redirect(url_for('routes.index'))
    return render_template('prof_home.html')

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
    return render_template('create_opening.html', form = oform)

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
    return render_template('my_openings.html',  myopenings = myopen)


#STUDENTS ONLY FOR THIS ROUTE I WILL ADD
@login_required
@bp_routes.route('/openings/', methods=['GET'])
def openings():
    if (current_user.is_anonymous):
        flash('Must be logged in to view')
        return redirect(url_for('routes.index'))
    allopen = Opening.query.all()
    return render_template('openings.html',  allopenings = allopen)
    

@login_required
@bp_routes.route('/openings/recommended/',methods=['GET'])
def recommended():
    if (current_user.is_anonymous):
        flash('Must be logged in to view')
        return redirect(url_for('routes.index'))
    
    allopenings = list(Opening.query.all())
    openings = None

    for major in current_user.majors:
        if openings:
            openings += list(Opening.query.filter(Opening.majors.contains(major)))
        else:
            openings = list(Opening.query.filter(Opening.majors.contains(major)))
    for lang in current_user.programming_languages:
        if openings:
            openings += list(Opening.query.filter(Opening.programming_languages.contains(lang)))
        else:
            openings = list(Opening.query.filter(Opening.programming_languages.contains(lang)))

    openings = list(openings)
    for element in openings:
        allopenings.remove(element)
    allopenings = openings + allopenings
    return render_template('openings.html', allopenings = allopenings)
    
    

@login_required
@bp_routes.route('/opening/<oid>', methods=['GET'])
def opening(oid):
    if (current_user.is_anonymous):
        flash('Must be logged in to view')
        return redirect(url_for('routes.index'))
    open = Opening.query.filter_by(id = oid).first()
    applications = db.session.query(Application).filter_by(opening_id = open.id).all() #ALSO THIS IS UGLY BUT WORKS :)
    return render_template('full_details.html', opening = open, applications = applications)

@login_required
@bp_routes.route('/opening/application/<oid>/', methods=['GET', 'POST'])
def apply(oid):
    if (current_user.is_anonymous) or (current_user.user_type != "Student"):
        flash('Must be logged in as student.')
        return redirect(url_for('routes.index'))
    aform = ApplicationForm()
    if aform.validate_on_submit():
        app = Application(interest_statement = aform.interest.data, reference_name=aform.ref_name.data, reference_email = aform.ref_email.data)
        app.applicant_id = current_user.id #clean this up by using the backref when loading applicant details???
        app.opening_id = oid               #like application.applicant or application.opening??
        db.session.add(app)
        db.session.commit()
        flash('Your application has been submitted')
        return redirect(url_for('routes.myapplications'))
    return render_template('application.html', form = aform)

@login_required
@bp_routes.route('/opening/application/<oid>/<aid>',methods=['GET']) #later post for accepting and withdrawing
def application(oid,aid): #use oid to track what you opening youre looking at?
    if (current_user.is_anonymous):
        flash('Must be logged in to view')
        return redirect(url_for('routes.index'))
    appl = Application.query.filter_by(id = aid).first()
    return render_template('full_application.html', application = appl)

@login_required
@bp_routes.route('/myapplications',methods=['GET'])
def myapplications():
    if (current_user.is_anonymous) or (current_user.user_type != "Student"):
        flash('Must be logged in as student.')
        return redirect(url_for('routes.index'))
    return render_template('my_applications.html', myapplications = current_user.applications)

@login_required
@bp_routes.route('/search',methods=['GET', 'POST'])
def search():
    if (current_user.is_anonymous) or (current_user.user_type != "Student"):
        flash('Must be logged in as student.')
        return redirect(url_for('routes.index'))
    fform = FilterForm()
    if fform.validate_on_submit():
        openings = None
        if fform.title.data:
            openings = list(Opening.query.filter(Opening.title.contains(fform.title.data)))
        if fform.description.data:
            if openings:
                openings += list(Opening.query.filter(Opening.description.contains(fform.description.data)))
            else:
                openings = list(Opening.query.filter(Opening.description.contains(fform.description.data)))
        if fform.titleOrDesc.data:
            if openings:
                openings += list(Opening.query.filter(Opening.description.contains(fform.titleOrDesc.data)))
                openings += list(Opening.query.filter(Opening.title.contains(fform.titleOrDesc.data)))
            else:
                openings = list(Opening.query.filter(Opening.description.contains(fform.titleOrDesc.data)))
                openings += list(Opening.query.filter(Opening.title.contains(fform.titleOrDesc.data)))
        if fform.major.data:
            for major in fform.major.data:
                if openings:
                    openings += list(Opening.query.filter(Opening.majors.contains(major)))
                else:
                    openings = list(Opening.query.filter(Opening.majors.contains(major)))
        if fform.languages.data:
            for lang in fform.languages.data:
                if openings:
                    openings += list(Opening.query.filter(Opening.programming_languages.contains(lang)))
                else:
                    openings = list(Opening.query.filter(Opening.programming_languages.contains(lang)))
        return render_template('search.html', openings = openings, form = fform)
    return render_template('search.html', form = fform)
        