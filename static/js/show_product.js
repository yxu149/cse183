 // This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        products: [],
        images: [],
        add_status: false,
        login_status: "out",
        post_content: "",
        posts: [],
        user: "",
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };


    app.annotate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {
            e._idx = k++;
            e.fprice = e.price.toLocaleString(
                undefined, { minimumFractionDigits: 2,
                    maximumFractionDigits: 2 }
            );
        });
        return a;
    };

    app.set_default_status = (a) => {
        // This adds an _idx field to each element of the array.
        a.map((e) => {e.status = false;});
        return a;
    };

    app.set_image_status = function (image_idx) {
        let image = app.vue.images[image_idx];
        for(let i of app.vue.images) {
            i.status = false;
        }
        image.status = !image.status;
        app.vue.$forceUpdate()
    }

    app.set_add_status = function (new_status) {
        app.vue.add_status = new_status; 
        app.vue.post_content = "";
    }

    app.add_post = function () {
        axios.post(add_product_post_url, {
            post_content: app.vue.post_content,
        }).then(function (response) {
            //TODO: 判断image是否为空，空着加入默认头像，否则加入post_user头像
            if (response.data.post[0].post_user_image == "") {
                temp_image = "";    //TODO: 还未加入默认头像，！！！！！！！！！！！！！！！！！！！！！！！！！！！
            } else {
                temp_image = response.data.post[0].post_user_image
            }
            app.vue.posts.push({
                id: response.data.post[0].id,
                user_id: response.data.post[0].user_id,
                post_content: app.vue.post_content,
                post_username: response.data.post[0].post_username,
                post_user_image: temp_image,
            });
            app.enumerate(app.vue.posts);
            app.vue.post_content = "";
            app.vue.add_status = false;
            app.vue.$forceUpdate()
        });
    }

    app.delete_post = function(row_idx) {
        let id = app.vue.posts[row_idx].id;
        axios.get(delete_product_post_url, {params: {id: id}}).then(function(response) {
            for(let i = app.vue.posts.length-1; i >= 0; i--) {
                if(app.vue.posts[i].id === id) {
                    app.vue.posts.splice(i, 1);
                    app.enumerate(app.vue.posts);
                    break;
                }
            }
        });
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        set_image_status: app.set_image_status,
        set_add_status: app.set_add_status,
        add_post: app.add_post,
        delete_post: app.delete_post,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        // Put here any initialization code.
        // Typically this is a server GET call to load the data.
        axios.get(load_product_detail_url)
            .then(function (response) {
                if (response.data.user.length < 1) {
                    app.vue.login_status = "out";
                } else {
                    app.vue.login_status = "in";
                }
                app.vue.products = response.data.product_detail;
                if (app.vue.products.length > 0) {
                    if (app.vue.products[0].image != null){
                        app.vue.images.push({
                            id: app.vue.products[0].id,
                            more_image: app.vue.products[0].image,
                            product_id: 0,
                        });
                    }
                }
                app.vue.posts = response.data.posts;
                app.vue.user = response.data.user;
                app.enumerate(app.vue.posts);
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
                app.vue.images = app.vue.images.concat(response.data.more_image);
                app.set_default_status(app.vue.images);
                app.enumerate(app.vue.images);
                app.vue.images[0].status = true;
            });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
