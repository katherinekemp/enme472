import sqldb

data_folder = "data"
sqldb.create_db(f"{data_folder}/water_usage.db")
sqldb.create_db(f"{data_folder}/nutrient_usage.db")