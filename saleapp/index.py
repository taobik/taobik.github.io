from flask import session
from saleapp import login, controller
from saleapp.admin import *


app.add_url_rule("/", "home", controller.home)
app.add_url_rule("/sanpham", "san_pham", controller.san_pham)
app.add_url_rule("/chitietsanpham/<int:id_sp>", "chitiet", controller.chitiet)
app.add_url_rule("/dangky", "dangky", controller.dangky, methods=['get', 'post'])
app.add_url_rule("/danhnhap", "dangnhap", controller.dangnhap, methods=['get', 'post'])
app.add_url_rule("/admin-login", "dangnhap_admin", controller.dangnhap_admin, methods=['post', 'get'])
app.add_url_rule("/dangxuat", "dangxuat", controller.dangxuat)
app.add_url_rule("/cart", "gio_hang", controller.gio_hang)
app.add_url_rule("/api/add-cart", "them_hang", controller.add_to_cart, methods=['post'])
app.add_url_rule("/api/update-cart", "up_hang", controller.update_cart, methods=['put'])
app.add_url_rule("/api/xoa_hang/<id_sp>", "xoa_hang", controller.xoa_hang, methods=['delete'])
app.add_url_rule("/api/pay", "thanh_toan", controller.pay, methods=['post'])
app.add_url_rule("/api/chitietsanpham/<int:sach_id>/comment", "comments", controller.comments, methods=['get'])
app.add_url_rule('/api/chitietsanpham/<int:sach_id>/comment', "add_comment", controller.add_comment, methods=['post'])


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.context_processor
def common_response():
    return {
        'cart_stats': utils.cart_stats(session.get('cart'))
    }


if __name__ == '__main__':
    app.run(debug=True)
