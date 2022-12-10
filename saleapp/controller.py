from flask import render_template, request, redirect, session, jsonify, url_for
from saleapp import app, utils
from flask_login import login_user, logout_user, login_required
from saleapp.models import UserRole
from datetime import datetime
import cloudinary.uploader


def home():
    sach = utils.load_sach()
    max_sach = utils.load_sach(max=4)
    min_sach = utils.load_sach(minban=4)
    ton = utils.load_sach(maxban=4)
    err_msg = request.args.get('err_msg')
    return render_template("index.html",
                           sach=sach,
                           max_sach=max_sach,
                           ton=ton,
                           min_sach=min_sach,
                           err_msg=err_msg)


def san_pham():
    id = request.args.get('the_loai_id')
    sach = utils.load_sach(id=id)
    soluongtl = utils.load_tl()
    return render_template("sanpham.html",
                           sach=sach,
                           soluongtl=soluongtl)


def chitiet(id_sp):
    id = request.args.get('the_loai_id')
    sach = utils.load_sach(id=id)
    sp = utils.load_sp_by_id(id_sp)
    return render_template("chitietsanpham.html",
                           sp=sp,
                           sach=sach)


def dangky():
    err_msg = ""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['passw']
        repass = request.form['repass']
        sodt = request.form['sodt']
        avatar_path = None

        try:
            if password.strip().__eq__(repass.strip()):
                if utils.load_username(username) == 1:
                    err_msg = "Tên đăng ký đã có người sử dụng"
                else:
                    avatar = request.files.get('avatar')
                    if avatar:
                        res = cloudinary.uploader.upload(avatar)
                        avatar_path = res['secure_url']
                    utils.user_add(name=name, username=username, password=password, email=email, so_dien_thoai=sodt,
                                   avatar=avatar_path)
                    err_msg = "Đăng kí thành công"
                    return redirect(url_for('dangnhap', err_msg=err_msg))
            else:
                err_msg = "Mật khẩu không khớp"
        except Exception as ex:
            err_msg = "Hệ thống đang có lỗi: " + str(ex)

    return render_template('dangky.html', err_msg=err_msg)


def dangnhap():
    err_msg = request.args.get('err_msg')
    i = 1
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

                err_msg = "Đăng nhập thành công"
                n = request.args.get('next')
                return redirect(n if n else '/')
            else:
                err_msg = "Đăng nhập thất bại!! Hãy thử lại sau"
                i = 2

    return render_template('dangnhap.html', err_msg=err_msg, i=i)


def dangnhap_admin():
    return redirect('/admin')


def dangxuat():
    logout_user()
    return redirect(url_for('dangnhap'))


def gio_hang():
    return render_template('giohang.html',
                           st=utils.cart_stats(session.get('cart')))


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


def update_cart():
    data = request.json
    id = str(data.get('id'))
    so_luong = data.get('so_luong')

    cart = session.get('cart')
    if cart and id in cart:
        cart[id]['so_luong'] = so_luong
        session['cart'] = cart

    return jsonify(utils.cart_stats(cart))


def xoa_hang(id_sp):
    cart = session.get('cart')

    if cart and id_sp in cart:
        del cart[id_sp]
        session['cart'] = cart

    return jsonify(utils.cart_stats(cart))


@login_required
def pay():
    try:
        utils.them_receipt(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


def comments(sach_id):
    data = []
    for c in utils.load_comments(sach_id):
        data.append({
            'id': c.id,
            'comment': c.comment,
            'ngay_tao': str(c.ngay_tao),
            'user': {
                'name': c.user.name,
                'avatar': c.user.avatar
            }
        })

    return jsonify(data)


def add_comment(sach_id):
    try:
        c = utils.save_comment(sach_id=sach_id, comment=request.json['comment'], ngay_tao=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    except:
        return jsonify({'status': 500})
    else:
        return jsonify({
            'status': 204,
            'comment': {
                'id': c.id,
                'comment': c.comment,
                'ngay_tao': str(c.ngay_tao),
                'user': {
                    'name': c.user.name,
                    'avatar': c.user.avatar
                }
            }
        })

