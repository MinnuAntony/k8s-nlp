import logging

logging.basicConfig(
    filename="queries.log",
    format="%(asctime)s - %(message)s",
    level=logging.INFO
)

def log_query(user_query, result):
    logging.info(f"Query: {user_query} | Result: {result}")
