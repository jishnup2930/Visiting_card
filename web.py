import db
import flask
from flask_cors import CORS

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
    if flask.request.method == "POST":
        leave_q = d.select(func.count(db.Leave.id)).where(db.Leave.employee_id == empid)
        leaves_taken = d.session.execute(leave_q).scalar()
        
        query = d.select(db.Designation.max_leaves).where(db.Employee.id == empid)
        max_leave = d.session.execute(query).scalar()
        
        if leaves_taken >= max_leave:
            print('dwsxfszdsdfdddddddddd')
            query = d.select(db.Employee).where(db.Employee.id == empid)
            user = d.session.execute(query).scalar()
            return flask.render_template("add_leave.html", user=user, leaves_taken=leaves_taken)
            # return redirect(url_for("employees"))

        else:
            leave_date = flask.request.form.get("leave_date")
            leave_reason = flask.request.form.get("leave_reason")
            leave = db.Leave(date=leave_date, employee_id=empid, reason=leave_reason)
            d.session.add(leave)
            d.session.commit()
            return redirect(url_for("employees"))

# @app.route('/search')
# def search():
#     query = request.args.get('query', '').lower()
    
#     # Execute the query and fetch the users
#     users = d.query(db.Employee).all()
    
#     filtered_users = [
#         user for user in users 
#         if query in user.fname.lower() or query in user.lname.lower()
#     ]
    
#     # Create a list of dictionaries for JSON serialization
#     filtered_user_dicts = [
#         {'id': user.id, 'fname': user.fname, 'lname': user.lname}
#         for user in filtered_users
#     ]
    
#     return jsonify(filtered_user_dicts)

@app.route("/about")
def about():
    return flask.render_template("about.html")

