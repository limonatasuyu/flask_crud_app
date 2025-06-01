from flask import Flask, request, render_template, redirect
from models import db, EmployeeModel

app = Flask(__name__)

# Linking SQLite DB with SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"

"""
quote from documentation:

If set to True, Flask-SQLAlchemy will track modifications of objects and emit signals. The
default is None, which enables tracking but issues a warning that it will be disabled by default
in the future. This requires extra memory and should be disabled if not needed.
"""
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Linking db instance from models.py
db.init_app(app)


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def HomePage():
    return render_template("home.html")


@app.route("/data/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("createpage.html")

    if request.method == "POST":
        employee_id = request.form["employee_id"]
        name = request.form["name"]
        age = request.form["age"]
        position = request.form["position"]
        employee = EmployeeModel(
            employee_id=employee_id, name=name, age=age, position=position
        )
        db.session.add(employee)
        db.session.commit()
        return redirect("/data")


@app.route("/data")
def RetrieveDataList():
    employees = EmployeeModel.query.all()
    return render_template("datalist.html", employees=employees)


@app.route("/data/<int:id>")
def RetrieveSingleEmployee(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()

    if employee:
        return render_template("data.html", employee=employee)

    return f"Employee with id ={id} Doenst exist"


@app.route("/data/<int:id>/update", methods=["GET", "POST"])
def update(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == "POST":
        if employee:
            db.session.delete(employee)
            db.session.commit()

            name = request.form["name"]
            age = request.form["age"]
            position = request.form["position"]
            employee = EmployeeModel(
                employee_id=id, name=name, age=age, position=position
            )

            db.session.add(employee)
            db.session.commit()

            return redirect(f"/data/{id}")

        return f"Employee with id = {id} Does nit exist"

    return render_template("update.html", employee=employee)


@app.route("/data/<int:id>/delete", methods=["GET", "POST"])
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == "POST":
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return redirect("/data")
        abort(404)
    return render_template("delete.html")


if __name__ == "__main__":
    app.run()
