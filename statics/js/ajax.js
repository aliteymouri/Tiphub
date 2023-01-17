function like(slug, id) {
    var like = document.getElementById("like_button")
    var count_like = document.getElementById("count_like")
    $.get(`/like/${slug}/${id}`).then(response => {
        if (response['response'] === 'liked') {
            like.className = "fa fa-heart"

        } else {
            like.className = "fa fa-heart-o"

        }
    })
}


function favorite(slug, id) {
    var like = document.getElementById("fav_button")
    $.get(`/favorite/${slug}/${id}`).then(response => {
        if (response['response'] === 'added') {
            like.className = 'fa fa-bookmark'
            Swal.fire({
                position: 'top-end-right',
                icon: 'success',
                text: 'این آموزش به علاقه مندی های شما اضافه شد',
                showConfirmButton: false,
                confirmButtonColor: '#112031',
                timer: 1500
            })

        } else {
            like.className = "fa fa-bookmark-o"

        }
    })
}









