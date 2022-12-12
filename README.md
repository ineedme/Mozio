git # Mozio

## Prompt

As Mozio expands internationally, we have a growing problem that many transportation suppliers we'd like to integrate cannot give us concrete zip codes, cities, etc that they serve.
To combat this, we'd like to be able to define custom polygons as their "service area" and we'd like for the owners of these shuttle companies to be able to define and alter their polygons whenever they want, eliminating the need for mozio employees to do this boring grunt work.


## Requirement
- Build a JSON REST API with CRUD operations for Provider (name, email, phone number, language an currency) and ServiceArea (name, price, geojson information)
- Create a specific endpoint that takes a lat/lng pair as arguments and return a list of all polygons that include the given lat/lng. 
- The name of the polygon, provider's name, and price should be returned for each polygon. This operation should be FAST
- Use unit tests to test your API
- Write up some API docs (using any tool you see fit)
- Create a Github account (if you don’t have one), push all your code and share the link with us
- Deploy your code to a hosting service of your choice. Mozio is built entirely on AWS, so bonus points will be awarded for use of AWS.

## Considerations

- All of this should be built in Python/DjangoRest. 
- Use any extra libraries you think will help, choose whatever database you think is best fit for the task, and use caching as you see fit.
- Ensure that your code is clean, follows standard PEP8 style (though you can use 120 characters per line) and has comments where appropriate.
- It should take you 8-10 hours to complete 
- We will not look at any attachments, screenshots or files sent by you, only Github and your deployed server.


## Brief
Based on the requirements, I must built a runnable server quickly.
I picked Python 3.10, Django 4.1, and Django REST Framework with GIS support because they come with a lot of functionality right out of the box.
Django has an ORM to work with many databases, I'm using Postgres because It has mature spatial features.
Created resources for Providers and Screen Area and used the HTTP Verbs implementing CRUD functions.
I used Django Cache to caching the endpoint get_providers_in_the_area results for 2 hours and avoid repeated heavy requests.
Deployed on AWS EC2 and Postgres RDS as requested in the requirements.


## Documentation
see Redoc API Documentation [http://ec2-3-139-99-66.us-east-2.compute.amazonaws.com:8000/](http://ec2-3-139-99-66.us-east-2.compute.amazonaws.com:8000/)

## Demo
see Demo [http://ec2-3-139-99-66.us-east-2.compute.amazonaws.com:8000/api/v1/](http://ec2-3-139-99-66.us-east-2.compute.amazonaws.com:8000/api/v1/)
