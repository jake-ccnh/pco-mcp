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

# @mcp.tool()
# def get_plan_team_member_assignments(plan_id: str, team_member_id: str) -> list:
#     """
#     Fetch a list of assignments for a specific team member in a plan.
    
#     Args:
#         plan_id (str): The ID of the plan.
#         team_member_id (str): The ID of the team member.
#     """
#     # Using the direct get method as shown in the documentation
#     response = pco.get(f'/services/v2/plans/{plan_id}/team_members/{team_member_id}/assignments')
#     return response['data']

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
