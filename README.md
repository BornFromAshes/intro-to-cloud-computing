# intro-to-cloud-computing

In this project, we implemented an ad registration service. The purpose of this project is to learn and work with cloud services; These services are used for different parts of the service, such as "database", "object-based storage", "image processing" and "email sending". <br>
Advertisements include all types of vehicles. Each user can send an advertisement of his vehicle in the form of a combination of text and image descriptions, along with his email address. Our service checks the registered ad in the first step. Each ad is placed in its corresponding category based on the type of vehicle in its image (car, motorcycle, bicycle, etc.). If the ad image does not contain any vehicle, the ad will be rejected. <br>
Finally, after processing the ad, the user will be notified of the result of his ad registration by sending an email. In this email, if the ad is approved, a link to the ad will be placed along with its category. If the ad is rejected, this will be mentioned in the email. <br>

## Description

Our software consists of two services. The first service is responsible for receiving user requests and responding to them. The second service has the task of processing (determining the category or rejecting the ad).

## First Service
This service consists of two APIs:
### Ad Registration API
1. This API receives the information of an ad, including text, image and sending email.
2. The information of this ad, including the text and the email address of the sender, is stored in the database and a unique identifier is considered for it.
3. Saves the image in an object storage. We choose the name of the image in this storage so that we can retrieve the image of an ad based on its identifiers.
4. Writes the ID of the ad for processing in the RabbitMQ queue.
5. As a response to the request, a message like "Your ad was registered with ID X" will be sent to the user.

### Ad receiving API
1. This API receives the ID of an ad.
2. If the ID related to an ad has not been checked, in response, a message like "Your ad is in the review queue" will be sent to the user.
3. If the ID related to an ad is rejected, a message like "Your ad was not approved" will be given in response.
4. If this ID corresponds to an approved ad, it will return the information of this ad including text, image, category and status in the response.

## Database schema
