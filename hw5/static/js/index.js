// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        add_mode: false,
        write_post: "",
        rows : [],

    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };


    app.add_post = function(){
        axios.post(add_post_url,
            {post: app.vue.write_post,
            }).then(function(response) {
                app.vue.rows.push({
                    id: response.data.id,
                    post: app.vue.write_post,
                });
                app.enumerate(app.vue.rows);
                app.reset_form();
                app.set_add_status(false);
        })
    };

    app.reset_form = function(){
        app.vue.write_post = "";

    }

    app.set_add_status = function(new_status){
        app.vue.add_mode = new_status;

    };

    app.delete_post = function(row_idx){
        let id = app.vue.rows[row_idx].id;
        axios.get(delete_post_url, {params: {id: id}}).then(function(response){
            for(let i = 0; i < app.vue.rows.length; i++){
                if(app.vue.rows[i].id){
                    app.vue.rows.splice(i,1);
                    app.enumerate(app.vue.rows);
                    break;
                }
            }
        });

    };
    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.

        add_post: app.add_post,
        set_add_status: app.set_add_status,
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
        axios.get(load_post_url).then(function(response){
           app.vue.rows=app.enumerate(response.data.rows);
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
