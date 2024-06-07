"""first templates Flask app"""
import os
from flask import Flask, render_template, request, jsonify

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)

# Set up Azure Search client
search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")

# Set up Azure OpenAI client
openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_key = os.getenv("AZURE_OPENAI_KEY")
#openai_client = AzureOpenAI(endpoint=openai_endpoint, credential=AzureKeyCredential(openai_key))
openai_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

def search_documents(query, top_n):
    search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=AzureKeyCredential(search_key))
    results = search_client.search(search_text=query, top=top_n)
    return [doc["data_chunks"] for doc in results]


def get_openai_response(prompt, content):
    openai_client = AzureOpenAI(api_key=openai_key, api_version="2024-02-01",azure_endpoint=openai_endpoint)
    response = openai_client.chat.completions.create(
            model="gpt-35-turbo",
            messages=[
                {"role": "system", "content": "As an AI assistant, your main role is to assist people in finding answer to the CMC questions asked from user. You only answer based on the information here, not from your general knowledgere. Go to next line for answering each questions with Noun in it. Do not return markdown format. " + content},
                {"role": "user", "content": prompt},
                ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content



@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/prompt', methods=['POST'])
def prompt():
    data = request.get_json()
    if data is None or "prompt" not in data:
        return jsonify({"response": "ERROR: Missing prompt text in request body"}), 400

    prompt_text = data["prompt"]

    answer = ""
    final_content = ''
    top = 5
    documents = search_documents(prompt_text, top)
    for i in documents:        
        final_content = final_content + ' ' + i + ' '

    
    answer = get_openai_response(prompt_text, final_content)


    # Prepare the JSON response
    response = {"prompt": prompt_text, "response": answer}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)