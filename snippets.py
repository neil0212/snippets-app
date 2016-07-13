import logging
import argparse
import psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established.")

def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    with connection, connection.cursor() as cursor:
        try:
            command = "insert into snippets values (%s, %s)"
            cursor.execute(command, (name, snippet))
        except psycopg2.IntegrityError as e:
            connection.rollback()
            command = "update snippets set message=%s where keyword=%s"
            cursor.execute(command, (snippet, name))
    logging.debug("Snippet stored successfully.")
    return name, snippet
    
def get(name):
    """Get a snippet with keyword."""
    logging.info("Get snippet from keyword{!r}".format(name))
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        row = cursor.fetchone()
    logging.debug("Snippet get successfully.")
    if not row:
        # No snippet was found with that name.
        return "404: Snippet Not Found"
    return row[0]

def catalog():
    """List all the keywords"""
    logging.info("List all the keywords")
    with connection, connection.cursor() as cursor:
        cursor.execute("select keyword from snippets order by keyword ASC")
        list=cursor.fetchall()
        for row in list:
            print(row)
        logging.debug("catalog")
    
def search(word):
    """Search for keyword"""
    logging.info("Search for keyword")
    with connection, connection.cursor() as cursor:
        cursor.execute("select * from snippets where message like %s",(word,))
        list=cursor.fetchall()
        for row in list:
            print(row)
        logging.debug("search")   
    





    
def main():
    

    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="Name of the snippet")
    put_parser.add_argument("snippet", help="Snippet text")
    
    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Get a snippet")
    get_parser.add_argument("name", help="Name of the snippet")
    
    #subparser for catalog command
    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Get keyword list")
    
    #subparser for search command
    logging.debug("Constructing search subparser")
    search_parser = subparsers.add_parser("search", help="search keyword")
    get_parser.add_argument("word", help="Search keyword")
    
    
    arguments = parser.parse_args()
    
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command == "catalog":
        catalog()
        print("Keywords")
    elif command == "search":
        snippet = search(**arguments)
        print("Search snippet: {!r}".format(snippet))

if __name__ == "__main__":
    
    main()