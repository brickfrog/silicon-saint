import streamlit as st
import openai
import time

from typing import List

from src.saints import Saint


def conversation(verses: List, saint: Saint) -> str:

    if not verses or all(not verse for verse in verses):
        raise ValueError("Input list cannot be empty or contain only empty strings.")

    for position, verse in enumerate(verses):

        col1, col2 = st.columns([1, 3])

        with col1:
            st.image(saint.picture),
            width = (125,)
            caption = f"{saint.name}"

        with col2:
            with st.expander(f"{saint.name}", expanded=True):
                with st.spinner("Generating dialogue..."):
                    st.write(generate_conversation(position, verses, saint))

        time.sleep(3)
    # prevents None being displayed
    return ""


def generate_conversation(position: int, verses: List, saint: str) -> str:

    gospel = verses[0]

    # Crux of text, the verse / gospel
    if position == 0:
        verse_input = f"Explain {gospel} in your own words."
        writing_input = f"Tie contemporary events in relation to your life to the verse, offering quotes from your writings."
    else:
        verse_input = f"Explain {verses[position]} in your own words. How does it relate to {gospel}. Expand on the common themes."
        writing_input = ""

    # These are the main two inputs into the OpenAI model
    system_content = f"""
        You are {saint.name}. Talk in the first person.
        Use these traits to influence your style, do not mention directly: {saint.traits}.
        """

    user_content = f"""
        Use the following structure, separate each section with a newline:
        
        {verse_input}
        {writing_input}
        """

    # Adding a prayer at the end
    if position == len(verses) - 1:
        user_content = f"""
        Offer the thoughts of yourself in character on the words of the Pope: {verses[position]}
        Ponder on the significance of these words for the future and offer guidance 
        and a prayer for the reader
        """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ],
            temperature=0.7,
        )

        generated_text = response["choices"][0]["message"]["content"]

    except Exception as e:
        # Handle the exception appropriately
        raise ValueError(f"Failed to generate conversation: {e}")

    return generated_text
