# Stock Market Data Processing

* Setting up Database
    * Created a database named altys_db and created a schema named stock_data
    * Created a table named ohlc_data with the below DDL
    
    CREATE TABLE IF NOT EXISTS stock_data.ohlc_data ( \
        date DATE, \
        company VARCHAR(50), \
        open FLOAT, \
        close FLOAT, \
        high FLOAT, \
        low FLOAT, \
        volume BIGINT, \
	UNIQUE(date, company) \
    ); \

    * I have added unique columns so that if in any case the script fails in between, we can run it again without worrying about data duplications

* Backfilling historical data (historical_dump.py)
    * I have created a script named historical_dump.py for migrating data to postgres db on localhost
    * After getting the API key, I have written a function (get_data) to get data from API and another function (clean_data) to get the required fields, converted the json to dataframe and filtered data from Jan 2020- May 2024
    * After getting all the data I have pushed it to postgres database

* Script for Daily Dump (D-1) (incremental.py)
    * Created the same script as historical the only change is in the date filter inside the clean_data function and added a variable to store the yesterday's date to compare
    * Stock Market is closed on Saturday and Sunday, so the resulting dataframe will be null for that day and no data will be inserted

* Indexing database of query performance
    * Created a single column index on company (idx_company)
    * Created a single column index on date (idx_date)
    * Created a composite index with columns company and date so that whenever both the fields are used in a query it will use this index (idx_company_date)


    1. Company Wise Daily Variation of Prices
        For Daily variation of price we might use high-low or close-open for getting the price changes, in this case if we add a where clause for company name the idx_company index will be used and for date idx_date will be used for getting faster results

    2. Company Wise Daily Volume Change
        For Volume change we can compare today's volume changes with yesterday's to get if it has been increase or decrease, in this query we will use window function lag to get the data for previuous day. In window function we have to sort by date and partition by company for which we already have composite index in our database.

    3. Median Daily Variation
        For Median daily variation, I have used (high-low) as variation and sort the data by variation in ascending order, partition by company and gave a row number to it and calculated the median from it.

    All 3 Queries uses composite index since we have used partition by company and sorted by date\
    All the queries are available in database.txt