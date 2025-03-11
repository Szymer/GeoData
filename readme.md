Summary
The aim of this task is to build a simple API (backed by any kind of database). The application should be able to store geolocation data in the database, based on IP address or URL - you can use https://ipstack.com/ to get geolocation data. The API should be able to add, delete or provide geolocation data on the base of ip address or URL. 

Application specification
It should be a RESTful API
You can use https://ipstack.com/ for the geolocation of IP addresses and URLs
The application can be built in any framework of your choice
It is preferable that the API operates using JSON (for both input and output)
The solution should also include base specs/tests coverage

How to submit
Create a public Git repository and share the link with us

Notes:
We will run the application on our local machines for testing purposes. This implies that the solution should provide a quick and easy way to get the system up and running, including test data (hint: you can add Docker support so we can run it easily)
We will test the behavior of the system under various "unfortunate" conditions (hint: How will the app behave when we take down the DB? How about the IPStack API?)
After we finish reviewing the solution, we'll invite you to Sofomo's office (or to a Zoom call) for a short discussion about the provided solution. We may also use that as an opportunity to ask questions and drill into the details of your implementation.



Project Description
The application allows the user to input an IP address or URL, which is then processed by the system. To ensure efficiency and scalability, operations related to adding and modifying records in the database are queued using Celery, with Redis acting as the message broker. This approach enables the application to handle multiple requests simultaneously, preventing the main application thread from being blocked.

Additionally, Pydantic is used for input data validation and modeling, ensuring strict data validation and automatic type conversion. This improves the application's reliability and maintainability.

The application can be utilized in various scenarios, such as monitoring server availability, storing and updating DNS records, or analyzing network connections. The architecture based on Celery and Redis allows for easy scaling and future feature expansions.


