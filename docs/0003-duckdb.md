# 3. Duckdb

Date: 2025-09-27

## Status

influences [4. Fastapi](0004-fastapi.md)

## Context


Our application currently serves data by exposing CSV files directly to clients. This approach has several limitations:


- **Performance issues**: Large CSV files require complete downloads before processing, leading to slow response times and high bandwidth usage
- **Limited querying capabilities**: Clients cannot filter, aggregate, or perform complex queries on the data without downloading entire datasets
- **Scalability concerns**: As data volumes grow, CSV files become unwieldy and memory-intensive for both server and client
- **Data type handling**: CSV files lack proper data typing, leading to parsing issues and inconsistent data interpretation
- **Concurrent access**: Multiple clients accessing large CSV files simultaneously can overwhelm server resources
- **Analytics limitations**: Business users need to perform ad-hoc queries and analysis but cannot do so efficiently with raw CSV exports


We need a solution that provides better performance, query capabilities, and scalability while maintaining the simplicity of our current data serving approach.


## Decision


We will implement DuckDB as an embedded analytical database to replace direct CSV file serving. Specifically:


- **Embed DuckDB** in our Python application as the primary data serving layer
- **Expose SQL query endpoints** that allow clients to run analytical queries directly against the data


## Consequences


### What becomes easier:


- **Better performance**: DuckDB's columnar storage and vectorized execution will dramatically improve query performance
- **Reduced bandwidth potential**: Only query results are transmitted instead of entire datasets when we decide to limit the results returned in the database
- **Better data types**: Proper typing eliminates parsing errors and improves data consistency
- **Scalability**: DuckDB can handle much larger datasets efficiently in memory or with spillover to disk
- **Development productivity**: SQL queries are more maintainable and testable than CSV processing logic


### What becomes more difficult:


- **Increased complexity**: Adding a database layer introduces more components to manage and monitor
- **Learning curve**: Team members need to learn DuckDB-specific features and SQL optimization techniques
- **Debugging**: Query performance issues may be more complex to diagnose than simple file transfer problems
- **Dependency management**: Application now depends on DuckDB library and its compatibility requirements
