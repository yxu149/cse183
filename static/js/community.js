// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        login_status: "out",
        user: "",
        user_id: "",
        add_status: false,
        post_content: "",
        posts: [],
        rater_up_status: 'none',
        rater_down_status: 'none',
        person_num: 1,
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.set_add_status = function (new_status) {
        app.vue.add_status = new_status; 
        app.vue.post_content = "";
    }

    app.add_post = function () {
        axios.post(add_post_url, {
            post_content: app.vue.post_content,
        }).then(function (response) {
            //TODO: 判断image是否为空，空着加入默认头像，否则加入post_user头像
            if (response.data.post[0].post_user_image == "") {
                temp_image = "";    //TODO: 还未加入默认头像，！！！！！！！！！！！！！！！！！！！！！！！！！！！
            } else {
                temp_image = response.data.post[0].post_user_image
            }
            app.vue.posts.push({
                post_id: response.data.post[0].id,
                user_id: response.data.post[0].user_id,
                post_content: app.vue.post_content,
                post_username: response.data.post[0].post_username,
                post_user_image: temp_image,
            });
            app.enumerate(app.vue.posts);
            app.vue.post_content = "";
            app.vue.add_status = false;
            app.init( );
        });
    }

    app.delete_post = function(row_idx) {
        let id = app.vue.posts[row_idx].id;
        axios.get(delete_post_url, {params: {id: id}}).then(function(response) {
            for(let i = app.vue.posts.length-1; i >= 0; i--) {
                if(app.vue.posts[i].id === id) {
                    app.vue.posts.splice(i, 1);
                    app.enumerate(app.vue.posts);
                    break;
                }
            }
        });
    };

    app.complete = (rows) => {
        rows.map((row) => {
            row.up_rating_status=false;
            row.down_rating_status=false;

            row.up_rating_status_display=false;
            row.down_rating_status_display=false;
        })
    };

    app.set_up_rating_status = function (row_idx, rating_status) {
        let row = app.vue.posts[row_idx];
        let id = row.id;
        if ( row.up_rating_status==true ) {
            row.rater_status_up = "none";
        } else {
            row.rater_status_up = "up";
            //当点击了赞后立马更新多少人点了赞
            axios.get(person_number_url, {params: {id: id, status: "up"}})
            .then(function (response) {
                app.vue.person_num = response.data.person_num+1;
            });
        }
        row.up_rating_status = !rating_status;
        row.up_rating_status_display = row.up_rating_status;
        if( row.down_rating_status == true && row.down_rating_status_display == true) {
            row.down_rating_status = false;
            row.down_rating_status_display = false;
        }
        axios.post(set_rating_url,
        {
            post_id: row.id,
            rating_up: row.up_rating_status,
            rating_down: row.down_rating_status,
        }).then((response) => {
            row.liked_user_name = response.data.liked_user_Name;
            row.disliked_user_name = response.data.disliked_user_Name;
        })
    }

    app.set_down_rating_status = function(row_idx, rating_status) {
        let row = app.vue.posts[row_idx];
        let id = row.id;
        if ( row.down_rating_status==true ) {
            row.rater_status_down = "none";
        } else {
            row.rater_status_down = "down";
            //当点击了踩后立马更新多少人点了踩
            axios.get(person_number_url, {params: {id: id, status: "down"}})
            .then(function (response) {
                app.vue.person_num = response.data.person_num+1;
            });
        }
        row.down_rating_status = !rating_status;
        row.down_rating_status_display = row.down_rating_status;
        if( row.up_rating_status == true && row.up_rating_status_display == true) {
            row.up_rating_status = false;
            row.up_rating_status_display = false;
        }
        axios.post(set_rating_url,
        {
            post_id: row.id,
            rating_up: row.up_rating_status,
            rating_down: row.down_rating_status,
        }).then((response) => {
            row.liked_user_name = response.data.liked_user_Name;
            row.disliked_user_name = response.data.disliked_user_Name;
        })
    };

    app.mouse_up_in = function(row_idx) {
        let row = app.vue.posts[row_idx];
        let id = row.id;
        row.rater_status_up='up';
        app.vue.rater_up_status = row.rater_status_up;
        //判断有多少人点击了赞
        axios.get(person_number_url, {params: {id: id, status: "up"}})
            .then(function (response) {
                app.vue.person_num = response.data.person_num;
            });
    };

    app.mouse_up_out = function(row_idx) {
        let row = app.vue.posts[row_idx];
        row.rater_status_up='none';
        app.vue.rater_up_status = row.rater_status_up;
    };

    app.mouse_down_in = function(row_idx) {
        let row = app.vue.posts[row_idx];
        let id = row.id;
        row.rater_status_down='down';
        app.vue.rater_down_status = row.rater_status_down;
        //判断有多少人点击了踩
        axios.get(person_number_url, {params: {id: id, status: "down"}})
        .then(function (response) {
            app.vue.person_num = response.data.person_num;
        });
    };

    app.mouse_down_out = function(row_idx) {
        let row = app.vue.posts[row_idx];
        row.rater_status_down='none';
        app.vue.rater_down_status = row.rater_status_down;
    };

    // This contains all the methods.
    app.methods = {
        set_add_status: app.set_add_status,
        add_post: app.add_post,
        delete_post: app.delete_post,
        complete: app.complete,
        set_up_rating_status: app.set_up_rating_status,
        set_down_rating_status: app.set_down_rating_status,
        mouse_up_in: app.mouse_up_in,
        mouse_up_out: app.mouse_up_out,
        mouse_down_in: app.mouse_down_in,
        mouse_down_out: app.mouse_down_out,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        axios.get(load_community_url)
            .then(function (response) {
                if (response.data.user.length < 1) {
                    app.vue.login_status = "out";
                } else {
                    app.vue.login_status = "in";
                }
                app.complete(response.data.posts);
                app.vue.user = response.data.user;
                app.vue.user_id = response.data.user_id;
                app.vue.posts = response.data.posts;
                app.enumerate(app.vue.posts);
                //如果当前用户登录则进入，否则不进入。 进入后检查用户的头像是否为空，如果不为空寻找相应帖子并且更新头像。
                if(app.vue.user.length > 0) {
                    if (app.vue.user[0].user_image != null) {
                        for(let i = 0; i < app.vue.posts.length; i++){
                            if (app.vue.posts[i].user_id == app.vue.user_id) {
                                app.vue.posts[i].post_user_image = app.vue.user[0].user_image;
                                axios.post(update_image_url,{
                                    id: app.vue.posts[i].id,
                                    image: app.vue.posts[i].post_user_image
                                }).then();
                            }
                        }
                    }
                }
            }).then(() => {
                for (let row of app.vue.posts) {
                    axios.get(get_rating_url, {params: {"row_id": row.id}})
                    .then((result) => {
                        row.up_rating_status=result.data.rating_up;
                        row.down_rating_status=result.data.rating_down;
                        row.up_rating_status_display=row.up_rating_status;
                        row.down_rating_status_display=row.down_rating_status;
                        app.vue.$forceUpdate();
                    });
                }
            });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
