from openai import OpenAI
import os
import streamlit as st


api_key = os.environ['OPENAI_API_KEY']



def get_openai_response(prompt, temperature=0.1, top_p=1):
    """
    This function sends a prompt to the OpenAI API and returns the text completion.
    """
    response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {
            "role": "system",
            "content": """
            You are a specialised chatbot that can help me solve optimization problems using IBM Docplex. Particularly constraint satisfaction problems.

            I will present an assignment to you and will need your help to solve it. Do this by providing a solution to the problem, along with the code in Python programming language.

            When providing the solutions, clearly define the decision variables, constraints and objective function using mathematical notation.
            
            When providing the code solution, you will need to use IBM Docplex, docplex.cp.model.CpoModel, solver. Ensure your code can be run using this solver

            Keep the replies as short a possible, and clearly define all the steps you take to solve the problem.

            You should also be able to explain followup questions about the solution you provide.

            Always print out mathematical notations  python code when you are offering a solution

            """
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=temperature,
    max_tokens=2048,
    top_p=top_p,
    stream=True
    )
    # print(response)
    
    return response

if __name__ == "__main__":
    client = OpenAI(api_key=api_key)

    # Streamlit app layout
    st.title("CSP Tutor")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
          response = st.write_stream(get_openai_response(prompt))

        st.session_state.messages.append({"role": "assistant", "content": response})