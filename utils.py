import os
import openai
from typing import List, Dict, Any

def load_env_file(filepath: str = ".env"):
    """Simple .env loader to avoid external dependencies."""
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    value = value.strip()
                    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    os.environ[key.strip()] = value
    except FileNotFoundError:
        pass

# Load environment variables
load_env_file()

# client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 
try:
    if not os.getenv("OPENAI_API_KEY"):
         print("Warning: OPENAI_API_KEY not found in environment or .env file.")
    client = openai.OpenAI()
except Exception as e:
    print(f"Warning: OpenAI client could not be initialized. Error: {e}")
    client = None

def read_file(filepath: str) -> str:
    """Reads content from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(filepath: str, content: str) -> bool:
    """Writes content to a file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing to {filepath}: {e}")
        return False

def call_llm(messages: List[Dict[str, str]], model: str = "gpt-5.2") -> str:
    """Calls the OpenAI LLM with the given messages."""
    if not client:
        return "Error: OpenAI client not initialized."
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling LLM: {e}"
