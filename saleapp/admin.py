from saleapp import app, db
from saleapp.models import Sach, TheLoai, TacGia, NhaXuatBan, User, UserRole
from flask_admin import BaseView, expose, Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect
import utils


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.vai_tro.__eq__(UserRole.admin)


class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', info=utils.load_tl())


admin = Admin(app=app,
              name="Quan ly nha sach",
              template_mode="bootstrap4",
              index_view=MyAdminIndex())
admin.add_view(AuthenticatedModelView(Sach, db.session))
admin.add_view(AuthenticatedModelView(TheLoai, db.session))
admin.add_view(AuthenticatedModelView(TacGia, db.session))
admin.add_view(AuthenticatedModelView(NhaXuatBan, db.session))
admin.add_view(AuthenticatedModelView(User, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))