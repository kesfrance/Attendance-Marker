from flask import render_template, redirect, url_for, request, Response
import json
import datetime
from datetime import datetime as d
from datetime import date
from marker import app
from .database import session
from .models import User, Member, Cell
import mistune
import datetime
from flask import flash
from flask.ext.login import login_user, login_required,current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask.ext.mail import Mail, Message

req = lambda y : request.form[y]

@app.route("/cells", methods = ['GET','POST'])
def cells():
    cells = session.query(Cell).order_by(Cell.cellname)
    admin = session.query(User).filter_by(email="kesfrance@yahoo.com").one()
    if request.method== 'POST':
       grp = Cell(cellname = req('cellname'),
         cellleader = req('cellleader'),
         celldescrip = req('celldescrip')
        )
       session.rollback()
       session.add(grp)
       session.commit()
       
       return redirect(url_for('cells', cells=cells, admin=admin))
    else:
        
        return render_template('cells.html', cells=cells, admin=admin)

@app.route("/cells/members/<int:id>", methods = ['GET','POST'])
def singlemembreport(id):
    cellmember = session.query(Member).filter_by(id = id).first()
    if request.method == 'POST':
        cellmember.memb_wk1 = req('memb_wk1')
        cellmember.memb_wk2 = req('memb_wk2')
        cellmember.memb_wk3 = req('memb_wk3')
        cellmember.memb_wk4 = req('memb_wk4')
        cellmember.memb_wk5 = req('memb_wk5')
        cellmember.memb_comment = req('memb_comment')
       # session.rollback()
        session.add(cellmember)
        session.commit()
        return redirect(url_for('cellreport', id=cellmember.cell_id))
    else:
        
        return render_template('singlecellreport.html', mem=cellmember,
                               cellid=cellmember.cell_id)

@app.route("/cells/<int:id>/cellreports", methods = ['GET','POST'])
def cellreport(id):
    if request.method == 'POST':
        cell_id = req('cellid')
        member = Member(memb_name = req('memb_name'),
            memb_address = req('memb_address'),
            memb_email = req('memb_email'),
            memb_contact = req('memb_contact'),
            memb_comment = req('memb_comment'),
            cell_id = req('cellid')
            )

        session.add(member)
        session.commit()
        return redirect(url_for('cellreport', id=cell_id))
    else:
        cells = session.query(Cell)
        cell = session.query(Cell).filter_by(id=id).one()
        member = session.query(Member).filter_by(cell_id=id).order_by(Member.memb_name)
    return render_template('cellreport.html', member=member, cell=cell, cells=cells)

@app.route("/delcell", methods = ['GET','POST'])
def delcellPost():
    if request.method =='POST':
        cellid = request.form['deleteitem'] #request.form['program_id'])
        celldel = session.query(Cell).filter_by(id = int(cellid)).one()
        session.delete(celldel)
        session.commit()
        return redirect(url_for('cells'))
    else:
        return "ok"

@app.route("/")
@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    flash("You have logged in", "info")
    return redirect(request.args.get('next') or url_for("cells"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for('login_get'))


@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
    return render_template("add_post.html")


@app.route("/signup", methods=["GET"])
def signup_get():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    name=request.form["name"]
    email=request.form["email"]
    password=request.form["password"]
    password_2=request.form["re-password"]

    if session.query(User).filter_by(email=email).first():
        flash("User with that email address already exists", "danger")
        return redirect(url_for("signup_get"))

    if not (password and password_2) or password != password_2:
        flash("Passwords did not match", "danger")
        return redirect(url_for("signup_get"))

    user = User(name=name, email=email, password=generate_password_hash(password))

    session.add(user)
    session.commit()

    flash("Success! You may now login with your credentials", "info")
    return redirect(url_for("login_get"))


