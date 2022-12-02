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
    hinh_anh = Column(String(100))
    trang_thai = Column(Boolean, default=True)
    so_luong_ton = Column(Integer, nullable=False)
    the_loai_id = Column(Integer, ForeignKey(TheLoai.id), nullable=False)
    tac_gia_id = Column(Integer, ForeignKey(TacGia.id), nullable=False)
    nha_xuat_ban_id = Column(Integer, ForeignKey(NhaXuatBan.id), nullable=False)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    __tablename__= 'user'

    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    so_dien_thoai = Column(String(11), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    trang_thai = Column(Boolean, default=True)
    ngay_them = Column(DateTime, default=datetime.now())
    vai_tro = Column(Enum(UserRole), default=UserRole.normal_user)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()




