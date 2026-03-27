from mcp.server.fastmcp import FastMCP
from src.job_api import fetch_linkedin_job,fetch_naukri_job


mcp = FastMCP(name="Job Recommendation System")

@mcp.tool()
async def fetch_linked(list_of_key):
    return fetch_linkedin_job(list_of_key)

@mcp.tool()
async def fetch_naukri(list_of_key):
    return fetch_naukri_job(list_of_key)


if __name__ == "__main__":
    mcp.run(transport="stdio")