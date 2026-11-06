# Customer Data Insights

A customer shopping analysis project using Python, MySQL and Power BI. I used Python to clean the data, SQL to explore shopping patterns, and Power BI to view the results.

## Dataset

The dataset has 3,900 customer records, including age, gender, products purchased, purchase amounts, ratings, discounts and subscription status.

## Data cleaning

- Filled 37 missing review ratings using the median rating for each category.
- Renamed columns for use in SQL.
- Grouped customers by age and added purchase frequency in days.
- Removed the promo code column because it matched the discount column.

## Analysis

The SQL queries explore spending by gender and age group, popular products, discounts, shipping preferences and subscriptions.

Total purchases in the dataset add up to **$233,081**, with an average purchase of **$59.76**.

## Run the project

Requirements: Python 3.12, MySQL 8 and Power BI Desktop.

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

1. Run `CONNECT_MYSQL.cmd` and enter your local MySQL details.
2. Run `OPEN_NOTEBOOK.cmd` to open the notebook.
3. Open `customer_behavior_sql_queries.sql` in MySQL Workbench to explore the data. `RUN_ANALYSIS.cmd` also saves the query results in the `results` folder.
4. Open `customer_behavior_dashboard.pbix` in Power BI Desktop. To use your local database, update the existing customer query using `powerbi_mysql_source.m` and enter your MySQL login. The included dashboard still uses its original imported data until you update the connection.

## Reference

Based on [Amlan Mohanty's customer shopping analysis](https://github.com/amlanmohanty1/customer-trends-data-analysis-SQL-Python-PowerBI), adapted to run with MySQL on my PC.
