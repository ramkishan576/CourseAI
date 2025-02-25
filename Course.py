# Required Libraries
import json
from difflib import get_close_matches
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Step 1: Load JSON data from a direct path
json_file_path = '/content/courses-list (1).json'  # Aapka direct path

with open(json_file_path, 'r') as file:
    course_data = json.load(file)

# Step 2: Prepare course data
def prepare_documents(course_data):
    documents = []
    for course in course_data:
        title = course.get('title', 'No Title Available')
        description = course.get('description', 'No Description Available')
        documents.append({
            "title": title,
            "name": course.get('name', 'No Name Available'),
            "url": course.get('url', 'No URL Available')
        })
    return documents

documents = prepare_documents(course_data)

# Step 3: Split Text for Embedding
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = []
for doc in documents:
    texts.extend(text_splitter.split_text(doc['content']))  # Use combined content instead of just title

# Step 4: Initialize OpenAI embeddings
GPT_API_KEY = "your api key"  # Apna actual OpenAI API key yahan daalein
embeddings = OpenAIEmbeddings(openai_api_key=GPT_API_KEY)

# Step 5: Create FAISS retriever
if texts:
    retriever = FAISS.from_texts(texts, embeddings)

# Step 6: Define the Prompt Template
def is_greeting(user_query):
    greetings = ["hello", "hi", "hey", "howdy", "greetings", "namaste", "salaam"]
    return any(greeting in user_query.lower() for greeting in greetings)

def is_faq(user_query):
    faq_queries = ["what is your name", "who are you", "how can you help me"]
    return any(faq in user_query.lower() for faq in faq_queries)

# Fuzzy Matching Function to Handle Short Queries
def get_best_match(query, documents):
    course_titles = [doc['title'] for doc in documents]
    best_match = get_close_matches(query, course_titles, n=1, cutoff=0.6)
    if best_match:
        return best_match[0]
    else:
        return None

# Suggest Course Function
def suggest_course(query):
    results = retriever.similarity_search(query, k=5)  # Increase k for more results

    if results:
        course_info = []
        for result in results:
            content = result.page_content
            for doc in documents:
                if content in doc['content']:
                    course_info.append((doc['title'], doc['name'], doc['url']))
                    break
        return course_info
    else:
        return "Mujhe aapke query ke according koi relevant courses nahi mile. Kripya thoda aur specific ho jayein."

# Step 7: User Interaction Loop
while True:
    user_input = input("Human: ").lower()  # Normalize user input
    if user_input == "exit":
        break

    if is_greeting(user_input):
        response = "Namaste! Aap kaise hain? Main yahan hoon aapki madad karne ke liye. Aap kis course mein interested hain?"
    elif is_faq(user_input):
        response = "Main aapki course ke suggestions mein madad karne wala ek assistant hoon. Aap mujhse kisi bhi course ke baare mein puchh sakte hain."
    else:
        response = suggest_course(user_input)

    print("AIMessage:")
    if isinstance(response, str):
        print(response)
    else:
        if response:
            for idx, (title, name, url) in enumerate(response, 1):
                print(f"{idx}. Title: {title}, Name: {name}, URL: {url}")
        else:
            print("Mujhe koi relevant course nahi mila.")
