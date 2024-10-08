# import sqlalchemy as sal
# from configuration.configuration import SQL_TABLE_NAME
# from configuration.configuration import CONNECTION_STRING
# from src import logger

# def load_data_to_sql(dataframe):
    
#     try:
#         engine = sal.create_engine(CONNECTION_STRING)

#         # Connect to the SQL Server
#         with engine.connect() as conn:
#             dataframe.to_sql(SQL_TABLE_NAME, con=conn, if_exists='append', index=False)
#             logger.info("Data loaded successfully into 'exchange_rates'")

#     except Exception as e:
#         logger.error(f"Error loading data to SQL: {e}")
#         raise
