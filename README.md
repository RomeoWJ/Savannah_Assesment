# Savannah Informatics - Data Engineering Pipeline

A comprehensive ETL pipeline that extracts, transforms, and loads e-commerce data from DummyJSON APIs into Google BigQuery for analysis.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Pipeline Structure](#pipeline-structure)
- [Usage](#usage)
- [Data Flow](#data-flow)
- [BigQuery Schema](#bigquery-schema)
- [Key Features](#key-features)
- [Assumptions & Trade-offs](#assumptions--trade-offs)
- [Future Enhancements](#future-enhancements)

## Overview

This project implements an automated ETL pipeline that:
- Extracts data from three public APIs (Users, Products, Carts)
- Cleans and normalizes the raw JSON data
- Loads transformed data into Google BigQuery
- Generates analytical insights through SQL transformations

**Tech Stack:**
- Python 3.x
- Google BigQuery
- DummyJSON API
- pandas, requests, google-cloud-bigquery

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Extract   │ ───> │  Transform   │ ───> │    Load     │
│  (APIs)     │      │  (Clean)     │      │  (BigQuery) │
└─────────────┘      └──────────────┘      └─────────────┘
      │                     │                      │
      v                     v                      v
  Raw JSON            CSV Files              BQ Tables
```

### Pipeline Flow:
1. **Extract** - Fetch data from DummyJSON APIs
2. **Transform** - Clean, normalize, and flatten data structures
3. **Load** - Upload to BigQuery tables
4. **Analyze** - Run SQL queries for insights

## Prerequisites

- Python 3.8+
- Google Cloud Account with BigQuery enabled
- Google Cloud credentials (service account JSON key)

## Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd savannah_data_pipeline
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up Google Cloud credentials:**
```bash
# Set environment variable to your service account key
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
```

## Pipeline Structure

```
savannah_data_pipeline/
│
├── main_pipeline.py         # Orchestrates the entire ETL workflow
├── extract_data.py          # Fetches data from APIs
├── clean_transform.py       # Data cleaning and transformation logic
├── load_bigquery.py         # Loads data into BigQuery
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
│
├── users.json              # Raw users data
├── products.json           # Raw products data
├── carts.json              # Raw carts data
│
├── clean_users.csv         # Cleaned users data
├── clean_products.csv      # Cleaned products data
└── clean_carts.csv         # Cleaned carts data
```

## Usage

### Run the Complete Pipeline:
```bash
python main_pipeline.py
```

This executes the entire ETL workflow in sequence.

### Run Individual Modules:

**Extract data:**
```bash
python extract_data.py
```

**Clean and transform:**
```bash
python clean_transform.py
```

**Load to BigQuery:**
```bash
python load_bigquery.py
```

## Data Flow

### 1. Extract (`extract_data.py`)
- Fetches data from three endpoints:
  - `https://dummyjson.com/users`
  - `https://dummyjson.com/products`
  - `https://dummyjson.com/carts`
- Saves raw JSON responses locally

### 2. Transform (`clean_transform.py`)

**Users Table:**
- Extracts: `user_id`, `first_name`, `last_name`, `gender`, `age`
- Flattens nested address fields: `street`, `city`, `postal_code`

**Products Table:**
- Extracts: `product_id`, `name`, `category`, `brand`, `price`
- Filters: Excludes products with price ≤ $50

**Carts Table:**
- Flattens products array into individual rows
- Calculates: `total_cart_value` per cart
- Fields: `cart_id`, `user_id`, `product_id`, `quantity`, `price`

### 3. Load (`load_bigquery.py`)
- Creates BigQuery dataset if not exists
- Uploads CSV files to three tables:
  - `users_table`
  - `products_table`
  - `carts_table`

## BigQuery Schema

### Users Table
```sql
user_id: INTEGER
first_name: STRING
last_name: STRING
gender: STRING
age: INTEGER
street: STRING
city: STRING
postal_code: STRING
```

### Products Table
```sql
product_id: INTEGER
name: STRING
category: STRING
brand: STRING
price: FLOAT
```

### Carts Table
```sql
cart_id: INTEGER
user_id: INTEGER
product_id: INTEGER
quantity: INTEGER
price: FLOAT
total_cart_value: FLOAT
```

## Key Features

### Error Handling
- API request retries with timeout handling
- Graceful handling of missing or malformed data
- Validation checks before BigQuery uploads

### Data Quality
- Removes null values in critical fields
- Validates data types before loading
- Ensures referential integrity across tables

### Modularity
- Separated concerns: extract, transform, load
- Reusable functions for common operations
- Easy to extend with new data sources

### Scalability
- Designed to handle larger datasets
- Batch processing capabilities
- Efficient pandas operations for transformations

## Analytical Queries

The pipeline enables the following analytical insights:

### User Summary
```sql
SELECT 
    u.user_id,
    u.first_name,
    u.age,
    u.city,
    SUM(c.total_cart_value) as total_spent,
    COUNT(DISTINCT c.cart_id) as total_purchases
FROM users_table u
LEFT JOIN carts_table c ON u.user_id = c.user_id
GROUP BY u.user_id, u.first_name, u.age, u.city
```

### Category Summary
```sql
SELECT 
    p.category,
    SUM(c.price * c.quantity) as total_sales,
    SUM(c.quantity) as total_items_sold
FROM products_table p
JOIN carts_table c ON p.product_id = c.product_id
GROUP BY p.category
ORDER BY total_sales DESC
```

## Assumptions & Trade-offs

### Assumptions:
1. **API Stability** - Assumes DummyJSON API structure remains consistent
2. **Data Volume** - Designed for the current dataset size (~100 users, ~200 products)
3. **Network Reliability** - Assumes stable internet connection for API calls
4. **Price Filter** - Products ≤ $50 are considered low-value and excluded

### Trade-offs:
1. **Local Storage** - Raw JSON and CSV files stored locally for debugging; could be optimized to stream directly to BigQuery
2. **Sequential Processing** - Pipeline runs tasks sequentially; could be parallelized for performance
3. **Schema Evolution** - Current schema is fixed; future versions could support dynamic schema detection
4. **No Incremental Loads** - Full refresh on each run; could implement incremental updates

## Future Enhancements

1. **Orchestration**
   - Implement Apache Airflow DAGs for scheduling
   - Add task dependencies and retry logic

2. **Data Quality**
   - Add Great Expectations for data validation
   - Implement data quality metrics and monitoring

3. **Performance**
   - Stream data directly to BigQuery (avoid CSV intermediates)
   - Implement parallel processing for API calls
   - Add partitioning and clustering to BigQuery tables

4. **Monitoring**
   - Add logging framework (e.g., Python logging)
   - Implement alerting for pipeline failures
   - Track pipeline execution metrics

5. **Testing**
   - Unit tests for transformation functions
   - Integration tests for end-to-end pipeline
   - Mock API responses for testing

## License

This project is created as part of the Savannah Informatics Data Engineering assessment.

## Contact

**Author:** WAIMIRI JOSEPH ROMEO 
**Email:** waimiri.romeo@gmail.com 

