// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {


    // This is the Vue data.
    app.data = {
        fields: [
            ['Product Name', 'product_name'],
            ['Quantity', 'quantity'],
            ['Price', 'price'],
            ['Description', 'description'],
        ],
        add_fields: {},
        add_mode: false,
        rows: [],
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    // This decorates the rows (e.g. that come from the server)
    // adding information on their state:
    // - clean: read-only, the value is saved on the server
    // - edit : the value is being edited
    // - pending : a save is pending.
    app.decorate = (a) => {
        for (e of a) {
            e._state = {}
            for (f of app.vue.fields) {
                e._state[f[1]] = "clean";
            }
        }
        return a;
    }

    app.add_product = function () {
        msg = {};
        for (f of app.vue.fields) {
            msg[f[1]] = app.vue.add_fields[f[1]];
        }
        axios.post(add_url, msg).then(function (response) {
            let n = app.vue.rows.length;
            app.vue.rows.push();
            msg.id = response.data.id;
            msg.image = null; // For reactivity on it.
            msg._state = {};
            for (let f of app.vue.fields) {
                msg._state[f[1]] = "clean";
            }
            msg._idx = n;
            app.vue.rows.push(msg);
            app.reset_form();
            app.set_add_status(false);
        });
    };

    app.reset_form = function () {
        for (f of app.vue.fields) {
            app.vue.add_fields[f[1]] = "";
        }
    };

    app.delete_product = function(row_idx) {
        let id = app.vue.rows[row_idx].id;
        axios.get(delete_url, {params: {id: id}}).then(function (response) {
            for (let i = 0; i < app.vue.rows.length; i++) {
                if (app.vue.rows[i].id === id) {
                    app.vue.rows.splice(i, 1);
                    app.enumerate(app.vue.rows);
                    break;
                }
            }
            });
    };

    app.set_add_status = function (new_status) {
        app.vue.add_mode = new_status;
    };

    app.start_edit = function (row_idx, fn) {
        let row = app.vue.rows[row_idx];
        app.vue.rows[row_idx]._state[fn] = "edit";
    };

    app.stop_edit = function (row_idx, fn) {
        let row = app.vue.rows[row_idx];
        if (row._state[fn] === "edit") {
            row._state[fn] = "pending";
            axios.post(edit_url,
                {
                    id: row.id,
                    field: fn,
                    value: row[fn], // row.first_name
                }).then(function (result) {
                row._state[fn] = "clean";
            });
        }
        // If I was not editing, there is nothing that needs saving.
    }

    app.upload_file = function (event, row_idx) {
        let input = event.target;
        let file = input.files[0];
        let row = app.vue.rows[row_idx];
        if (file) {
            let reader = new FileReader();
            reader.addEventListener("load", function () {
                // Sends the image to the server.
                let image = reader.result;
                axios.post(upload_url,
                    {
                        product_id: row.id,
                        image: image,
                    })
                    .then(function () {
                        // Sets the local preview.
                        row.image = image;
                    });
            });
            reader.readAsDataURL(file);
        }
    };

    app.add_more = function (event, row_idx) {
        let input = event.target;
        let file = input.files[0];
        let row = app.vue.rows[row_idx];
        if (file) {
            let reader = new FileReader();
            reader.addEventListener("load", function () {
                // Sends the image to the server.
                let more_image = reader.result;
                axios.post(add_more_url,
                    {
                        product_id: row.id,
                        more_image: more_image,
                    })
                    .then(function () {
                        // Sets the local preview.
                        if (row.more_image != null){
                            row.more_image = row.more_image.concat(more_image);
                        } else {
                            row.more_image = [more_image];
                        }
                        app.vue.$forceUpdate()
                    });
            });
            reader.readAsDataURL(file);
        }
    };

    app.load_image = function(row_idx) {
        let row = app.vue.rows[row_idx];
        axios.get(load_image_url, {params: {product_id: row.id}})
            .then(function (response) {
                if (row.more_image != null){
                    console.log(response.data.more_image);
                    for (let image of response.data.more_image){
                        row.more_image = row.more_image.concat(image.more_image);
                    }
                } else {
                    for (let image of response.data.more_image){
                        row.more_image = [image.more_image];
                    }
                    console.log(row.more_image);
                }
                app.vue.$forceUpdate()
            })
    }

    // We form the dictionary of all methods, so we can assign them
    // to the Vue app in a single blow.
    app.methods = {
        add_product: app.add_product,
        set_add_status: app.set_add_status,
        delete_product: app.delete_product,
        start_edit: app.start_edit,
        stop_edit: app.stop_edit,
        upload_file: app.upload_file,
        add_more: app.add_more,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    // Generally, this will be a network call to the server to
    // load the data.
    // For the moment, we 'load' the data from a string.
    app.init = () => {
        for (let f of app.vue.fields) {
            app.vue.add_fields[f[1]] = "";
        }
        axios.get(load_url).then(function (response) {
            app.vue.rows = app.decorate(app.enumerate(response.data.rows));
            for (let row of app.vue.rows) {
                app.load_image(row._idx);
            }
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);