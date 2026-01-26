from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GROQ_API_KEY")
if not key:
    print("No GROQ_API_KEY found")
else:
    client = Groq(api_key=key)
    print("Listing Groq models...")
    try:
        models = client.models.list()
        with open("models.txt", "w") as f:
            for m in models.data:
                f.write(m.id + "\n")
                print(m.id)
    except Exception as e:
        print(f"Error listing models: {e}")
