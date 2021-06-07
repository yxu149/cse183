// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        user: [],
        show_items_status: false,
        items: [],
        show_community_status: false,
        posts: [],
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

    app.upload_file = function (event) {
        let input = event.target;
        let file = input.files[0];
        if(file) {
            let reader = new FileReader();
            reader.addEventListener("load", function () {
                let image = reader.result;
                axios.post(upload_user_image_url,
                    {
                        image: image,
                    }).then(function () {
                        app.vue.user.user_image = image;
                        app.vue.$forceUpdate()
                    });
            });
            reader.readAsDataURL(file);
        }
    }

    app.init_item_status = function () {
        show_items_status = false;
        show_community_status = false;
    }

    app.show_items = function () {
        console.log("user_profile:", app.vue.user.user_id);
        axios.get(show_items_url, {params: {user_id: app.vue.user.user_id}})
            .then(function (response) {
                app.vue.show_items_status = !app.vue.show_items_status;
                if (app.vue.show_community_status == true) {
                    app.vue.show_community_status = false;
                }
                app.vue.items = response.data.products;
            });
    }

    app.show_community_post = function () {
        axios.get(show_community_status_url, {params: {user_id: app.vue.user.user_id}})
            .then(function (response) {
                app.vue.show_community_status=!app.vue.show_community_status;
                if (app.vue.show_items_status == true) {
                    app.vue.show_items_status = false;
                }
                app.vue.posts = response.data.posts;
                app.enumerate(app.vue.posts);
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

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        upload_file: app.upload_file,
        show_items: app.show_items,
        show_community_post: app.show_community_post,
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
        axios.get(load_Info_url).then(function (response) {
            app.vue.user = response.data.user;
            console.log(app.vue.user);
            console.log(app.vue.user.user_id);
        });
        app.init_item_status();
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
