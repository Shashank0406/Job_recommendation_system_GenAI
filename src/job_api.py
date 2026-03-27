from apify_client import ApifyClient
import os
from dotenv import load_dotenv
load_dotenv()

client = ApifyClient(token=os.getenv("APIFY_API_TOKEN"))

def fetch_linkedin_job(search_query,location='india',rows=5):
    run_input = {
        "title": search_query,
        "location": location,
        "rows": rows,
        "proxy": {
        "useApifyProxy": True,
        "apifyProxyGroups": ["RESIDENTIAL"],
        },

    }
    # Run the Actor and wait for it to finish
    run = client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    if run is None:
        return print("No run found for the given input.")
    jobs = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs

def fetch_naukri_job(search_query,location='india',rows=5):
    run_input = {
    "keyword": search_query,
    "maxJobs": 100,
    "freshness": "all",
    "sortBy": "relevance",
    "experience": "all",
    }
    # Run the Actor and wait for it to finish
    run = client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)
    if run is None:
        return print("No run found for the given input.")
    jobs = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs

