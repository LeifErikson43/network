document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#post_form').onsubmit = submit_post;

    document.querySelector('#post_submit').disabled = true;

    document.querySelector('#write_post').onkeyup = () => {
        if (document.querySelector('#write_post').value.length > 0) {
            document.querySelector('#post_submit').disabled = false;
        } else {
            document.querySelector('#post_submit').disabled = true;
        }
        
    }

    load_posts();
});


function submit_post() {
    fetch('/posts', {
        method: 'POST',
        body: JSON.stringify({
            post_txt : document.querySelector('#write_post').value
        })
    })
    .then(response => response.json())
    .then(result => {
      if ((result.error !== 201) && (result.error !== undefined)) {
        alert(result.error);
       } else {
          alert("Post was sent.");
          load_posts();    
          }
    })
}


function load_posts() {
    document.querySelector('#all_post_view').style.display = 'block';
    document.querySelector('#profile_view').style.display = 'none';
}

function change_like(post_id, user, action) {
    let actionNeeded = action.getAttribute("data-like-action");
    console.log(post_id);
    console.log(user);
    console.log(actionNeeded);
    if (actionNeeded == "unlike"){
        console.log("you need to unlike this one")
    }

    if (actionNeeded != "like") {
        console.log('you need to unlike this one')
        url = '/unlikes/' + post_id
        console.log(url)
        fetch('/unlikes/'+post_id, {
            method: 'PUT'
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)    
            post_likes = document.querySelector(`#like${data.post_id}`)
            post_likes.setAttribute("data-like-action", "like")
            post_likes.innerHTML = '&#9825;'
            likeNUM = document.querySelector(`#like_num${data.post_id}`)
            likeNUM.innerHTML = `Likes ${data.value}`

        })
    } else {
        console.log('you need to like this one')
        url = '/likes/' + post_id
        console.log(url)
        fetch('/likes/'+post_id, {
            method: 'PUT'
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)   
            post_likes = document.querySelector(`#like${data.post_id}`)
            post_likes.setAttribute("data-like-action", "unlike")
            post_likes.innerHTML = '&#9829;'
            likeNUM = document.querySelector(`#like_num${data.post_id}`)
            likeNUM.innerHTML = `Likes ${data.value}`

        })
    }

    }

    function change_follow(poster_id, user, action) {
        let actionNeeded = action.getAttribute("data-follow-action");
        console.log(`you need to ${actionNeeded} `)
        console.log(poster_id);
        console.log(user);
        console.log(actionNeeded);
        if (actionNeeded != "follow"){
            url = `/unfollow/${poster_id}`
            fetch('/unfollow/'+poster_id, {
                method: 'PUT'
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                follow_button = document.querySelector(".follow_btn");
                follow_button.setAttribute("data-follow-action", "follow");
                follow_button.innerHTML = "follow";
                follow_count = document.querySelector("#followCount");
                follow_count.innerHTML = `${data.follow_count} followers`;

            })
        }

        else {
            url = `/follow/${poster_id}`
            fetch('/follow/'+poster_id, {
                method: 'PUT'
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                follow_button = document.querySelector(".follow_btn");
                follow_button.setAttribute("data-follow-action", "unfollow");
                follow_button.innerHTML = "unfollow";
                follow_count = document.querySelector("#followCount");
                follow_count.innerHTML = `${data.follow_count} followers`;

            })
        }

    }

function edit(post_id) { 
    let text_info = document.querySelector(`#post_text${post_id}`).innerHTML;
    console.log(text_info);

    document.querySelector(`#post_text${post_id}`).style.display = 'none';
    document.querySelector(`#edit_post_text${post_id}`).style.display = 'block';
    document.querySelector(`#edit_post_button${post_id}`).style.display = 'block';

    document.querySelector(`#edit_post_text${post_id}`).placeholder = `${text_info}`;
    
    let edit_text = document.querySelector(`#edit_post_text${post_id}`);
    let edit_button = document.querySelector(`#edit_post_button${post_id}`);

    edit_button.addEventListener('click', () => {
        fetch('/edit/'+post_id, {
            method: 'PUT',
            body: JSON.stringify({
                post: edit_text.value
            })
        });
        edit_text.style.display = 'none';
        edit_button.style.display = 'none';

        document.querySelector(`#post_text${post_id}`).style.display = 'block'
        document.querySelector(`#post_text${post_id}`).innerHTML = edit_text.value;

    })

    edit_text.value = "";
}

function delete_post(post_id) {
    if (confirm("Are you sure you want to Delete Post")){
        fetch('delete_post/'+post_id,{
        })
        .then(data => {
            console.log(data);
            let post_to_delete = document.querySelector(`#post_text${post_id}`);
            post_to_delete.parentElement.style.animationPlayState = 'running';
            post_to_delete.parentElement.addEventListener('animationend', () => {
            post_to_delete.parentElement.remove();
            })

        }) 
    }
    
}