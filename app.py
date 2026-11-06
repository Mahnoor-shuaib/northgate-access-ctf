import os

from flask import Flask, render_template, request, make_response

app = Flask(__name__)

# Flag: 24 characters in total. Override with the FLAG environment variable if needed.
FLAG = os.environ.get("FLAG", "CGS{t34ch3r_c00k13_h4ck}")

COURSES = [
    {"code": "CS-201", "name": "Data Structures", "room": "Hall B, 10:00", "tag": "Mon / Wed"},
    {"code": "CS-224", "name": "Database Systems", "room": "Lab 3, 12:30", "tag": "Tue / Thu"},
    {"code": "MT-210", "name": "Discrete Mathematics", "room": "Hall A, 09:00", "tag": "Mon / Fri"},
    {"code": "HU-105", "name": "Technical Writing", "room": "Room 14, 14:00", "tag": "Wed"},
]

NEWS = [
    ("Nov 03", "Mid-term result sheets are now available at the examination office."),
    ("Nov 01", "Library hours extended until 9 pm during the exam season."),
    ("Oct 28", "Career fair registration closes this Friday."),
]

GRADEBOOK = [
    ("Ayesha Khan", "CS-201", "A-"),
    ("Bilal Ahmed", "CS-201", "B+"),
    ("Hira Fatima", "CS-224", "A"),
    ("Usman Ali", "MT-210", "B"),
    ("Zainab Noor", "HU-105", "A-"),
]


def current_role():
    """VULNERABILITY: the role is read straight from a cookie the user controls."""
    return request.cookies.get("role", "student").strip().lower()


def page(template, status=200, **ctx):
    role = current_role()
    resp = make_response(render_template(template, role=role, **ctx), status)
    # Every new visitor is handed a plain 'student' role cookie.
    if "role" not in request.cookies:
        resp.set_cookie("role", "student", samesite="Lax")
    return resp


@app.route("/")
def home():
    return page("home.html", courses=COURSES, news=NEWS)


@app.route("/faculty")
def faculty():
    # VULNERABILITY: authorization depends only on the client-supplied cookie value.
    if current_role() != "teacher":
        return page("denied.html", status=403)
    return page("faculty.html", gradebook=GRADEBOOK, flag=FLAG)


@app.errorhandler(404)
def not_found(_):
    return page("denied.html", status=404, missing=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
