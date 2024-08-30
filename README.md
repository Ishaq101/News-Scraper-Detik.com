# [Detik.com](https://www.detik.com/) News Scraping


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
1. Clone repository
   - `git clone <repository-url>`
   - `cd <repository-directory>`
2. Create env
   - `conda create -n venvname python==3.10`
   - `conda activate venvname`
3. Prepare your environment by installing the requirements.
   - `pip install -r requirements.txt`
4. Run this command on your environment terminal:
   - **Command:** `python run_scraping.py`
   - **Example:** 
     - `python run_scraping.py --from_date="29/08/2024" --to_date="30/08/2024" --keyword=[pangan]`
     - `python run_scraping.py --from_date="29/08/2024" --to_date="30/08/2024" --keyword=[pangan, BBM, pasar induk]`
5. The output will be exported into a Parquet file.
