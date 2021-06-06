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

    app.init_item_status = function () {
        show_items_status = false;
        show_community_status = false;
    }

    app.show_items = function () {
        axios.get(show_items_url, {params: {user_id: app.vue.user.id}})
            .then(function (response) {
                app.vue.show_items_status = !app.vue.show_items_status;
                if (app.vue.show_community_status == true) {
                    app.vue.show_community_status = false;
                }
                app.vue.items = response.data.products;
            });
    }

    app.show_community_post = function () {
        axios.get(show_community_status_url, {params: {user_id: app.vue.user.id}})
            .then(function (response) {
                app.vue.show_community_status=!app.vue.show_community_status;
                if (app.vue.show_items_status == true) {
                    app.vue.show_items_status = false;
                }
                app.vue.posts = response.data.posts;
                app.enumerate(app.vue.posts);
            });
    }


    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        show_items: app.show_items,
        show_community_post: app.show_community_post,
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
        axios.get(visitor_load_Info_url).then(function (response) {
            app.vue.user = response.data.user;
        });
        app.init_item_status();
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
