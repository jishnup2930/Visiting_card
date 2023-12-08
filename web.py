import db
import flask

from flask import url_for, redirect
from sqlalchemy.sql import func

employees = []

app = flask.Flask("hrms")
d = db.SQLAlchemy(model_class=db.HRDBBase)

@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "GET":
        return flask.render_template("index.html")
    elif flask.request.method == "POST":
        return "Posted!"


@app.route("/employees")
def employees():
    query = d.select(db.Employee).order_by(db.Employee.fname)
    users = d.session.execute(query).scalars()
    return flask.render_template("userlist.html", users = users)


# @app.route("/employees/<int:empid>")
# def employee_details(empid):
#     query_1 = d.select(db.Employee).order_by(db.Employee.fname)
#     users = d.session.execute(query_1).scalars()
#     query_2 = d.select(db.Employee).where(db.Employee.id == empid)
#     user = d.session.execute(query_2).scalar()
#     leave_q =d.select(func.count(db.Employee.id)).join(db.Leave,db.Employee.id == db.Leave.employee_id).filter(db.Employee.id==empid)
#     leave =d.session.execute(leave_q).scalar()
#     return flask.render_template("userdetail.html", user = user,users=users,leave=leave)

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


@app.route("/add_leave/<int:empid>", methods=["POST"])
def add_leave(empid):
    if flask.request.method == "POST":
        leave_date = flask.request.form.get("leave_date")
        leave_reason = flask.request.form.get("leave_reason")
        leave = db.Leave(date=leave_date, employee_id=empid, reason=leave_reason)
        d.session.add(leave)
        d.session.commit()
        return flask.redirect(url_for("employee_details", empid=empid))
    
@app.route("/about")
def about():
    return flask.render_template("about.html")

