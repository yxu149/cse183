// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        userName: '',
        wishlist: [],   //TODO: This contain the information of wishlist database.
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

    app.delete_wishlist = function (row_idx) {
        let id = app.vue.wishlist[row_idx].id;
        axios.get(delete_wishlist_url, {params: {id: id}}).then(function (response) {
            for(let i = app.vue.wishlist.length-1; i >= 0; i--) {
                if(app.vue.wishlist[i].id === id) {
                    app.vue.wishlist.splice(i, 1);
                    app.enumerate(app.vue.wishlist);
                    break;
                }
            }
        })
    }

    app.get_username = function () {
        axios.get(get_username_url)
            .then(function (result) {
                app.vue.userName = result.data.userName;
                if(result.data.userName == ""){
                    app.vue.login_status = 'out';
                } else {
                    app.vue.login_status = 'in';
                }
            });
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        get_username: app.get_username,
        delete_wishlist: app.delete_wishlist
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
        app.get_username();
        axios.get(load_wishlist_url)
            .then(function (response) {
                app.vue.wishlist = response.data.wishlist;
                app.enumerate(app.vue.wishlist);
            });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
