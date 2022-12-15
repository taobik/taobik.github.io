from saleapp import app, db
from saleapp.models import Sach, TheLoai, TacGia, User, NhaXuatBan, UserRole, ReceiptDetail, Receipt, Comments
from sqlalchemy import func
from flask_login import current_user
import hashlib


def load_theloai():
    return TheLoai.query.all()


def load_sach(id=None, max=None, maxban=None, minban=None):
    sach = Sach.query.filter(Sach.trang_thai.__eq__(True))
    if id:
        sach = sach.filter(Sach.the_loai_id.__eq__(id))
    if max:
        sach = sach.order_by(-Sach.da_ban).limit(max)
    if maxban:
        sach = sach.filter(Sach.da_ban).order_by(Sach.da_ban).limit(maxban)
    if minban:
        sach = sach.filter(Sach.da_ban).order_by(Sach.da_ban).limit(minban)
    return sach


def load_sp_by_id(id_sp):
    with app.app_context():
        return Sach.query.join(TheLoai, TheLoai.id == Sach.the_loai_id, isouter=True) \
            .join(TacGia, TacGia.id == Sach.tac_gia_id) \
            .join(NhaXuatBan, NhaXuatBan.id == Sach.nha_xuat_ban_id) \
            .filter(Sach.id.__eq__(id_sp)) \
            .add_columns(Sach.id, Sach.hinh_anh, Sach.gia, Sach.so_luong_ton, TheLoai.id, TheLoai.name, TacGia.name,
                         NhaXuatBan.name).all()


def load_tl():
    with app.app_context():
        return db.session.query(TheLoai.id, TheLoai.name, func.count(Sach.id)) \
            .join(Sach, Sach.the_loai_id == TheLoai.id, isouter=True) \
            .group_by(TheLoai.id, TheLoai.name).all()


def load_dtthang_sp(kw=None, from_date=None, to_date=None):
    sach = db.session.query(Sach.id, Sach.name, func.sum(ReceiptDetail.don_gia * ReceiptDetail.so_luong))\
                            .join(ReceiptDetail, ReceiptDetail.sach_id.__eq__(Sach.id), isouter=True)\
                            .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))\
                            .group_by(Sach.id)
    if kw:
        sach = sach.filter(Sach.name.contains(kw))
    if from_date:
        sach = sach.filter(Receipt.ngay_tao.__ge__(from_date))
    if to_date:
        sach = sach.filter(Receipt.ngay_tao.__le__(to_date))
    return sach.all()


def load_dtthang_tl(kw=None, from_date=None, to_date=None):
    sach = db.session.query(TheLoai.id, TheLoai.name, func.sum(ReceiptDetail.so_luong * ReceiptDetail.don_gia))\
                            .join(Sach, Sach.the_loai_id.__eq__(TheLoai.id))\
                            .join(ReceiptDetail, ReceiptDetail.sach_id.__eq__(Sach.id))\
                            .group_by(TheLoai.id)
    if kw:
        sach = sach.filter(TheLoai.name.contains(kw))
    if from_date:
        sach = sach.filter(Receipt.ngay_tao.__ge__(from_date))
    if to_date:
        sach = sach.filter(Receipt.ngay_tao.__le__(to_date))
    return sach.all()


def load_username(u):
    us = db.session.query(User.username).group_by(User.username).all()
    for x in us:
        if u == x[0]:
            p = 1
        else:
            p = 2
    return p


def get_user_by_id(user_id):
    return User.query.get(user_id)


def user_add(name, username, password, email, so_dien_thoai, avatar):
    # password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(), username=username.strip(), password=password, email=email,
                so_dien_thoai=so_dien_thoai, avatar=avatar)
    db.session.add(user)
    db.session.commit()


def user_check(username, password, role=UserRole.normal_user):
    if username and password:
        # password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.vai_tro.__eq__(role)).first()


def them_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)

        for x in cart.values():
            p = ReceiptDetail(receipt=receipt,
                              sach_id=x['id'],
                              so_luong=x['so_luong'],
                              don_gia=x['gia'])
            db.session.add(p)

        db.session.commit()


def load_comments(sachid):
    return Comments.query.filter(Comments.sach_id.__eq__(sachid)).order_by(-Comments.ngay_tao).all()


def save_comment(sach_id, comment, ngay_tao):
    c = Comments(comment=comment, sach_id=sach_id, user=current_user, ngay_tao=ngay_tao)
    db.session.add(c)
    db.session.commit()

    return c


def cart_stats(cart):
    total_amount, total_quantity = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['so_luong']
            total_amount += c['so_luong'] * c['gia']

    return {
        'total_amount': total_amount,
        'total_quantity': total_quantity
    }
