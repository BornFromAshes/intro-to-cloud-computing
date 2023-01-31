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

Our database consists of 6 rows:
- id(int) : A unique ID for every ad
- description(string) : Description of the ad given by the user
- email(string) : User's email
- state(string) : 3 different states : Pending, Accepted, Rejected
- category(string) : Photo's category, determing by Imagga
- path(string) : Photo's saved path

## Second Service
The task of this service is to read advertisements from the RabbitMQ queue, process them and save the result on the database.
1. This service is connected to the RabbitMQ queue and listens to new messages. Each message corresponds to a registered advertisement.
2. There is an advertisement ID in each message read from the queue. With this ID, the ad photo is received from the object storage.
3. The ad photo is sent to the photo tagging service for processing. From the response of the tagging service, the first tag is selected as the ad category and gets set as the category column of the database.
4. By using the email sending service, an email is sent to the user to inform the user of the status (approval or rejection) of his ad.

## Overall Schema
![image](https://user-images.githubusercontent.com/117355603/215842973-5be3fa36-2f58-42c1-ab92-98c67f15c4f4.png)

## Cloud Services Used
### Cloud Host
To implement this project, we must first have a host; A host is a computer system that has a static IP address and contains various security tools such as firewalls. Obviously, this computer should not be disabled in case of problems such as power failure. For this, we used the services of a cloud hosting provider.

### Database as a Service
Database as a Service (DBaaS) is a managed cloud computing service that provides access to the database without the need to set up physical hardware, install software, or configure the database. In this project, server B and A are supposed to work with the database.

### S3 Object Storage
To store the photo file, we need an object storage. One of the most famous object storage services is Amazon's Simple Service Storage, which is called S3 for short. Different cloud service providers generally offer the same user interface convenience as S3.

### Image Tagging Service
The task of this service is to create and return a number of labels for a photo, which represent the concepts inside the photo. There are different cloud services for this; There is no limit to choose the desired cloud service. After receiving the response, you check the received tags, which have two modes:
1. If there is no "vehicle" tag in the received tags, the ad will be rejected. (or the label "vehicle" was available, but its confidence percentage was less than 50)
2. If there was a "vehicle" tag in the received tags and the confidence percentage was greater than 50, the ad is approved and the tag with the highest confidence percentage is stored in the database as the category of the ad.

### Email Sending Service
After the photo processing phase is finished and the information is saved in the database, an email should be sent to the intended user to inform them of the status (approval/rejection) of the ad. For this, we want to use an email sending service. Different clouds are providing this service.

## Try For Yourself!
Before you can run this project you need to intall it's requirements as below: <br>
Install pika:

```
pip install pika
```

Install flask:

```
pip install flask
```

Install Pymongo:

```
pip install pymongo
```

Install boto3:

```
pip install boto3
```

Install requests:

```
pip install requests
```

After all the requirements are installed you have to set your own services, urls, secret codes, ... inside code. All services used in this project are free so don't worry about costs! All fields that you have to change are specified inside code<br>
After that run server.py and main.py seperatly. And done. Enjoy!

## Known Issues
There aren't currently any issues so far so if you find any please create an issue on this repository.
Any suggestions for implementation would also be greatly appreciated.
