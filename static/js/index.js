// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        query: "",
        results: [],
        products: [],
        login_status: 'out',
        userName: '',
        text_status: 'None',   //text_status has two status: None and GET
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

    app.search = function () {
        axios.get(searchBar_url, {params: {q: app.vue.query}})
            .then(function(result) {
                app.vue.results = app.annotate(result.data.results);
                app.enumerate(app.vue.results)
            });
    };

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

    app.get_products = function () {
        axios.get(get_products_url)
            .then(function (response) {
                app.vue.products = response.data.products;
            });
    };

    app.add_wishlist = function (product_id, owner) {
        axios.post(add_wishlist_url, {
            product_id: product_id,
            product_owner: owner,
        }).then(function (response) {

        });
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        search: app.search,
        get_username: app.get_username,
        get_product: app.get_products,
        add_wishlist: app.add_wishlist,
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
        app.get_products();
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
