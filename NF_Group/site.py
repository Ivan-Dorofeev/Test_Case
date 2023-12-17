from flask import Flask, render_template, redirect, url_for, request
from dotenv import load_dotenv

from db_func import db_all_metros, db_all_re_objects, db_add_metro, db_add_re_object, db_re_objects_by_id, \
    db_re_object_metros, db_filter_re_objects

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main():
    """Главная страница"""
    if request.method == "POST":
        s_area = request.form.get('area') if request.form.get('area') else 0
        s_floor = request.form.get('floor') if request.form.get('floor') else 0
        s_metro = request.form.get('metro')
        all_objects = db_filter_re_objects(s_area, s_floor, s_metro)
        return render_template("main.html", all_objects=all_objects, s_area=s_area, s_floor=s_floor, s_metro=s_metro)

    all_objects = db_all_re_objects()
    return render_template("main.html", all_objects=all_objects)


@app.route('/object_detail/<id>')
def object_detail(id):
    """Детальная информация по объекту"""
    re_obj = db_re_objects_by_id(id)
    re_obj_metros = db_re_object_metros(id)
    return render_template("detail.html", re_obj=re_obj, re_obj_metros=re_obj_metros)


@app.route('/add_metro', methods=["GET", "POST"])
def add_metro():
    """Создаём новое метро"""
    all_metros = db_all_metros()
    if request.method == "POST":
        name = request.form["name"]
        if name in all_metros:
            return render_template("add_metro.html", all_metros=all_metros, error_msg="Такое метро уже существует")
        db_add_metro(name)
        return redirect(url_for("add_metro"))

    return render_template("add_metro.html", all_metros=all_metros)


@app.route('/add_re_object', methods=["GET", "POST"])
def add_re_object():
    """Создаём нового объекта"""
    if request.method == "POST":
        data = request.form
        name = data["name"],
        address = data["address"],
        floor = data["floor"],
        area = data["area"],
        obj_type = data["obj_type"]
        metro = data.getlist("metro")

        db_add_re_object(name, address, floor, area, obj_type, metro)
        return redirect(url_for("main"))

    obj_types = (('Квартира', 'Квартира'), ('Апартаменты', 'Апартаменты'), ('Пентхаус', 'Пентхаус'))
    metros = db_all_metros()
    return render_template("add_object.html", obj_types=obj_types, metros=metros)


if __name__ == '__main__':
    app.run(debug=False)
