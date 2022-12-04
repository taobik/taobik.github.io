function them_hang(id, name, gia){
    event.preventDefault()

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

        let dem = document.getElementById('gio')
        dem.innerText = data.total_quantity
    }).catch(function(err) {
        console.error(err)
    })
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