# simple-manager

## Overview

![Simple Manager Diagram!](/resources/simple-manager.png "Simple Manager Diagram")

As shown in the diagram, there are three basic components:
- the front end is in `client` folder which is a single page application in Vue.js
- the back end is in `django-rest` folder which is a REST service in Django. It also serve the admin website
- the `invoice-receiver` folder contains only one python script to be run on AWS lambda. It is to be invoked by invoice emails and then create invoices.

## Development

To develop the web app locally, first check out the repository, and then:
1. Go to django-rest folder, follow the dev instructions there to launch the local django server;
2. In another terminal, go to the client folder and follow dev instructions there to launch the Vue dev server;
3. Then, you should be able to see the web app at http://localhost:8080

## Deployment
To deploy the web app, follow the deployment instructions in the three individual folders probably in the order: django-rest, client, invoice-receiver.

## Admin Operations

### Add a new user

You need to be super user to add a new user. First, login the admin site https://myapi.vanityart.com/admin and go to `Users` table and click `ADD USER` button. And then input username and password:
- The username should be the user's **email** with all **lower case letters**;
- You can set password randomly and do not need to remember it. Because you will tell the new user to use `forgot paswword` function to reset it.

And then, click the `SAVE` button which will direct you to the `Change user` page. Here, you need to:
- Input the **same email** with all **lower case letters** into `Email address` field;
- Super or Staff or Normal (you can also update this later)
  - to make a super user, who can login admin site add/update/delete `Users` table and all other tables as well, you need to check both `Staff status` and `Superuser status`;
  - to make a staff user, who can login admin site and manually modify records in tables other than `Users` table, you need to check `Staff status` but leave `Superuser status` unchecked;
  - to make a normal user, who cannot login admin site at all, you need to uncheck both `Staff status` and `Superuser status`
 
And then, click the `SAVE` button, and now the new user has been added. So now you also want to inform the new added user to get on https://manager.varnityart.com and reset the password and sign in.

### Delete a user

To delete a user, login admin site https://myapi.vanityart.com/admin and go to `Users` table and click the user you want to delete. And then you can do one of the following:
- Click the `DELETE` button which will delete the user from the database;
- Or you can uncheck `Active` checkbox, which will not delete the user but just the user cannot sign in anymore. This way you can bring the user back later.


