from fastmcp import FastMCP
from pypco import PCO  # Import the PCO client
from pypco.exceptions import PCORequestException
import os
from dotenv import load_dotenv
import sys
import time

try:
    # Load environment variables from .env file
    load_dotenv()

    mcp = FastMCP("PCO People MCP Server")

    # Initialize the PCO client with credentials from environment variables
    pco = PCO(
        application_id=os.getenv("PCO_APPLICATION_ID"),
        secret=os.getenv("PCO_SECRET_KEY")
    )
    
    response = pco.get('/people/v2?offset=1')
except PCORequestException as pcoe:
    print("There was an error with the PCO request:", pcoe)
    sys.exit(1)

@mcp.tool()
def get_people_lastname(lastname) -> list:
    """
    Fetch a list of people from the People module in Planning Center Online API.
    """
    # Using the direct get method as shown in the documentation
    response = pco.get('/people/v2/people?where[last_name]='+str(lastname)+'&per_page=100')
    return response['data']

@mcp.tool()
def get_people_firstname(firstname) -> list:
    """
    Fetch a list of people from the People module in Planning Center Online API.
    """
    # Using the direct get method as shown in the documentation
    response = pco.get('/people/v2/people?where[first_name]='+str(firstname)+'&per_page=100')
    return response['data']

@mcp.tool()
def get_people_first_and_lastname(firstname, lastname) -> list:
    """
    Fetch a list of people from the People module in Planning Center Online API.
    """
    # Using the direct get method as shown in the documentation
    response = pco.get(f'/people/v2/people?per_page=100&where[first_name]={firstname}&where[last_name]={lastname}')
    return response['data']

@mcp.tool()
def get_person_activity(person_id) -> list:
    """
    Fetch a list of people from the People module in Planning Center Online API.
    """
    # Using the direct get method as shown in the documentation
    today = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    real_today = "2025-07-20T11%3A50%3A36-06%3A00"
    year_from_today = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 365 * 24 * 60 * 60))
    print(today,)
    response = pco.get(f'/people/v2/people/{person_id}/activities?before={today}&after={year_from_today}&per_page=100')
    return response['data']


if __name__ == "__main__":
    # Example usage of the tools
    print("PCO Services MCP Server - CLI Test Mode")
    print("Checking Permissions...")
    print("Fetching People...")

    # Test get_people_lastname
    people = get_people_lastname("smith")
    print(f"Fetched {len(people)} people with last name 'smith'.")
    for person in people:
        print(f"Person ID: {person['id']}, Name: {person['attributes']['name']}")

    # Test get_people_firstname
    people = get_people_firstname("john")
    print(f"\nFetched {len(people)} people with first name 'john'.")
    for person in people:
        print(f"Person ID: {person['id']}, Name: {person['attributes']['name']}")

    # Test get_people_first_and_lastname
    people = get_people_first_and_lastname("john", "smith")
    print(f"\nFetched {len(people)} people with first name 'john' and last name 'smith'.")
    for person in people:
        print(f"Person ID: {person['id']}, Name: {person['attributes']['name']}")
    # Test get_person_activity
    if people:
        person_id = people[0]['id']
        activities = get_person_activity(person_id)
        print(f"\nFetched {len(activities)} activities for person ID {person_id}.")
        for activity in activities:
            print(f"Activity ID: {activity['id']}, Type: {activity['type']}")
    print("\nCLI test completed.")