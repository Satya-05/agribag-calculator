import os
import json
import re
import base64
from dotenv import load_dotenv
from groq import Groq

# Load API key
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

print("Groq OCR Engine loaded successfully!")

def encode_image(image_path):
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')



def extract_values_from_image(image_path):
    try:
        # Encode image to base64
        base64_image = encode_image(image_path)
        
        # Get file extension
        ext = os.path.splitext(image_path)[1].lower()
        media_type = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
        
        # Send to Groq
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{media_type};base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": """This image contains a handwritten register page with 4 sections side by side.
Each section has 2 columns: S.No (serial number) and KG's (weight in kg).
Each section has exactly 15 rows numbered sequentially.

Section 1: rows 1-15
Section 2: rows 16-30
Section 3: rows 31-45
Section 4: rows 46-60

IMPORTANT RULES:
- Extract ONLY the KG weight values
- Dash means decimal: "43-5" = 43.5, "42-5" = 42.5, "44-5" = 44.5
- Dot means decimal: "76·2" = 76.2, "72·6" = 72.6
- If a value has X, x, or strikethrough on it, return 0 (cancelled)
- If a value has letters like K, M, k, m next to it, ignore the letter and read only the number
- If a cell is EMPTY (no handwritten number visible), return 0
- If a cell has only a dash, dot, tick mark, or scribble, return 0
- Only return a non-zero value if you can clearly see a number written
- Each column MUST have EXACTLY 15 values

Return ONLY a JSON object, no extra text:
{
    "col1": [v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15],
    "col2": [v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15],
    "col3": [v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15],
    "col4": [v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15]
}"""
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        response_text = response.choices[0].message.content.strip()
        print(f"Groq response: {response_text}")
        
        # Clean response
        response_text = re.sub(r'```json|```', '', response_text).strip()
        
        # Parse JSON
        data = json.loads(response_text)
        
        col1 = [float(v) for v in data['col1']]
        col2 = [float(v) for v in data['col2']]
        col3 = [float(v) for v in data['col3']]
        col4 = [float(v) for v in data['col4']]
        
        # Pad to 15
        while len(col1) < 15: col1.append(0.0)
        while len(col2) < 15: col2.append(0.0)
        while len(col3) < 15: col3.append(0.0)
        while len(col4) < 15: col4.append(0.0)
        
        return col1[:15], col2[:15], col3[:15], col4[:15]
    
    except Exception as e:
        print(f"Error in Groq OCR: {e}")
        return [0.0]*15, [0.0]*15, [0.0]*15, [0.0]*15