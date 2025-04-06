# Planning Center Online API and MCP Server Integration  

This project integrates the Planning Center Online (PCO) API with an MCP server to enable seamless interaction with a Large Language Model (LLM). The goal is to allow users to ask questions and retrieve data from Planning Center in a conversational manner.  

## Features  
- **PCO API Integration**: Connects to Planning Center Online to access and manage data.  
- **FASTMCP Server**: Acts as a middleware to handle requests and responses between the LLM and PCO API.  
- **LLM Query Support**: Enables natural language queries to fetch and manipulate data from Planning Center.  

## Use Cases  
- Retrieve information about services in Planning Center.  
- Automate workflows by querying and updating data using natural language.  
- Provide insights and analytics through conversational queries.  

## Getting Started  

### Prerequisites  
- Access to the [Planning Center API](https://developer.planningcenteronline.com/).  
- Python environment 
- MCP Client (i.e. Claude Desktop)
- API keys for authentication.  

### Installation  
1. Clone this repository:  
    ```bash  
    git clone https://github.com/your-repo/pco-mcp-integration.git  
    ```  
2. Install dependencies:  
    ```bash  
    uv pip install -r requirements.txt 
    ```  
3. Configure environment variables:  
    - `PCO_SECRET_KEY`: Your Planning Center API key.  
    - `PCO_APPLICATION_ID`: URL of the MCP server.  

4. Test the server:  
    ```bash  
    fastmcp dev services.py
    ```  

## Usage  
1. Send a natural language query to the MCP server.  
2. The server processes the query and interacts with the PCO API.  
3. Receive a structured response or perform the requested action.  

Add MCP server config
``` json
{
  "mcpServers": {
    "pco-services": {
      "command": "/Users/calvarychapelnewharvest/anaconda3/envs/mcp/bin/fastmcp",
      "args": [
        "run",
        "/Users/calvarychapelnewharvest/Documents/pco-mcp/services.py"
      ]
    }
  }
}
```

## Future Work
It is intended to continue work on other areas of planning center.

## Contributing  
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.  

## License  
This project is licensed under the [MIT License](LICENSE).  

## Resources  
- [Planning Center API Documentation](https://developer.planningcenteronline.com/)  
- [FastMCP](https://github.com/jlowin/fastmcp)  
- [pypco](https://github.com/billdeitrick/pypco)
