# Detik.com News Scraping

## Requirement:
- Python 3.10.14
- Installed packages (use `requirements.txt`)

## Scope:
- Currently, this engine is only built for the detik.com website

## Features:
- News scraping with input as date range and keywords search
- Optimized with asynchronous flow

## Usage:
- News dataset collection (including news metadata like title, published date, news keywords, authors)

## How to Use:
1. Prepare your environment by installing the requirements.
2. Run this command on your environment terminal:
   - **Command:** `python run_scraping.py`
   - **Example:** 
     - `python run_scraping.py 10/02/2024 30/08/2024 pangan`
     - `python run_scraping.py 10/02/2024 30/08/2024 "pangan, BBM, pasar induk"`
3. The output will be exported into a Parquet file.
