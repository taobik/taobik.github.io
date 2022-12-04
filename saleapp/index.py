from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, login_required
from saleapp import app, login
import utils
from saleapp.models import UserRole
from saleapp.admin import *


@app.route("/")
def home():
    sach = utils.load_sach()
    err_msg = request.args.get('err_msg')
    return render_template("index.html",
                           sach=sach,
                           err_msg=err_msg)


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
    sp = utils.load_sp_by_id(id_sp)
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
                us = utils.load_username(username)
                if us == 1:
                    err_msg = "Tên đăng ký đã có người sử dụng"
                else:
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

        user_admin = utils.user_check(username, password, role=UserRole.admin)
        user = utils.user_check(username, password, role=UserRole.normal_user)
        if user_admin:
            login_user(user=user_admin)
            err_msg = "Đăng nhập quản trị thành công"
            return redirect(url_for('dangnhap_admin', err_msg=err_msg))
        else:
            if user:
                login_user(user=user)

                next = request.args.get('next', 'home')
                err_msg = "Đăng nhập thành công"
                return redirect(url_for(next, err_msg=err_msg))
            else:
                err_msg = "Đăng nhập thất bại!! Hãy thử lại sau"

    return render_template('dangnhap.html', err_msg=err_msg)


@app.route('/admin-login', methods=['post', 'get'])
def dangnhap_admin():
    return redirect('/admin')


@app.route('/dangxuat')
def dangxuat():
    logout_user()
    return redirect(url_for('dangnhap'))


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/cart')
def gio_hang():
    return render_template('giohang.html',
                           st=utils.cart_stats(session.get('cart')))


@app.route('/api/add-cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    gia = data.get('gia')

    cart = session.get('cart')

    if not cart:
        cart = {}

    if id in cart:
        cart[id]['so_luong'] = cart[id]['so_luong'] + 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'gia': gia,
            'so_luong': 1
        }

    session['cart'] = cart

    return jsonify(utils.cart_stats(cart))


@app.route('/api/pay', methods=['post'])
@login_required
def pay():
    try:
        utils.them_receipt(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


@app.context_processor
def common_response():
    return {
        'cart_stats': utils.cart_stats(session.get('cart'))
    }


if __name__ == '__main__':
    app.run(debug=True)
