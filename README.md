# Customer Data Insights

An analysis of customer shopping behaviour using Python, MySQL 8 and Power BI. The project cleans the data, loads it into MySQL and answers ten business questions about spending, discounts, subscriptions and customer segments.

## Results

The dataset contains **3,900 customers** and **$233,081** in purchases, with an average purchase of **$59.76**. Cleaning fills 37 missing review ratings using the median for each product category. Age groups use dataset quartiles, rather than fixed age bands.

## Run locally

You need Windows, Python 3.12 and a running MySQL 8 server.

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

1. Double-click `CONNECT_MYSQL.cmd`. Enter the MySQL host, port, username and password, then click **Connect and load project**. The account needs permission to create the `customer_behavior` database and its `customer` table on the first run.
2. Open `OPEN_NOTEBOOK.cmd` to work through the notebook.
3. Use `RUN_ANALYSIS.cmd` to rerun the import and SQL analysis. The cleaned data, ten query results and verification summary are written to `results/`.

The Windows setup encrypts the password for the current user and stores it outside the repository, under `%LOCALAPPDATA%\CustomerSalesInsights`. Host and port are saved locally in `mysql_config.json`. Neither file belongs in GitHub.

Existing customer tables are preserved. The importer reuses a matching table and stops if its contents differ from the source dataset.

## SQL analysis

Open `customer_behavior_sql_queries.sql` in MySQL Workbench after loading the data. It covers revenue by gender and age group, discounted purchases, product ratings, shipping, subscriptions, customer loyalty and popular products in each category.

## Power BI

`customer_behavior_dashboard.pbix` is the original reference dashboard. Its imported model is included, but its source has not been migrated or refresh-tested against this MySQL setup.

To connect it locally, open **Transform data**, select the existing customer query and replace its source in **Advanced Editor** with `powerbi_mysql_source.m`. Keep the existing query name so the visuals retain their bindings. Adjust the host and port if needed, authenticate locally, then **Close & Apply** and refresh. Power BI may require its supported MySQL Connector/NET provider.

## Files

- `Customer_Shopping_Behavior_Analysis.ipynb`: data exploration and cleaning
- `pipeline.py`: cleaning, MySQL import and analysis export
- `setup_gui.py`: local connection setup
- `customer_shopping_behavior.csv`: source dataset
- `customer_behavior_sql_queries.sql`: ten MySQL analysis queries
- `customer_behavior_dashboard.pbix`: reference Power BI report

## Validation

On Windows with Python 3.12 and MySQL 8, all 3,900 imported records matched the cleaned CSV and all ten SQL queries executed successfully. The notebook ran without error. The Power BI refresh remains unverified.

## Attribution

Adapted from [Amlan Mohanty's customer behaviour analysis](https://github.com/amlanmohanty1/customer-trends-data-analysis-SQL-Python-PowerBI). The dataset, notebook workflow and reference dashboard come from that project. This version adds a Windows setup and MySQL-specific workflow. The original MIT license is retained in `LICENSE`.
