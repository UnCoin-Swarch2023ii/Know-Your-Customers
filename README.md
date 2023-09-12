# Know Your Customer MS for UnCoin

## Description

This is a microservice for UnCoin. It is responsible for validating the user identities. The validation is done by comparing the users photo and the picture that appears in the user's CC (cedula de ciudadanía).


The microservice uses the followin technologies:

- Python.
- Face Comparison.
- Flask.
- Docker.
- AWS S3 storage.

## Project Structure

```bash
.
├── .env
├── .env.example
├── app.py
├── Dokerfile
├── requirements
└── helpers
    └── s3Aws.ts
```

## How to run

1. Clone the repository
2. Create a `.env` file based on `.env.example`
3. Run `docker compose up`. This may take a while because of the  face-comparison models loading.
4. The server will be running on port specified by environment variable `PORT` or 5000 by default
5. That's it!

### Environment variables

The enviroment variables are related to your AWS S3 IAM credentials. In order to create your own AWS S3 Bucket you should follow this link https://aws.amazon.com/es/s3/. Then you should create an acces to the bucket in the IAM panel, and then give the permisions to CRUD operations to the new user. 

**aws_access_key_id** : Aws acces key ID from your s3 bucket.
**aws_secret_access_key**: Aws acces key ID from your s3 bucket.
**region_name**: The region where your bucket is placed.
**bucketName** = The name of your bucket.


## Endpoints

### `/delete-image` - Delete the image from the bucket that mathces the recieved name.

### `/get-image` - Download the image from the bucket that mathces the recieved name.

### `/upload_image1` - Upload the image that is required to be checked. The image 1 refers to the user CC pic. Retrieves wether or not the face-comparison detects a human face.

### `/upload_image2` - Upload the image that is required to be checked. The image 2 refers to the user CC pic. Retrieves wether or not the face-comparison detects a human face.

### `/compare_images` - Upload two images that are required to be compared.  Retrieves wether or not the images compared belong to the same person.

