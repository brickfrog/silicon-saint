import streamlit as st
import openai
import time

from typing import List

from src.saints import Saint

def conversation_ui(verses: List, saint: Saint, language: str) -> str:

    if not verses or all(not verse for verse in verses):
        raise ValueError("Input list cannot be empty or contain only empty strings.")
    
    gospel_verses = verses[:1] + verses[-1:]

    for position, verse in enumerate(gospel_verses):
        col1, col2 = st.columns([1, 5])


        with col1:
            if position == 0:
                st.image(saint.picture, width = 100, caption = f"{saint.name}")

        with col2:
            header_string = f"{saint.name} on '{gospel_verses[0]}' with accompanying words frrom the Pope"
            
            if position == 0:
                st.write(header_string)

            with st.expander(f"...", expanded=True):
                with st.spinner("Generating dialogue..."):
                    st.write(conversation(position, verses, saint, language, "gospel"))

        time.sleep(2)
    else:
        reading_verses = verses[1:-1]
        col1, col2 = st.columns([1, 5])

        with col1:
            st.image(saint.picture, width = 100, caption = f"{saint.name}")
        with col2:
            if len(reading_verses) == 1:
                header_string = f"{saint.name} on '{reading_verses[0]}'"
            else:
                header_string = f"{saint.name} on " + " and ".join([f"'{s}'" for s in reading_verses[:-1]]) + f", and '{reading_verses[-1]}'"
            st.write(header_string)
            with st.expander(f"...", expanded=True):
                with st.spinner("Generating dialogue..."):
                    st.write(conversation(position, reading_verses, saint, language, "reading"))

    # prevents None being displayed
    return ""

@st.cache_data
def conversation(position: int, verses: List, saint: str, language: str, topic_chosen: str) -> str:

    # Crux of text, the verse / gospel
    if topic_chosen == "gospel" and position == 0:
        intro_input = "Introduction to post."
        verse_input = f"Explain {verses[0]} in your own words."
        ending_input = "This is the first half a response, do not treat this as a complete thought."
    else:
        intro_input = ""
        verse_input = f"Explain {verses} in your own words."
        ending_input = ""

    writing_input = f"Tie contemporary events in relation to your life to the verse, offering quotes from your writings."

    # These are the main two inputs into the OpenAI model
    # The first half, the system content, which 'primes' the proceeding prompt.
    system_content = f"""
        You are {saint.name}. Write your thoughts as if  you were penning a longform blog 
        post in {language} in the style of the New Yorker.
        """

    # The second half of the prompt, the input
    user_content = f"""
        Use the following structure, separate each section with a newline:
        
        {intro_input}
        {verse_input}
        {writing_input}
        {ending_input}
        """

    # Adding a prayer at the end
    if position == len(verses) - 1 and topic_chosen == "gospel":
        user_content = f"""
        This is the final section of a longform blog post.

        Offer the thoughts of yourself in character on the words of the Pope: {verses[position]}
        Ponder on the significance of these words for the future.
        Give something for the reader to think about during their day.
        Finally, offer a prayer for the reader
        """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ],
            temperature=0.65,
        )

        generated_text = response["choices"][0]["message"]["content"]

    except Exception as e:
        # Handle the exception appropriately
        st.error(ValueError(f"Failed to generate conversation: {e}"))
        st.stop()

    return generated_text

@st.cache_data
def prayer(input_text: str, language: 'English') -> str:

    if len(input_text) > 150:
        raise ValueError("Input text should be less than 150 characters.")

    system_content = f"""
    You are an extremely knowledgeable theologian, known for their moving and eloquent 
    writing. 
    You are asked to write a prayer for the topic in {language}, calling for 
    an intercession from a saint that is most relevant for the topic. 

    Make your prayer verbose and emotional.

    Ask for reformulation if the topic is inappropriate, an example of inappropriate
    would be sexual or illegal topics.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": f"The topic is: '{input_text}'"},
            ],
            temperature=0.65,
        )

        generated_text = response["choices"][0]["message"]["content"]

    except Exception as e:
        # Handle the exception appropriately
        st.error(ValueError(f"Failed to generate conversation: {e}"))
        st.stop()

    return generated_text