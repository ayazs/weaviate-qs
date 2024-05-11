import weaviate
import weaviate.classes as wvc
import os

with weaviate.connect_to_wcs(
    cluster_url=os.getenv("WCS_URL"),
    auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WCS_API_KEY")),
    headers={
        "X-OpenAI-Api-Key": os.environ["OPENAI_APIKEY"]  # Replace with your inference API key
    }
) as client:  # Use this context manager to ensure the connection is closed
    print(client.is_ready())


try:
    client.connect()
    questions = client.collections.get("Question")

    response = questions.query.near_text(
        query="biology",
        limit=2,
        filters=wvc.query.Filter.by_property("category").equal("ANIMALS")        
    )

    print(response.objects[0].properties)  # Inspect the first object
    
    
    questions = client.collections.get("Question")

    response = questions.generate.near_text(
        query="biology",
        limit=2,
        single_prompt="Explain {answer} as you might to a five-year-old."
    )

    print(response.objects[0].generated)  # Inspect the generated text
    
    
    questions = client.collections.get("Question")

    response = questions.generate.near_text(
        query="biology",
        limit=2,
        grouped_task="Write a tweet with emojis about these facts."
    )

    print(response.generated)  # Inspect the generated text    

finally:
    client.close()  # Close client gracefully