import streamlit as st
from streamlit.logger import get_logger
import openai
from PIL import Image

from datetime import datetime, timedelta

from src.chat import conversation_ui, prayer
from src.saints import dorothy, augustine, aquinas
from src.util import (
    scrape_vatican_word,
    scrape_vatican_saint,
    verse_extract,
    extract_text,
)

LOGGER = get_logger(__name__)

def run():

    st.set_page_config(
        page_title="Silicon Saint",
        page_icon="✝️",
        menu_items={
            "Get Help": "https://www.github.com/brickfrog/silicon-saint/issues",
            "About": """
            ### Silicon Saint
            An app to have a GPT 3.5 based conversation 
            on the gospel of the day with various characters
            of importance in the Catholic Church.
            """,
        },
    )

    st.markdown(
        """
        <h1 style="color:mediumorchid;text-align:center;">✝️ Silicon Saint</h1><br>
        """,
        unsafe_allow_html=True,
    )

    # This is a hacky way to center the image
    image = Image.open("app/static/generated_augustine.png")
    icol1, icol2, icol3 = st.columns([1, 3, 1])

    with icol1:
        st.write("")

    with icol2:
        st.image(
            image,
            width=400,
            caption='Saint Augustine, DALLE-2 generated. Prompt="“A stained glass image of Saint Augustine with a computer, purple highlights”"',
        )

    with icol3:
        st.write("")

    st.markdown(
        """
        <style>
        main {
        background-image: url("app/static/generated_augustine.png");
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """Silicon Saint is a gpt-3.5 analysis based on the Vatican's 
        [word of the day](https://www.vaticannews.va/en/word-of-the-day.html).
        Additionally contains information about the 
        [Saint(s)](https://www.vaticannews.va/en/saints.html) of the day. Each tab
        represents that information for the date (UTC+1), with the default representing the 
        spot for the generated conversation. ¹ I primarily made this for my own usage
        and to learn more about AI prompting 'characters'. ² It should be used as a 
        catalyst to think about the word of day, and for this reason it's limited to text
        for those.
        """
    )

    # This is for when I want users to use the API key, possibly when I deploy it
    # or hit my API limits
    try:
        api_key = st.secrets["key"]
    except:
        api_key = st.text_input(
            "Enter your OpenAI key, you need to register for an account lookup your keys [here](https://platform.openai.com/account/api-keys).",
            type="password",
        )

    openai.api_key = api_key

    # Horizontal line to divide the footnotes
    st.divider()

    dt = st.date_input(
        "This allows you to select previous dates if so inclined:", datetime.today()
    )
    today = dt.strftime("%Y/%m/%d")

    date_cutoff = datetime.today() + timedelta(days=1)
    if dt > date_cutoff.date():
        st.error("Date selected is in the future. May cause errors.")

    data = scrape_vatican_word(today)
    saints = scrape_vatican_saint(today)

    reading, gospel, word = data[0], data[1], data[2]

    verses = verse_extract(reading) + verse_extract(gospel)
    verses = verses[::-1] + [extract_text(word)]

    gpt_saints = [augustine, dorothy, aquinas]

    tab1, tab2, tab3, tab4 = st.tabs(
        ["**AI Dialogue**", "**AI Prayer Idea**", "Vatican Daily Readings", " Daily Saint(s)"]
    )

    # AI Dialogue
    with tab1:
        st.markdown(
            """
            This is the main part of the application, select from the dropdown and click generate. 
            The other tabs contain the input text readings for your convenience.
            """
        )

        names = [saint.name for saint in gpt_saints]
        option = st.selectbox(
            label="Select a Name to Generate a Conversation based on today's reading(s) as the selected character",
            options=names,
            help="This is the character that the model will be prompted on.",
        )

        selected_saint = gpt_saints[names.index(option)]
        st.write("")

        icol4, icol5 = st.columns([1, 5])

        with icol4:
            st.image(selected_saint.picture, width=100)

        with icol5:
            st.markdown(f"[{selected_saint.name}]({selected_saint.wiki})" + " was " + selected_saint.traits)

        st.divider()

        input_dialogue_flag = 0

        if st.button("Generate"):
            conversation_ui(verses, selected_saint)
            input_dialogue_flag = 1

        if input_dialogue_flag == 0:
            st.divider()

            with st.expander("Data Input"):
                st.write("These are the data inputs for the conversational model:")
                st.write(verses)
                st.write(selected_saint)

    # Prayer Request
    with tab2:
        st.write("Enter a prayer request and click generate to get a prayer idea.")
        prayer_input = st.text_input("Prayer Topic (Enter to confirm):", "I've lost an important document")

        if st.button("Prayer"):
            st.write(prayer(prayer_input))
    # Reading
    with tab3:
        st.markdown(reading, unsafe_allow_html=True)
        st.write("")
        st.markdown(gospel, unsafe_allow_html=True)
        st.write("")
        st.markdown(word, unsafe_allow_html=True)

    # Saint(s) of the day
    with tab4:
        st.write("Information about the Saint(s) of the day, using Wikipedia iframes:")
        st.caption(
            """
            For more obscure Saints, there might be no wikipedia article. 
            Apologies. I use a submit button cause I don't like spamming 
            Wikipedia / Streamlit doesn't let you edit the SameSite headers.
            """
        )
        with st.form("my_form"):
            submitted = st.form_submit_button("Load")
            if submitted:
                for saint in saints:
                    saint_text = (
                        "Saint "
                        + str(saint.contents[1].get_text()).split(",")[0].split(".")[-1]
                    )
                    st.markdown(saint, unsafe_allow_html=True)
                    st.markdown(saint_text)
                    st.markdown(
                        f'<iframe width="700" height="700" referrerpolicy="origin" src="https://wikipedia.org/w/index.php?title={saint_text}"></iframe>',
                        unsafe_allow_html=True,
                    )
                    st.write("")

    # Horizontal line to divide the footnotes
    st.divider()

    st.caption(
        """
    ¹ For all intents and purposes this is a context-stuffed version primed 
    on information about the character(s) selected, that is, the model probabilistically 
    takes the context and uses that to extrapolate guidance. Ideally, one would use 
    this as a starting point to ponder the readings. Being an AI model, one could get 
    erroneous or herectical results depending on input. Treat it as if you were 
    discussing religion with an acquaintance, defer matters of authority to your 
    priest or spiritual director where applicable.

    ² Inasmuch as a LLM (Large Language Model) that has memorized their works can be.
    Just reiterating that I'm a layperson and not a theologian, my github is 
    [here](https://www.github.com/brickfrog). I'm not affiliated with the Vatican in any way,
    if there's any issues with the content please let me know. You can find most of my 
    contact info by link jumping to my github.
    """
    )


if __name__ == "__main__":
    run()
