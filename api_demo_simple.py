from openai import OpenAI

MODEL = "gpt-5-nano"
API_KEY = ""

# Initialize OpenAI client with API key
client = OpenAI(api_key=API_KEY)

# initialize the conversation with the system prompt
# and the first user message
conversation = [
    {"role": "system", "content": "You are Bobby Hill from King of the Hill. Respond only in character rather than as GPT."},
    {"role": "user", "content": "Generate a tight five comedy set and tell me the first bit."}
]

print(f"System prompt: {conversation[0]["content"]}")
print(f"\nInitial query: {conversation[1]["content"]}")

# Create the OpenAI response
response0 = client.responses.create(
    model=MODEL,
    input=conversation,
)

# Append the first response’s output to context to keep
# track of the conversation
conversation.append({"role":"assistant","content":response0.output_text})
print(f"\n\nReply: {conversation[-1]["content"]}")

# Add the next user message
conversation.append({ "role": "user", "content": "Continue to the next bit." })
print(f"\n\nUser: {conversation[-1]["content"]}")

# generate response
response1 = client.responses.create(
    model=MODEL,
    input=conversation,
)

# append the response
conversation.append({"role":"assistant","content":response1.output_text})
print(f"\n\nReply: {conversation[-1]["content"]}")

# Add the next user message
conversation.append({ "role": "user", "content": "Wrap up the set." })
print(f"\n\nUser: {conversation[-1]["content"]}")

# generate response
response2 = client.responses.create(
    model=MODEL,
    input=conversation,
)

# append the response
conversation.append({"role":"assistant","content":response2.output_text})
print(f"\n\nReply: {conversation[-1]["content"]}")