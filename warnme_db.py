# warnme_db.py

import snowflake.connector
import pandas as pd
import logging

class SnowflakeConnector:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('WarnMeLogger')

    def Connect(self):
        try:
            conn = snowflake.connector.connect(
                user=self.config["WARNME_DB_USER"],
                password=self.config["WARNME_DB_PASSWORD"],
                account=self.config["WARNME_DB_ACCOUNT"],
                database=self.config["WARNME_DB_DATABASE"],
                schema=self.config["WARNME_DB_SCHEMA"],
                role=self.config["WARNME_DB_ROLENAME"]
            )
            self.logger.info("Connection to Snowflake established.")
            return conn
        except Exception as e:
            self.logger.error(f"Error connecting to Snowflake: {e}")
            return None

    def SetWarehouse(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute(f"USE WAREHOUSE {self.config['WARNME_DB_WAREHOUSE']}")
            cursor.close()
            self.logger.info("Warehouse selected.")
        except Exception as e:
            self.logger.error(f"Error setting warehouse: {e}")

    def Query(self, sqlQuery):
        conn = self.Connect()
        if conn is None:
            return None
        self.SetWarehouse(conn)
        try:
            df = pd.read_sql(sqlQuery, conn)
            conn.close()
            self.logger.info("Query executed successfully.")
            return df
        except Exception as e:
            self.logger.error(f"Error executing query: {e}")
            return None
