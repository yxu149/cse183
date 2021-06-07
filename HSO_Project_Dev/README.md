README.md

Qihang Huang -qhuang24@ucsc.edu - 1591526
Valentina Tang - xtang21@ucsc.edu - 1663512
Sijia Zhong - szhong16@ucsc.edu - 1690286
Yanwen Xu - yxu149@ucsc.edu - 1662432

Yanwen Xu: 
Main Project Designing & Idea Generating
Website & Domain Management & Deployment
Database Management
Developments on Community Functions & User Profile Page
Catch-all Issue Resolving Specialist

Qihang Huang: 
Database Designing
vue.js Developments 
Backend Developments
Developments on Community Functions & Product  & main store page

Valentina Tang: 
vue.js Developments
Front-end Developments 
Developer on Cart & Store Functions
Communications Director

Sijia Zhong: 
Product Manager
Operations Director
PR and Outreach
UI Design & Beautifications
Co-developer on Cart & Store Functions


Files
Index.html, Index.js
Main page of the project, visitors can view this page without logging in. This main page summarizes the introduction of this website and you will be able to take a look at the items people are selling. There’s also a search bar where you can look for specific products. Tabs on the top left hand corner can direct you to different pages(Store, Community, Profile, Wishlist) to see more specific information.
Layout.html
The file for designing how the navigation bar will look like. By changing this file, we can have a directory of html on the navigation bar. 
Community.html, Community.js
The page for the community of our users. In this page, we have all the community posts which come from our users. And users can always click on the add button for adding a new post. We met the problem when we tried to do this. We cannot delete the post but now it is solved. 
Manage_products.html, Manage_product.js
This page enables users to register and edit the product they want to sell. By clicking on the “add product button” there will be a chart where you can put product information(product name, quantity, price, and description) and after you fill in the chart. You can click on the “add” button and then product information will be stored and displayed on the main page and in the store page. There’s also an upload image button after you register the product(you can only upload images smaller than 40KB). If you want you can add more than one image.
Registration.html
This is a page set inside of the user profile page. All the users can click on the edit button on the user profile to get to this page. In this page, it can change the user’s information. Users can update their info by this page. 
Show_product.html, Show_product.js
This will generate all the information of one product. If this product has multiple images, we can switch the current showing page on the product detail by clicking on a different image of this product. You can also post to discuss what you thought of the product with other users. 
User_profile.html, User_profile.js
This page is a profile page. In this page, users can see all the info about themselves or other people. We have some contents here, one is the product for sale and the other is a community post. Users can see what they are selling or what other people are selling on their profile page. And also can see what this person posts in the community. When we implement this, we meet some problems like the contents it might show from other users, or it just cannot show the contents. 
Visitor.html, Visitor.js
If a non-registered user visits the website they will be able to view product information and community. They can also access the seller's profile to directly contact them even though they haven’t registered.
Wishlist.html, Wishlist.js
The wishlist page for all users. People might forget what they found before. They will always go back to the website and think about what I just found before. People can save the product they like here. If the user didn’t add anything to their wishlist then a message will be displayed to tell them.

Backend
Controllers.py
The controller is used to control each connection as a whole, as the center for integrating all content. It is an indispensable part. Each function that obtains the database needs to be connected through the controller and the data is obtained through the controller to return your data.
Models.py
	We totally have 3 basic databases and 10 extra databases. We use different databases on different tables. Beside what professor gives us for the 3 basic databases, we have tables of user, user option info, product, more_image. product_post, user_rate_it, post, thumbs, rater_person, wishlist. Table of users contains basic info of a user. Table of user_option_info which is linked with the users table contains the extra info of a user like what we can add on the profile page. Table of products contains the info of a product like what it will show on the profile page or the main page. The more_image table and the product_post table are connected with the product table. More_image is for adding more than one image, and product_post is for the comment in the detail page. User_rate_it and post and thumbs and rater_person are used in community.html. It will show which user posted this community post and how many people like this post or dislike it. The wishlist table is for creating a wishlist for people to save what they found on this website, to remember the items they like for them. Wishlist table is linked with the product because we need to add a product inside. 

We met a lot of problems when we deployed this. We have problems with the post on community.html that cannot be deleted. Or it just cannot be saved after you actually click delete. We also met problems like the website cannot be signin and we try to solve all those problems. 
Our website is fully functional locally, but after deployment, it always gives us some new bugs. When we were doing database docking, we clearly realized the role of database type for storing data. For example: when I want to save boolean in mysql, because the type of mysql boolean is given, it cannot connect with the local database. Because the local database gave mysql a string type ‘T’. But in fact, mysql can only recognize true and false without knowing what ‘T’ represents.  We still really try hard to solve the problems and work together. Hope you guys will like it and thank you for your time no matter reading this file or watching our presentation or testing our website. Thanks for all the work done by everyone. 

Version tracking log can be found at Sijia's Repo at https://github.com/szhong16/CSE183-Final-Project
