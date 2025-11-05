from openai import OpenAI
import os
import csv

PATH = "./images/"
API_KEY = ""

# Function to upload a file with the OpenAI Files API
def upload(file_path):
  print(f"Uploading {file_path}")
  with open(file_path, "rb") as file_content:
    result = client.files.create(
        file=file_content,
        purpose="vision",
    )
    return result.id

# Initialize OpenAI client with API key
client = OpenAI(api_key=API_KEY)

# Get image files
images = sorted([entry for entry in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, entry))])

rows = []

for image in images:
    if not image.endswith(".jpg") and not image.endswith(".png"):
       continue
    print(f"Processing image {image}\n==========================")
    
    # Create empty conversation history
    conversation = [
    ]

    # upload the file
    file_id = upload(os.path.join(PATH, image))

    # generate initial instruction to OCR text
    conversation.append({
            "role": "user",
            "content": [
                {"type": "input_text", "text": "ocr this image and return only the text as best as can be recognized, without any other messaging"},
                {
                    "type": "input_image",
                    "file_id": file_id,
                },
            ],
        })
    
    # Create the response
    response = client.responses.create(
        model="gpt-5-nano",
        input=conversation,
        reasoning={"effort": "minimal"},
    )

    # clear conversation history to reduce context tokens
    # and populate with the OCR text we just got back
    # as the assistant (LLM) role
    text = " ".join(response.output_text.split())
    print(f"\nText: \n{text}")

    conversation = [{"role":"assistant","content":text}]
    
    # append user request for description 

    conversation.append({"role": "user", "content": "Describe this document in 1-3 sentences in English"})

    # generate LLM response
    response = client.responses.create(
        model="gpt-5-nano",
        input=conversation,
        reasoning={"effort": "minimal"},
    )

    # append response text to conversation
    conversation.append({"role":"assistant","content":response.output_text})
    description = response.output_text
    print(f"\nDescription: \n{description}")

    # append user request for language id
    conversation.append({"role": "user", "content": "identify the primary language of this document and return only the ISO 639 language code"})

    response = client.responses.create(
        model="gpt-5-nano",
        input=conversation,
        reasoning={"effort": "minimal"},
    )

    conversation.append({"role":"assistant","content":response.output_text})
    language = response.output_text
    print(f"\nLanguage: {language}\n\n")
    rows.append([image,text,description,language])
    break

with open("documents.csv","w",encoding="UTF-8") as outfile:
   outfile.write("file,text,description,language\n")
   writer = csv.writer(outfile)
   writer.writerows(rows)

for row in rows:
   with open(f"output/{row[0]}.txt","w",encoding="UTF-8") as outfile:
      outfile.write(f"Text:\n{row[1]}\n\nDescription:\n{row[2]}\n\nLanguage: {row[3]}")