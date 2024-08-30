# Detik.com News Scraping 
<br>
<b>Requirement:</b><br>
- python 3.10.14<br>
- installed packages (use requirements.txt)
<br><br>
<b>Scope:</b><br>
- Currently, this engine is only build for detik.com web
<br><br>
<b>Feature:</b><br>
- News scraping with input is date range and keywords search
- Optimized with asynchronous flow
<br><br>
<b>Usage:</b><br>
- News dataset collection (including news metadata like title, published date, news keywords, authors)
<br><br>
<b>How to use:</b><br>
- prepare your environment by installing the requirements <br>
- run this command on your env terminal <br>
    > command: `python run_scraping.py <from_date> <to_date> <keyword[s]>` <br>
    > example: `python run_scraping.py 10/02/2024 30/08/2024 pangan` <br>
    > example: `python run_scraping.py 10/02/2024 30/08/2024 "pangan, BBM, pasar  induk"` <br>
- the output will be exported into parquet file <br>