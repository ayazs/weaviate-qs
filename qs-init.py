import weaviate
import weaviate.classes as wvc
import os
import requests
import json

with weaviate.connect_to_wcs(
    cluster_url=os.getenv("WCS_DEMO_URL"),  # Replace with your WCS URL
    auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WCS_DEMO_RO_KEY")),  # Replace with your WCS key
    headers={'X-OpenAI-Api-key': os.getenv("OPENAI_APIKEY")}  # Replace with your vectorizer API key
) as client:  # Use this context manager to ensure the connection is closed
    print(client.is_ready())


try:
    collection_name = "Question"

    client.connect()    
    if not client.collections.exists(name=collection_name):    
        questions = client.collections.create(
            name=collection_name,
            vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
            generative_config=wvc.config.Configure.Generative.openai()  # Ensure the `generative-openai` module is used for generative queries
        )
        
    resp = requests.get('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
    data = json.loads(resp.text)  # Load data

    question_objs = list()
    for i, d in enumerate(data):
        question_objs.append({
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        })

    questions = client.collections.get("Question")
    questions.data.insert_many(question_objs)    
    
finally:
    client.close()  # Close client gracefully