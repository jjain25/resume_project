# import streamlit as st
# import google.generativeai as genai

# genai.configure(api_key="AIzaSyDzat6gY-WmuDOe1qljTVl_-nelpo9dvUU")

# model=genai.GenerativeModel("gemini-pro")
# chat=model.start_chat(history=[])

# def get_gemini_response(question):
#     response=chat.send_message(question,stream=True)
#     return response

# st.set_page_config(page_title="Q&A Demo")
# st.header("Gemini LLM Application")

# if 'chat_history' not in st.session_state:
#     st.session_state['chat_history'] = []

# input = st.text_input("Input:",key="input")
# submit=st.button("Ask the question")

# if submit and input:
#     response=get_gemini_response(input)
#     # add user query and response to session chat history
#     st.session_state['chat_history'].append(("You",input))
#     st.subheader("The Response is")
#     for chunk in response:
#         st.write(chunk.text)
#         st.session_state['chat_history'].append(("Bot",chunk.text))

# st.subheader("The Chat History is")

# for role,text in st.session_state['chat_history']:
#     st.write(f"{role}:{text}")




# Configure Gemini API
genai.configure(api_key="AIzaSyDzat6gY-WmuDOe1qljTVl_-nelpo9dvUU")

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Streamlit UI setup
st.set_page_config(page_title="Q&A with PDF")
st.header("Gemini LLM with PDF Q&A")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'pdf_text' not in st.session_state:
    st.session_state['pdf_text'] = ""

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    st.session_state['pdf_text'] = extract_text_from_pdf(uploaded_file)
    st.success("PDF uploaded and text extracted successfully!")

if st.session_state['pdf_text']:
    st.subheader("Extracted PDF Content (Preview)")
    st.text_area("PDF Text", st.session_state['pdf_text'], height=200)

    input = st.text_input("Ask a question based on the PDF content:")
    submit = st.button("Ask the question")

    if submit and input:
        # Combine PDF text with the user's question
        context = f"Context from PDF:\n{st.session_state['pdf_text']}\n\nQuestion: {input}"
        response = get_gemini_response(context)

        # Update session state with user query and response
        st.session_state['chat_history'].append(("You", input))
        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))

# Display chat history
st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
