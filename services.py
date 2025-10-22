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
def get_all_arrangements_for_song(song_id: str) -> list:
    """
    Get a list of all the arrangements for a particular song from the Planning Center Online API.

    Args: 
        song_id (str): The ID for the song. 
    """
    response = pco.get(f'/services/v2/songs/{song_id}/arrangements')
    return response['data']

@mcp.tool()
def get_arrangement_for_song(song_id: str, arrangement_id: str) -> list:
    """
    Get information for a particular song from the Planning Center Online API.

    Args: 
        song_id (str): The ID for the song. 
        arrangement_id (str): The ID for the arrangement within a song. 
    """
    response = pco.get(f'/services/v2/songs/{song_id}/arrangements/{arrangement_id}')
    return response['data']

@mcp.tool()
def get_keys(song_id: str, arrangement_id: str) -> list:
    """
    Get a list of keys available for a particular song ID and arrangement ID from the Planning Center Online API. 

    Args: 
        song_id (str): The ID for the song. 
        arrangement_id (str): The ID for the arrangement within a song. 
    """
    response = pco.get(f'/services/v2/songs/{song_id}/arrangements{arrangement_id}/keys')
    return response['data']

@mcp.tool()
def create_song(title: str, ccli: str = None) -> dict:
    """
    Create a new song in Planning Center Online.

    Args:
        title (str): The title of the song.
        ccli (str, optional): The CCLI number for the song.

    Returns:
        dict: The created song data.
    """
    attributes = {"title": title}
    if ccli:
        attributes["ccli_number"] = ccli

    body = pco.template('Song', attributes)
    response = pco.post('/services/v2/songs', body)
    return response['data']

@mcp.tool()
def find_song_by_title(title: str) -> list:
    """
    Find songs by title.

    Args:
        title (str): The title of the song to search for.

    Returns:
        list: List of songs matching the title.
    """
    response = pco.get(f'/services/v2/songs?where[title]={title}&where[hidden]=false')
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

@mcp.tool()
def assign_tags_to_song(song_id: str, tag_names: list[str]) -> dict:
    """
    Assign tags to a specific song.

    Args:
        song_id (str): The ID of the song.
        tag_names (list[str]): List of tag names to assign to the song.

    Returns:
        dict: Success status and message.
    """
    # Get all tag groups with their tags included
    tag_groups_response = pco.get('/services/v2/tag_groups?include=tags&filter=song')

    # Extract tags from the included section
    included_tags = tag_groups_response.get('included', [])

    # Find the tag IDs for the requested tag names
    tag_data = []
    for tag_name in tag_names:
        for tag in included_tags:
            if tag['type'] == 'Tag' and tag['attributes']['name'].lower() == tag_name.lower():
                tag_data.append({
                    "type": "Tag",
                    "id": tag['id']
                })
                break

    if not tag_data:
        return {"success": False, "message": "No matching tags found"}

    # Build the request body
    body = {
        "data": {
            "type": "TagAssignment",
            "attributes": {},
            "relationships": {
                "tags": {
                    "data": tag_data
                }
            }
        }
    }

    # Make the POST request
    response = pco.post(f'/services/v2/songs/{song_id}/assign_tags', body)

    # A 204 status means success with no content
    return {"success": True, "message": f"Successfully assigned {len(tag_data)} tag(s) to song {song_id}"}

@mcp.tool()
def find_songs_by_tags(tag_names: list[str]) -> list:
    """
    Find songs that have all of the specified tags.

    Args:
        tag_names (list[str]): List of tag names to filter songs by. Songs must have all specified tags.
    """
    # Get all tag groups with their tags included
    tag_groups_response = pco.get('/services/v2/tag_groups?include=tags&filter=song')

    # Extract tags from the included section
    included_tags = tag_groups_response.get('included', [])

    # Find the tag IDs for the requested tag names
    tag_ids = []
    for tag_name in tag_names:
        for tag in included_tags:
            if tag['type'] == 'Tag' and tag['attributes']['name'].lower() == tag_name.lower():
                tag_ids.append(tag['id'])
                break

    if not tag_ids:
        return []

    # Build the query string with tag filters
    # Multiple tag filters create an AND condition
    tag_filters = '&'.join([f'where[song_tag_ids]={tag_id}' for tag_id in tag_ids])
    query = f'/services/v2/songs?per_page=200&where[hidden]=false&{tag_filters}'

    response = pco.get(query)
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
