import streamlit as st
import openai
import toml
import base64
from PIL import Image
import yaml
from yaml.loader import SafeLoader
from utils import strip_spaces

secrets = toml.load(".secrets.toml")

api_key = secrets["openai"]["api_key"]

client = openai.OpenAI(api_key=api_key)

with open('app/config/prompts.yaml') as file:
    prompts = yaml.load(file, Loader=SafeLoader)

MODEL = "gpt-4o-mini"
DEFAULT_PROMPT = strip_spaces(prompts["gpt_4o_mini"]["ru"]["photo_recognition"])

def chat_with_file():
    st.header("Interact with ChatGPT using Uploaded File")
    st.write("Upload an image file and provide a prompt to ChatGPT to generate a response.")
    st.write(f"*Currently used model: {MODEL}*")
    
    def encode_file(file_path):
        """
        Reads a file, encodes it, and prepares it for sending to ChatGPT.
        """
        try:
            with open(file_path, "rb") as file:
                file_content = file.read()
            encoded_file = base64.b64encode(file_content).decode('utf-8')
            return encoded_file
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    @st.cache_data
    def chat_with_image(img_path, img_type, prompt):
        """
        Sends a file and a prompt to ChatGPT and gets the response.
        """
        print(img_path)
        encoded_file = encode_file(img_path)
        if not encoded_file:
            print("Failed to encode file.")
            return

        # Custom payload with file and prompt
        messages = [
            {"role": "system", "content": "You are an medical assistant skilled in extracting data from files."},
            {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{img_type};base64,{encoded_file}"},
                },
            ],
        }
            #     {"type": "text", "content": prompt},
            #     # {"type": "image_url", "image_url": f"data:{img_type};base64,{encoded_file}"},
            # ]}
        ]

        try:
            # Make API request
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                # temperature=0.5
            )
            return response
            
            
        except Exception as e:
            print(f"Error with ChatGPT API: {e}")
            st.error("An error occurred with ChatGPT API. Please try again later.")
            
    def display_response(response):
        st.subheader("ChatGPT Response:")
        print("Response from ChatGPT: ", response)
        # print(response["choices"][0]["message"]["content"])
        st.write(f"Response from ChatGPT: {response.choices[0].message.content}")
        with st.expander("Raw JSON Response"):
            st.json(response)

    # Usage

    uploaded_file = st.file_uploader("Upload a file (text-based)", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        file_type = uploaded_file.type
        st.write(f"Uploaded file type: {file_type}")
        file_name = uploaded_file.name
        file_path = f"temp/{file_name}"
        with open(file_path, "wb") as temp_image:
            temp_image.write(uploaded_file.read())
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        user_prompt = st.text_area("Enter your prompt for ChatGPT:", value=DEFAULT_PROMPT)
        
        if st.button("Chat with ChatGPT"):
            if user_prompt.strip():
                response = chat_with_image(file_path, file_type, user_prompt)
                display_response(response)
            else:
                st.error("Please provide a prompt for ChatGPT.")