from app import create_app, db
from app.Model.models import User, Major, ProgLang, Student, Professor, Opening

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': app.db, 'User': User, 'Major': Major, 'ProgLang': ProgLang, 'Student': Student, 'Professor': Professor, 'Opening': Opening}

@app.before_request
def initDB(*args, **kwargs):
    if app.got_first_request:
        db.create_all()
        if Major.query.count() == 0:
            majors = [{'name':'Computer Science'},
                      {'name':'Software Engineering'},
                      {'name':'Electrical Engineering'},
                      {'name':'Mechanical Engineering'},
                      {'name':'Mathematics'}  ]
            for t in majors:
                db.session.add(Major(name=t['name']))
            db.session.commit()
        if ProgLang.query.count() == 0:
            langs = [{'name':'C/C++'},
                      {'name':'Python'},
                      {'name':'Java'}  ]
            for l in langs:
                db.session.add(ProgLang(name=l['name']))
            db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)