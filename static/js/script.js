$(function () {

    // GET COOKIE INFO
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });//END COOKIE INFO

    // FEED LIKE BUTTON
    $("button.post-like").click(function () {
        var $like_button = $(this);
        var $like_count = $(this).parent().prev().children().first();
        var pid = $(this).attr("data-pid");

        $.get("/feed/posts/like/", {post_id: pid}, function (data) {
            var likes = data.num_likes + (data.num_likes > 1 ? " likes" : " like");

            if (data.status == 1) {
                $like_count.text(likes);
                $like_count.show();
                $like_button.html('<span class="glyphicon glyphicon-thumbs-down"></span> Unlike');
            }
            else if (data.status == 0) {
                if (data.num_likes > 0) {
                    $like_count.text(likes);
                    $like_count.show();
                }
                else {
                    $like_count.text("");
                    $like_count.hide();
                }
                $like_button.html('<span class="glyphicon glyphicon-thumbs-up"></span> Like');
            }
        });
    });

    $("button.comment-like").click(function () {
        var $like_button = $(this);
        var $like_count = $(this).parent().prev();
        var cid = $(this).attr("data-cid");

        $.get("/feed/comments/like/", {comment_id: cid}, function (data) {
            var likes = data.num_likes + (data.num_likes > 1 ? " likes" : " like");

            if (data.status == 1) {
                $like_count.text(likes);
                $like_count.show();
                $like_button.html('<span class="glyphicon glyphicon-thumbs-down"></span> Unlike');
            }
            else if (data.status == 0) {
                if (data.num_likes > 0) {
                    $like_count.text(likes);
                    $like_count.show();
                }
                else {
                    $like_count.text("");
                    $like_count.hide();
                }
                $like_button.html('<span class="glyphicon glyphicon-thumbs-up"></span> Like');
            }
        });
    });// END FEED LIKE BUTTON

    // SEARCH EXISTING FRIENDS
    $("#search_existing_friends").keyup(function () {
        var friendsData = $("#friends_data");
        var searchInput = $("#search_existing_friends").val();
        friendsData.hide();
        var searchResults = $("#search_results");

        if (searchInput === "") {
            searchResults.empty();
            friendsData.show();
        }
        else {
            $.post("/profile/search_friends", {searchInput: searchInput}, function (data) {
                if(data.friends.length > 0) {
                    searchResults.empty();
                    var uTemplate = $("#searched_friends_template").html();
                    var executeTemplate = _.template(uTemplate);

                    for (var i = 0; i < data.friends.length; i++) {
                        searchResults.append(executeTemplate({
                            friend: data.friends[i],
                            avatar: data.friends_profile_avatar[i]
                        }));
                    }
                }
                else{
                    searchResults.html('<h1>No results</h1>');
                }
            });
        }
    });// END SEARCH EXISTING FRIENDS

    // SEARCH NEW FRIENDS
    $("#search_new_friends").keyup(function(){
        var searchResults = $("#search_results");
        var searchInput =$("#search_new_friends").val();

        if (searchInput === ""){
            searchResults.html("<h1>No results</h1>");
        }
        else{
            $.post("/profile/find_friends", {search_input: searchInput}, function(data){
                if(data.usersMatched.length > 0){
                    searchResults.empty();
                    var uTemplate = $("#found_users_template").html();
                    var executeTemplate = _.template(uTemplate);
                    var isFriend = false;

                    for(var i=0; i<data.usersMatched.length; i++) {
                        _.contains(data.currentUserFriends, data.usersMatched[i].username) ? isFriend=true : isFriend=false;
                        searchResults.append(executeTemplate({
                            user: data.usersMatched[i],
                            userAvatar: data.usersMatchedAvatar[i],
                            isFriend: isFriend
                        }));
                    }
                }
                else searchResults.html("<h1>No results</h1>");
            });
        }
    });// END SEARCH NEW FRIENDS

    //ADD FRIEND OR UNFRIEND
    $("#search_results").on( "click", ".friends", function() {
        var friendId = $(this).attr("data-uid");

        $.get("/profile/edit_friendship/", {friend_id: friendId, action: "add"}, function(data){
            alert("Friend " + data.friendName + " added!");
            location.reload();
        });
    });
    $("#search_results").on( "click", ".not_friends", function() {
        var friendId = $(this).attr("data-uid");

        $.get("/profile/edit_friendship/", {friend_id: friendId, action: "remove"}, function(data){
            alert("Friend " + data.friendName + " removed!");
            location.reload();
        });
    });//END ADD FRIEND OR UNFRIEND


});// LOAD PAGE