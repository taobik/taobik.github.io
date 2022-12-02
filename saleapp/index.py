from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user
from saleapp import app, login
import utils
from saleapp.admin import *


@app.route("/")
def home():
    sach = utils.load_sach()

    return render_template("index.html",
                           sach=sach)


@app.route("/sanpham")
def san_pham():
    id = request.args.get('the_loai_id')
    sach = utils.load_sach(id=id)
    soluongtl = utils.load_tl()
    return render_template("sanpham.html",
                           sach=sach,
                           soluongtl=soluongtl)


@app.route("/chitietsanpham/<int:id_sp>")
def chitiet(id_sp):
    id = request.args.get('the_loai_id')
    sach = utils.load_sach(id=id)
    sp = utils.load_sp(id_sp)
    return render_template("chitietsanpham.html",
                           sp=sp,
                           sach=sach)


@app.route("/dangky", methods=['get', 'post'])
def dangky():
    err_msg = ""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['passw']
        repass = request.form['repass']
        sodt = request.form['sodt']

        try:
            if password.strip().__eq__(repass.strip()):
                utils.user_add(name=name, username=username, password=password, email=email, so_dien_thoai=sodt)
                err_msg = "Đăng kí thành công"
                return redirect(url_for('dangnhap', err_msg=err_msg))
            else:
                err_msg = "Mật khẩu không khớp"
        except Exception as ex:
            err_msg = "Hệ thống đang có lỗi: " + str(ex)

    return render_template('dangky.html', err_msg=err_msg)


@app.route('/danhnhap', methods=['get', 'post'])
def dangnhap():
    err_msg = request.args.get('err_msg')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['passw']

        user = utils.user_check(username, password)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))

    return render_template('dangnhap.html', err_msg=err_msg)


@app.route('/dangxuat')
def dangxuat():
    logout_user()
    return redirect(url_for('dangnhap'))


@app.route("/login<user>")
def send(user):
    return render_template("aa.html")
# @app.route('/api/cart', methods=['post'])
# def add_to_cart():
#     pass


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    app.run(debug=True)