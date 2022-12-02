from saleapp import admin, db
from saleapp.models import Sach, TheLoai, TacGia, NhaXuatBan, User
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(Sach, db.session))
admin.add_view(ModelView(TheLoai, db.session))
admin.add_view(ModelView(TacGia, db.session))
admin.add_view(ModelView(NhaXuatBan, db.session))
admin.add_view(ModelView(User, db.session))