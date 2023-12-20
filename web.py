import db
import flask
from flask_cors import CORS
from flask import request
from flask import url_for, redirect
from sqlalchemy.sql import func

employees = []

app = flask.Flask("hrms")
CORS(app)
d = db.SQLAlchemy(model_class=db.HRDBBase)

@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "GET":
        return flask.render_template("index.html")
    elif flask.request.method == "POST":
        return "Posted!"


@app.route("/employees")
def employees():
    query = d.select(db.Employee).order_by(db.Employee.id,db.Employee.fname,db.Employee.lname)
    users = d.session.execute(query).scalars()
    ret =[]
    for user in users:
        details = {"id":user.id,
            "fname" : user.fname,
            "lname" : user.lname,
            "designation":user.title.title}
        ret.append(details)
    return flask.jsonify(ret)

@app.route("/employees/<int:empid>")
def employee_details(empid):
    query = d.select(db.Employee).where(db.Employee.id == empid)
    user = d.session.execute(query).scalar()
    leave_q =d.select(func.count(db.Employee.id)).join(db.Leave,db.Employee.id == db.Leave.employee_id).filter(db.Employee.id==empid)
    leave =d.session.execute(leave_q).scalar()
    ret = {"id":user.id,
           "fname" : user.fname,
           "lname" : user.lname,
           "title" : user.title.title,
           "email" : user.email,
           "phone" : user.phone,
           "max_leaves":user.title.max_leaves,
           "leave":leave}
    return flask.jsonify(ret)

@app.route("/leave/<int:empid>", methods=["POST"])
def add_leave(empid):
    try:
        if request.method == "POST":
            data = request.json
            leave_date = data.get("leave_date")
            leave_reason = data.get("leave_reason")
            leave_q = d.select(func.count(db.Leave.id)).where(db.Leave.employee_id == empid)
            leaves_taken = d.session.execute(leave_q).scalar()
            
            query = d.select(db.Designation.max_leaves).where(db.Employee.id == empid)
            max_leave = d.session.execute(query).scalar()
            
            if leaves_taken >= max_leave:
                return flask.jsonify({"Error:No leave left for this employee"}),400
            else:
                leave = db.Leave(date=leave_date, employee_id=empid, reason=leave_reason)
                d.session.add(leave)
                d.session.commit()
                return flask.jsonify({"message": "Leave added successfully"}),200

    except Exception as e:
        return flask.jsonify({"error": "An unexpected error occurred"}), 500

@app.route("/vcard/<int:empid>")
def generate_vcard(empid):
    vcard_q =d.select(db.Employee).where(db.Employee.id==empid)
    user=d.session.execute(vcard_q).scalar()
    ret={"vcard":f"""
            BEGIN:VCARD
            VERSION:2.1
            N:{user.lname};{user.fname}
            FN:{user.fname} {user.lname}
            ORG:Authors, Inc.
            TITLE:{user.title.title}
            TEL;WORK;VOICE:{user.phone}
            ADR;WORK:;;100 Flat Grape Dr.;Fresno;CA;95555;United States of America
            EMAIL;PREF;INTERNET:{user.email}
            REV:20150922T195243Z
            END:VCARD"""}

    return flask.jsonify(ret)
    

@app.route("/about")
def about():
    return flask.render_template("about.html")

