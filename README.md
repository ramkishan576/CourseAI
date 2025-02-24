# CourseAI
CourseAi

Course Recommendation System

A course recommendation system that uses OpenAI's GPT model to suggest relevant courses based on user queries. The system processes user inputs, identifies the key topics, and fetches the most relevant courses from a dataset containing various course details.

Features

Suggests courses based on user queries related to topics such as Machine Learning, Data Science, Web Development, etc.
Uses GPT-4 for understanding the user's intent and providing accurate course suggestions.
Retrieves relevant courses with details like name, title, URL, and description.
Supports dynamic queries and returns the most relevant courses even for ambiguous or broad queries.
Technologies Used

Python: The primary programming language for the implementation.
OpenAI GPT-4: For intent recognition and natural language processing.
FAISS: For fast similarity search using embeddings to match courses with user queries.
JSON: For storing course data.
Installation

Step 1: Install Python Dependencies

To get started, clone the repository and install the required dependencies. Run the following commands in your terminal:

git clone https://github.com/ramkishan222/CourseAi.git
cd CourseAi
pip install -r requirements.txt
