# Spotify Data Pipeline Project

## Project Overview

This project demonstrates a data pipeline built on AWS to automate the extraction, transformation, and loading (ETL) of data from the Spotify API. The pipeline is designed to run daily, extracting fresh data, processing it, and making it available for analysis and visualization.

### Key Features:

- **Data Extraction**: A Python-based AWS Lambda function extracts data from the Spotify API. This function is triggered daily by Amazon CloudWatch and stores the raw data in an Amazon S3 bucket (`to_processed/` folder).
- **Data Transformation**: A second Lambda function is automatically triggered whenever new raw data is added to the `to_processed/` folder in the S3 bucket. This function processes the data, transforming it into a more usable format and storing the results in a separate `transformed_data/` folder within the same S3 bucket.
- **Data Archival**: After the transformation, the original raw data is moved from the `to_processed/` folder to the `processed/` folder for archival purposes, ensuring that only unprocessed data is kept in the `to_processed/` folder.
- **Data Availability**: The transformed data is organized into subfolders for `artist_data`, `songs_data`, and `album_data`, and is made available for further analysis through Amazon Athena, with the schema being managed by AWS Glue.
- **Data Visualization**: The processed and transformed data is then downloaded from Athena and visualized in Tableau.

## Project Architecture

![Project Architecture Diagram](https://github.com/omotuno/Spotify-ETL-Data-Pipeline/blob/main/Spotify%20ETL%20Data%20Pipeline.drawio.svg)


The architecture diagram above represents the end-to-end data pipeline. Below is a step-by-step explanation of each component and how they integrate into the overall architecture:

### 1. Integrating with Spotify API and Extracting Data

- **Spotify API**: The project begins with integrating the Spotify API to extract data related to tracks, albums, and artists. This data is retrieved in JSON format using a Python script running on AWS Lambda.

### 2. Deploying Code on AWS Lambda for Data Extraction

- **AWS Lambda (Data Extraction)**: The code responsible for making API requests to Spotify and extracting data is deployed on AWS Lambda. This serverless function is highly scalable and allows you to execute code in response to events.

### 3. Adding a Trigger to Run the Extraction Automatically

- **Amazon CloudWatch (Daily Trigger)**: To automate the data extraction process, a CloudWatch Event Rule is configured to trigger the Lambda function daily. This ensures that the pipeline continuously ingests fresh data without manual intervention.

### 4. Writing the Transformation Function

- **AWS Lambda (Data Transformation)**: After extracting the data, it is crucial to process and clean it. A second Lambda function is created to transform the raw JSON data into a structured format that can be easily analyzed. This function is deployed on AWS Lambda and is triggered automatically whenever new data arrives in the S3 bucket.

### 5. Building an Automated Trigger on the Transformation Function

- **Automated Trigger**: An S3 event notification is configured to trigger the transformation Lambda function whenever new raw data is uploaded to the `to_processed/` folder in the S3 bucket. This event-driven approach ensures that data is transformed as soon as it is available.

### 6. Store Files on S3 Properly

- **Amazon S3 (Data Storage)**: S3 is used to store both raw and transformed data. The pipeline is designed with the following structure:
  - **Raw Data Storage**:
    - `raw_data/to_processed/`: Stores the raw data extracted from the Spotify API awaiting processing.
    - `raw_data/processed/`: After processing, raw data files are moved to this folder for archival.
  - **Transformed Data Storage**:
    - `transformed_data/artist_data/`: Stores transformed data related to artists.
    - `transformed_data/songs_data/`: Stores transformed data related to songs.
    - `transformed_data/album_data/`: Stores transformed data related to albums.
  - The structured storage of both raw and transformed data helps maintain organization and ensures that data is easily accessible for analysis.

### 7. Building Analytics Tables on Data Files Using Glue and Athena

- **AWS Glue Crawler & Data Catalog**: AWS Glue is used to automatically infer the schema of the transformed data stored in S3. The Glue Crawler scans the S3 bucket and updates the Glue Data Catalog with the schema details. This step is crucial for making the data queryable by Amazon Athena.
- **Amazon Athena (Querying & Analytics)**: Amazon Athena is a serverless query service that allows you to analyze the transformed data stored in S3 using standard SQL. By querying the data through Athena, you can derive insights, generate reports, and export results for further analysis in tools like Tableau.

### Data Visualization in Tableau



1. **Export Data from Athena**:

   - Use Amazon Athena to run SQL queries on the data stored in S3.
   - Export the query results in a format compatible with Tableau (e.g., CSV).
2. **Import Data into Tableau**:

   - Open Tableau and connect to the exported CSV files or connect directly to the Athena service using the Tableau connector for AWS.
   - Build visualizations and dashboards based on the Spotify data.
3. **Analyze and Share**:

   - Use Tableau to analyze the data and share the insights.
   - The link to the dashboard is https://public.tableau.com/app/profile/olusegun.omotunde/viz/SpotifyTop100SongsinNigeria/Dashboard1

## Getting Started

### Prerequisites

- **Spotify Developer Account**: You will need a Spotify Developer account to access the Spotify API. After registering, you will get a `client_id` and `client_secret` which are required to authenticate your requests.

  - Save these credentials as environment variables in your AWS Lambda functions:
    - `SPOTIFY_CLIENT_ID`
    - `SPOTIFY_CLIENT_SECRET`
  - This can be done in the AWS Lambda console under the "Configuration" tab, in the "Environment variables" section.
- **AWS Account**: You need an AWS account with access to services such as Lambda, S3, Glue, and Athena.
- **IAM Roles**: Ensure that the IAM roles associated with your Lambda functions have the necessary permissions to access S3, Glue, and Athena.
- **Python 3.12**: Installed locally for developing and testing the Lambda functions.
- **Boto3 Library**: Install the Boto3 library (AWS SDK for Python) using pip:

  ```bash
  pip install boto3
  ```


## Project Structure

- **`spotify_api_extract_lambda_function.py`**: The Lambda function code for extracting data from Spotify API.
- **`spotify_transformation_load_lambda_function.py`**: The Lambda function code for transforming and loading data into S3.
- **`README.md`**: Documentation of the project.

## Deployment

1. **Create S3 Buckets**:

   - Create an S3 bucket for storing raw data (`spotify-raw-data`) with two subfolders: `to_processed/` and `processed/`.
   - Create an S3 bucket for storing transformed data (`spotify-transformed-data`) with three subfolders: `artist_data/`, `songs_data/`, and `album_data/`.
2. **Deploy Lambda Functions**:

   - Deploy the `spotify_api_extract_lambda_function.py` to AWS Lambda.
   - Deploy the `spotify_transformation_load_lambda_function.py` to AWS Lambda.
   - Set up appropriate IAM roles and policies for these Lambda functions.
3. **Set Up CloudWatch Trigger**:

   - Create a CloudWatch Event Rule to trigger the data extraction Lambda function daily.
4. **Set Up S3 Event Trigger**:

   - Configure S3 event notifications to trigger the data transformation Lambda function whenever new data is added to the `to_processed/` folder.
5. **Set Up Glue Crawler**:

   - Create a Glue Crawler to scan the transformed data in the S3 bucket and update the Glue Data Catalog.
6. **Set Up Athena**:

   - Use Athena to query the data stored in S3 using the schema information from the Glue Data Catalog.

## Data Visualization in Tableau

1. **Export Data from Athena**:

   - Use Amazon Athena to run SQL queries on the data stored in S3.
   - Export the query results in a format compatible with Tableau (e.g., CSV).
2. **Import Data into Tableau**:

   - Open Tableau and connect to the exported CSV files or connect directly to the Athena service using the Tableau connector for AWS.
   - Build visualizations and dashboards based on the Spotify data.
3. **Analyze and Share**:

   - Use Tableau to analyze the data and share the insights with stakeholders.

## Contributing

Feel free to fork this repository and submit pull requests. Please ensure any new code is well-documented and follows the existing coding style.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/omotuno/Spotify-ETL-Data-Pipeline/blob/main/LICENSE) file for details.

## Acknowledgments

- Special thanks to Spotify for providing the API used in this project.
- Thanks to AWS for providing the infrastructure that supports this data pipeline.
