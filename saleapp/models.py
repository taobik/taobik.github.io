from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from saleapp import db, app
from datetime import datetime
from enum import Enum as userenum
from flask_login import UserMixin


class UserRole(userenum):
    admin = 1
    normal_user = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class TheLoai(BaseModel):
    __tablename__ = 'TheLoai'

    name = Column(String(50), nullable=False)
    Sach = relationship('Sach', backref='TheLoai', lazy=False)

    def __str__(self):
        return self.name


class NhaXuatBan(BaseModel):
    __tablename__ = 'NhaXuatBan'

    name = Column(String(50), nullable=False)
    dia_chi = Column(String(50), nullable=False)
    Sach = relationship('Sach', backref='NhaXuatBan', lazy=False)

    def __str__(self):
        return self.name


class TacGia(BaseModel):
    __tablename__ = 'TacGia'

    name = Column(String(50), nullable=False)
    Sach = relationship('Sach', backref='TacGia', lazy=False)

    def __str__(self):
        return self.name


class Sach(BaseModel):
    __tablename__ = 'Sach'

    name = Column(String(50), nullable=False)
    gia = Column(Float, default=0)
    hinh_anh = Column(String(255))
    trang_thai = Column(Boolean, default=True)
    da_ban = Column(Integer, nullable=False)
    so_luong_ton = Column(Integer, nullable=False)
    the_loai_id = Column(Integer, ForeignKey(TheLoai.id), nullable=False)
    tac_gia_id = Column(Integer, ForeignKey(TacGia.id), nullable=False)
    nha_xuat_ban_id = Column(Integer, ForeignKey(NhaXuatBan.id), nullable=False)
    receipt_details = relationship('ReceiptDetail', backref='sach', lazy=True)
    comment = relationship('Comments', backref='sach', lazy=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    so_dien_thoai = Column(String(11), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(255), nullable=False)
    trang_thai = Column(Boolean, default=True)
    ngay_them = Column(DateTime, default=datetime.now())
    vai_tro = Column(Enum(UserRole), default=UserRole.normal_user)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comment = relationship('Comments', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    ngay_tao = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)


class ReceiptDetail(db.Model):
    so_luong = Column(Integer, default=0)
    don_gia = Column(Float, default=0)
    sach_id = Column(Integer, ForeignKey(Sach.id), nullable=False, primary_key=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)


class Comments(BaseModel):
    comment = Column(String(255), nullable=False)
    ngay_tao = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    sach_id = Column(Integer, ForeignKey(Sach.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        u1 = User(name='truong linh', email='linh01653023898@gmail.com', so_dien_thoai=
        '0985623320', username='taobik', password='taobik',
                  avatar='https://res.cloudinary.com/dascseee2/image/upload/v1670516895/cld-sample-5.jpg', trang_thai=1,
                  ngay_them='2022-12-03 18:38:41', vai_tro=UserRole.admin)
        u2 = User(name='minh sang', email='linh01653023898@gmail.com', so_dien_thoai=
        '0985623320', username='sangsang', password='sang',
                  avatar='https://res.cloudinary.com/dascseee2/image/upload/v1670516893/cld-sample.jpg', trang_thai=1,
                  ngay_them='2022-12-03 23:53:05', vai_tro=UserRole.normal_user)
        db.session.add_all([u1, u2])
        db.session.commit()

        tg1 = TacGia(name='Tony Buổi Sáng')
        tg2 = TacGia(name='Thân Hoàng Giang')
        tg3 = TacGia(name='Nhiều Tác Giả')
        tg4 = TacGia(name='Robert Greene')
        tg5 = TacGia(name='Richard S. Tedlow')
        tg6 = TacGia(name='Cao Minh')

        db.session.add_all([tg1, tg2, tg3, tg4, tg5, tg6])
        db.session.commit()

        tl1 = TheLoai(name='Văn học')
        tl2 = TheLoai(name='Tâm lý')
        tl3 = TheLoai(name='Thiếu nhi')
        tl4 = TheLoai(name='Kinh tế')

        db.session.add_all([tl1, tl2, tl3, tl4])
        db.session.commit()

        nxb1 = NhaXuatBan(name='Trẻ', dia_chi='TP Hồ Chí Minh')
        nxb2 = NhaXuatBan(name='Kim Đồng', dia_chi='TP Hồ Chí Minh')
        nxb3 = NhaXuatBan(name='Hồng Đức', dia_chi='TP Hồ Chí Minh')
        nxb4 = NhaXuatBan(name='Văn học', dia_chi='TP Hồ Chí Minh')
        nxb5 = NhaXuatBan(name='Thanh Niên', dia_chi='TP Hồ Chí Minh')
        nxb6 = NhaXuatBan(name='Thế Giới', dia_chi='TP Hồ Chí Minh')

        db.session.add_all([nxb1, nxb2, nxb3, nxb4, nxb5, nxb6])
        db.session.commit()

        s1 = Sach(name='Trên Đường Băng (Tái Bản 2022)', gia=73000,
                  hinh_anh='https://res.cloudinary.com/dascseee2/image/upload/v1670521998/trenduongbang_oh88do.jpg',
                  trang_thai=1, da_ban=35, so_luong_ton=234, the_loai_id=1, tac_gia_id=1, nha_xuat_ban_id=1)
        s2 = Sach(name='Vàng Xám Và Những Câu Chuyện Ngốc Nghếch', gia=108000,
                  hinh_anh='https://res.cloudinary.com/dascseee2/image/upload/v1670521998/trenduongbang_oh88do.jpg',
                  trang_thai=1, da_ban=175, so_luong_ton=221, the_loai_id=1, tac_gia_id=2, nha_xuat_ban_id=4)
        s3 = Sach(name='Nghĩa Tình Miền Tây', gia=140000,
                  hinh_anh='https://res.cloudinary.com/dascseee2/image/upload/v1670521998/trenduongbang_oh88do.jpg',
                  trang_thai=1, da_ban=143, so_luong_ton=76, the_loai_id=1, tac_gia_id=3, nha_xuat_ban_id=5)
        s4 = Sach(name='Pokémon Diamond & Pearl: Bá Vương Ảo Ảnh Zoroark', gia=20000,
                  hinh_anh='https://res.cloudinary.com/dascseee2/image/upload/v1670521998/trenduongbang_oh88do.jpg',
                  trang_thai=1, da_ban=64, so_luong_ton=238, the_loai_id=4, tac_gia_id=3, nha_xuat_ban_id=2)
        s5 = Sach(name='33 Chiến Lược Của Chiến Tranh (Tái Bản 2021)', gia=70000,
                  hinh_anh='https://res.cloudinary.com/dascseee2/image/upload/v1670521998/trenduongbang_oh88do.jpg',
                  trang_thai=1, da_ban=90, so_luong_ton=50, the_loai_id=3, tac_gia_id=4, nha_xuat_ban_id=1)
        s6 = Sach(name='Những Người Khổng Lồ Trong Giới Kinh Doanh', gia=100000,
                  hinh_anh='https://res.cloudinary.com/dascseee2/image/upload/v1670521998/trenduongbang_oh88do.jpg',
                  trang_thai=1, da_ban=164, so_luong_ton=322, the_loai_id=3, tac_gia_id=5, nha_xuat_ban_id=1)
        s7 = Sach(name='Thiên Tài Bên Trái, Kẻ Điên Bên Phải (Tái Bản 2021', gia=120000,
                  hinh_anh='https://res.cloudinary.com/dascseee2/image/upload/v1670521998/trenduongbang_oh88do.jpg',
                  trang_thai=1, da_ban=236, so_luong_ton=276, the_loai_id=2, tac_gia_id=6, nha_xuat_ban_id=6)

        db.session.add_all([s1, s2, s3, s4, s5, s6, s7])
        db.session.commit()
