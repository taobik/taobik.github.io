function them_hang(id, name, gia){
    event.preventDefault()

    alert("Đã thêm vào giỏ hàng");
    fetch('/api/add-cart', {
        method: 'post',
        body: JSON.stringify ({
            'id': id,
            'name': name,
            'gia': gia,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then((data) => {
        console.info(data)

        let dem = document.getElementsByClassName('gio')
        for (let i = 0; i < dem.length; i++)
            dem[i].innerText = data.total_quantity
    }).catch(function(err) {
        console.error(err)
    })
}

function up_hang(id, p){
    fetch('/api/update-cart', {
        method: 'put',
        body: JSON.stringify ({
            'id': id,
            'so_luong': parseInt(p.value),
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let dem = document.getElementsByClassName('gio')
        for (let i = 0; i< dem.length; i++)
            dem[i].innerText = data.total_quantity

        let tong = document.getElementById('tong-tien')
        tong.innerText = new Intl.NumberFormat().format(data.total_amount)
    })
}


function xoa_hang(id){
    if (confirm("Bạn chắc chắn xóa sản phẩm?") == true){
    fetch('/api/xoa_hang/' + id, {
        method: 'delete',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let dem = document.getElementsByClassName('gio')
        for (let i = 0; i< dem.length; i++)
            dem[i].innerText = data.total_quantity

        let tong = document.getElementById('tong-tien')
        tong.innerText = new Intl.NumberFormat().format(data.total_amount)

        let e = document.getElementById("sanpham" + id)
        e.remove()

    }).catch(err => console.error(err))
}
}


function pay() {
    if (confirm("Bạn chắc chắn thanh toán không?") == true) {
        fetch('/api/pay',{
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.code == 200)
                location.reload()
        }).catch(err => console.error(err))
    }
}