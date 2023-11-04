from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://sql12647981:XM51KVKzDA@sql12.freemysqlhosting.net:3306/sql12647981"

CORS(app)

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime, index=True)
    name = db.Column(db.Text(collation="latin1_swedish_ci"))
    email = db.Column(db.Text(collation="latin1_swedish_ci"))
    password = db.Column(db.Text(collation="latin1_swedish_ci"))
    college_name = db.Column(db.Text(collation="latin1_swedish_ci"))
    phone_number = db.Column(db.Text(collation="latin1_swedish_ci"))
    gender = db.Column(db.Text(collation="latin1_swedish_ci"))
    course = db.Column(db.Text(collation="latin1_swedish_ci"))
    specialization = db.Column(db.Text(collation="latin1_swedish_ci"))
    skills = db.Column(db.Text(collation="latin1_swedish_ci"))
    linkedin = db.Column(db.Text(collation="latin1_swedish_ci"))
    github = db.Column(db.Text(collation="latin1_swedish_ci"))
    behance = db.Column(db.Text(collation="latin1_swedish_ci"))


@app.route("/profile", methods=["GET", "POST"])
def user_profile():
    if request.method == "GET":
        user_email = request.args.get("email")
        user = User.query.filter_by(email=user_email).first()
        if user:
            # Split the "name" into "First Name" and "Last Name"
            first_name, last_name = user.name.split() if user.name else ("", "")
            user_data = {
                "id": user.id,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "deleted_at": user.deleted_at,
                "firstName": first_name,
                "lastName": last_name,
                "email": user.email,
                "password": user.password,
                "college_name": user.college_name,
                "phone_number": user.phone_number,
                "gender": user.gender,
                "course": user.course,
                "specialization": user.specialization,
                "skills": user.skills,
                "linkedin": user.linkedin,
                "github": user.github,
                "behance": user.behance,
            }
            return jsonify(user_data)
        else:
            return jsonify({"message": "User not found"})

    elif request.method == "POST":
        data = request.get_json()
        user_email = data.get("email")
        user = User.query.filter_by(email=user_email).first()
        if user:
            # Merge "firstName" and "lastName" into "name"
            first_name = data.get("firstName")
            last_name = data.get("lastName")
            user.name = f"{first_name} {last_name}"
            user.phone_number = data.get("phone_number")
            user.college_name = data.get("college_name")
            user.gender = data.get("gender")
            user.course = data.get("course")
            user.specialization = data.get("specialization")
            user.skills = data.get("skills")
            user.linkedin = data.get("linkedin")
            user.github = data.get("github")
            user.behance = data.get("behance")
            db.session.commit()
            return jsonify({"message": "Profile updated successfully"})
        else:
            return jsonify({"message": "User not found"})


if __name__ == "__main__":
    app.run(debug=True)
