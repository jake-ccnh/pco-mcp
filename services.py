from fastmcp import FastMCP
from pypco import PCO  # Import the PCO client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

mcp = FastMCP("PCO Services MCP Server")

# Initialize the PCO client with credentials from environment variables
pco = PCO(
    application_id=os.getenv("PCO_APPLICATION_ID"),
    secret=os.getenv("PCO_SECRET_KEY")
)

@mcp.tool()
def get_service_types() -> list:
    """
    Fetch a list of service types from the Planning Center Online API.
    """
    # Using the direct get method as shown in the documentation
    response = pco.get('/services/v2/service_types')
    # return [service_type['attributes'] for service_type in response['data']]
    return response['data']

@mcp.tool()
def get_plans(service_type_id: str) -> list:
    """
    Fetch a list of plans for a specific service type.
    
    Args:
        service_type_id (str): The ID of the service type.
    """
    # Using the direct get method as shown in the documentation
    response = pco.get(f'/services/v2/service_types/{service_type_id}/plans?order=-updated_at')
    return response['data']

@mcp.tool()
def get_plan_items(plan_id: str) -> list:
    """
    Fetch a list of items for a specific plan.
    
    Args:
        plan_id (str): The ID of the plan.
    """
    # Using the direct get method as shown in the documentation
    response = pco.get(f'/services/v2/plans/{plan_id}/items')
    return response['data']

@mcp.tool()
def get_plan_team_members(plan_id: str) -> list:
    """
    Fetch a list of team members for a specific plan.
    
    Args:
        plan_id (str): The ID of the plan.
    """
    # Using the direct get method as shown in the documentation
    response = pco.get(f'/services/v2/plans/{plan_id}/team_members')
    return response['data']

@mcp.tool()
def schedule_team_member(service_type_id: str, plan_id: str, team_id: int, team_position_name: str, person_id: str) -> list:
    """
    Schedule a team member for a specific plan under a service type.
    
    Args:
        service_type_id (str): The ID of the service type.
        plan_id (str): The ID of the plan.
        team_id (int): The ID of the team.
        team_position_name (str): The role or position name within the team.
        person_id (str): The ID of the person to schedule.
    
    """
    endpoint = f'/services/v2/service_types/{service_type_id}/plans/{plan_id}/schedule_team_members'

    payload = {
        "data": {
            "attributes": {
                "team_id": team_id,
                "team_position_name": team_position_name,
                "people_ids": [person_id]
            }
        }
    }

    response = pco.post(endpoint, payload)
    return response

@mcp.tool()
def get_teams() -> list:
    """
    Fetch a list of teams from the Planning Center Online API.
    
    This function retrieves all teams, including extended teams, from the Planning Center Online API.
    It uses the endpoint for extended teams to ensure all teams are included.
    """
    response = pco.get('/services/v2/extended_teams?order=name&offset=0&per_page=100')
    return response['data']

@mcp.tool()
def get_team_people(team_id: str) -> list:
    """
    Fetch a list of people associated with a specific team.
    """
    response = pco.get(f'/services/v2/service_types/{service_type_id}/not_deleted_teams/{team_id}/team_people?offset=0&order=first_name&per_page=100')
    return response['data']

@mcp.tool()
def get_songs() -> list:
    """
    Fetch a list of songs from the Planning Center Online API.
    """
    # Using the direct get method as shown in the documentation
    response = pco.get('/services/v2/songs?per_page=200&where[hidden]=false')
    return response['data']

@mcp.tool()
def get_song(song_id: str) -> dict:
    """
    Fetch details for a specific song.
    
    Args:
        song_id (str): The ID of the song.
    """
    # Using the direct get method as shown in the documentation
    response = pco.get(f'/services/v2/songs/{song_id}')
    return response['data']



if __name__ == "__main__":
    # Example usage of the tools
    print("PCO Services MCP Server - CLI Test Mode")
    
    # Test getting service types
    print("\nFetching service types...")
    service_types = get_service_types()
    print(f"Found {len(service_types)} service types")
    print(service_types)
    
    if service_types:
        # Test getting plans for the first service type
        service_type_id = service_types[0].get('id')
        print(f"\nFetching plans for service type ID: {service_type_id}")
        plans = get_plans(service_type_id)
        print(f"Found {len(plans)} plans")
        
        if plans:
            # Test getting plan items for the first plan
            plan_id = plans[0].get('id')
            print(f"\nFetching items for plan ID: {plan_id}")
            items = get_plan_items(plan_id)
            print(f"Found {len(items)} items")
            
            # Test getting team members for the first plan
            print(f"\nFetching team members for plan ID: {plan_id}")
            team_members = get_plan_team_members(plan_id)
            print(f"Found {len(team_members)} team members")
            
            if team_members:
                # Test getting assignments for the first team member
                team_member_id = team_members[0].get('id')
                print(f"\nFetching assignments for team member ID: {team_member_id}")
                # assignments = get_plan_team_member_assignments(plan_id, team_member_id)
                # print(f"Found {len(assignments)} assignments")
    
    # Test getting songs
    print("\nFetching songs...")
    songs = get_songs()
    print(f"Found {len(songs)} songs")
    
    if songs:
        # Test getting details for the first song
        song_id = songs[0].get('id')
        print(f"\nFetching details for song ID: {song_id}")
        song_details = get_song(song_id)
        print(f"Song details: {song_details.get('title')} by {song_details.get('author')}")
    
    # # Test iterating through plans
    # if service_types:
    #     service_type_id = service_types[0].get('id')
    #     print(f"\nIterating through plans for service type ID: {service_type_id}")
    #     plans = iterate_through_plans(service_type_id)
    #     print(f"Found {len(plans)} plans through iteration")
    
    print("\nCLI test completed.")
