import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

print(os.environ.get("OPENAI_API_KEY")) #key should now be available


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "I need a little text talking about technology and IA, use only 10 words.",
        }
    ],
    model="gpt-3.5-turbo"
)