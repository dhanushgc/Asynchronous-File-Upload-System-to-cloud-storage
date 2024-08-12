# Asynchronous File Upload System to Cloud Storage

This project is an Asynchronous File Upload System designed to efficiently handle file uploads to cloud storage (Azure Blob Storage). The system is built using Django for the backend, Celery for asynchronous task processing, and RabbitMQ as the message broker. The system is capable of handling large files by uploading them in chunks, ensuring robust and scalable performance.

## Features

- **Asynchronous Processing**: File uploads are processed asynchronously using Celery, ensuring that the web application remains responsive even when handling large files.
- **Chunked File Uploads**: Large files are uploaded in chunks, allowing for efficient handling of files that exceed typical upload size limits.
- **Temporary Storage**: Files are temporarily stored on the server during processing and are automatically deleted after successful upload to Azure Blob Storage.
- **Azure Blob Storage Integration**: The system integrates with Azure Blob Storage, allowing files to be stored securely in the cloud.
- **Scalable Architecture**: By leveraging Celery and RabbitMQ, the system is designed to scale easily, handling multiple file uploads concurrently.

## Technology Stack

- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Celery**: An asynchronous task queue/job queue based on distributed message passing. Celery is focused on real-time operation, but also supports task scheduling.
- **RabbitMQ**: A message broker that allows asynchronous communication between the Django application and Celery workers.
- **Azure Blob Storage**: A scalable, secure, and highly available cloud storage service by Microsoft Azure, used for storing files in this project.
