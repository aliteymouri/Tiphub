function like(slug, id) {
    var like = document.getElementById("like_button")
    var count_like = document.getElementById("count_like")
    $.get(`/like/${slug}/${id}`).then(response => {
        if (response['response'] === 'liked') {
            like.className = "fa fa-heart liked"
            count_like.innerText = Number(count_like.innerText) + 1

        } else {
            like.className = "fa fa-heart-o"
            count_like.innerText = Number(count_like.innerText) - 1

        }
    })
}




