from saleapp import app, db
from saleapp.models import Sach, TheLoai, TacGia, NhaXuatBan, User, UserRole
from flask_admin import BaseView, expose, Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect, request
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


class ThongKe(BaseView):
    @expose('/')
    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        kwtl = request.args.get('kwtl')
        from_datetl = request.args.get('from_datetl')
        to_datetl = request.args.get('to_datetl')
        return self.render('admin/thongkebaocao.html',
                           sach=utils.load_dtthang_sp(kw=kw,
                                                      to_date=to_date,
                                                      from_date=from_date),
                           tl=utils.load_dtthang_tl(kw=kwtl,
                                                    to_date=to_datetl,
                                                    from_date=from_datetl))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.vai_tro == UserRole.admin


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
admin.add_view(ThongKe(name='Thống kê báo cáo'))
admin.add_view(AuthenticatedModelView(User, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))