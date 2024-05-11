import weaviate
import weaviate.classes as wvc
import os

client = weaviate.connect_to_wcs(
    cluster_url=os.getenv("WCS_URL"),
    auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WCS_API_KEY")),
    headers={
        "X-OpenAI-Api-Key": os.environ["OPENAI_APIKEY"]  # Replace with your inference API key
    }
)

try:
    pass # Replace with your code. Close client gracefully in the finally block.
    questions = client.collections.get("Question")

    response = questions.query.near_text(
        query="biology",
        limit=2
    )

    print(response.objects[0].properties)  # Inspect the first object

finally:
    client.close()  # Close client gracefully