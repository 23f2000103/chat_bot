import streamlit as st
import requests

st.title("AjraSakha AI Review Agent")

question = st.text_input("Ask a question")

if st.button("Submit"):

    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={
            "question": question
        }
    )

    data = response.json()

    # st.write(data) # for debugging showing the json format of the response

    if data["status"] == "success":

        st.subheader("AI Response")
        st.write(data["response"])

        st.subheader("Review Decision")
        st.write(data["review"]["decision"])

        st.subheader("Confidence")
        st.write(data["review"]["confidence"])

        #st.subheader("Issues") 
        #st.write(data["review"]["issues"])

        st.subheader("Matched Historical Question")
        st.write(
            data["review"]["matched_question"]
        )

        st.subheader("Matched Historical Answer")
        st.write(
            data["review"]["matched_answer"]
        )

        st.subheader("Human Escalation")
        st.write(
            data["human_escalation"]
        )

    else:

        st.error(
            data["message"]
        )