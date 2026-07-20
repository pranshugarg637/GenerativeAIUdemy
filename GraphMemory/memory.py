from dotenv import load_dotenv
from mem0 import Memory 
#It is responsible for
#  storing memories
# searching memories
# deleting memories
# updating memories
import os
import json

from openai import OpenAI

load_dotenv()

client = OpenAI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEO_USERNAME=os.getenv("NEO_USERNAME")
NEO_PASSWORD=os.getenv("NEO_PASSWORD")
NEO_URL=os.getenv("NEO_CONNECTION_URI")

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": { "api_key": OPENAI_API_KEY, "model": "text-embedding-3-small" }
    },
    "llm": {
        "provider": "openai",
        "config": { "api_key": OPENAI_API_KEY, "model": "gpt-4.1" }
    },
    "graph_store":{  # ab neo4j waale graph database mein bhi relations add honge
        "provider":"neo4j",
        "config":{
            "url":NEO_URL,
            "username":NEO_USERNAME,
            "password":NEO_PASSWORD
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

mem_client = Memory.from_config(config)
#now while chatting we just have to pass the chats to mem_client

while True:
    user_query = input("> ")
    search_memory = mem_client.search(query=user_query, user_id="piyushgarg",)

    memories = [
        f"ID: {mem.get("id")}\nMemory: {mem.get("memory")}" 
        for mem in search_memory.get("results")
    ]
    print("Found Memories", memories)

    SYSTEM_PROMPT = f"""
        Here is the context about the user:
        {json.dumps(memories)}
    """
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            { "role": "system", "content": SYSTEM_PROMPT },
            { "role": "user", "content": user_query }
        ]
    )

    ai_response = response.choices[0].message.content

    print("AI:", ai_response)
    mem_client.add(
        user_id="piyushgarg",
        messages=[
            { "role": "user", "content": user_query },
            { "role": "assistant", "content": ai_response }
        ]
    )

    print("Memory has been saved...")

#yaha pe ek searching and saving ka system chal raha hai. Jab user kuch query dega toh woh bangea user query and then uske baad mem_client ka search method search krega ki usse related kuch context uske paas hai kya? agar hai toh wahi woh aage system prompt mein as system query bhej dega llm ko ki yeh tha pehle ka context and iske basis pe aage continue kar chat. Lekin agar koi related information nahi hogi toh system prompt mein context khaali jaayega and wahi khaaali context paas hoga to llm to continue the chat further.

#Also ek important doubt mere man mein yeh aaya tha ki .search function kaise kaam krega.iss function mein kuch internal working hai (check kr sakta hai chatgpt ya ctrl + right click krke) jo apne aap semantic search perform kr legi based on the llm and embedding model passed.