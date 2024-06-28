import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from lyzr_automata.tasks.task_literals import InputType, OutputType

st.set_page_config(
    page_title="HTML To ReactJS Convertor",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

api = st.sidebar.text_input("Enter Your OPENAI API KEY HERE", type="password")

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("HTML To ReactJS Convertor💻")
st.markdown("## Welcome to the HTML To ReactJS Convertor!")
st.markdown(
    "This App Harnesses power of Lyzr Automata to Convert HTML code to ReactJS. You Need to input Your HTML,CSS and JS code and it will convert it into ReactJS.")


if api:
    openai_model = OpenAIModel(
        api_key=api,
        parameters={
            "model": "gpt-4-turbo-preview",
            "temperature": 0.2,
            "max_tokens": 1500,
        },
    )
else:
    st.sidebar.error("Please Enter Your OPENAI API KEY")


def reactjs_conversion(html, css, javascript):
    react_agent = Agent(
        prompt_persona=f"You are a Frontend Engineer with over 10 years of experience.",
        role="Frontend Engineer",
    )

    react_task = Task(
        name="Dataset generation",
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=openai_model,
        agent=react_agent,
        log_output=True,
        instructions=f"""
        We need to convert an existing HTML design with css and js into a ReactJS application. 
        The conversion should result in a well-structured, maintainable, and performant React codebase. 
        Follow Below Instructions:
        
        **Component Structure**:
        Break down the HTML design into reusable React components.
        Define a clear component hierarchy, ensuring components are logically organized and nested.
        
        **State Management**:
        Identify which components will need to manage state.
        Decide whether to use React's built-in state management (useState, useReducer) or an external library (Redux, MobX).
        
        **Props and Data Flow**:
        Determine how data will flow between components.
        Clearly define the props each component will require and their types.
        
        Only give ReactJS Code nothing apart from it.
        
        HTML: {html}
        CSS: {css}
        JAVASCRIPT: {javascript}
        
        
        """,
        )

    output = LinearSyncPipeline(
        name="Dataset Generation",
        completion_message="Dataset Generated!",
        tasks=[
            react_task
        ],
    ).run()
    return output[0]['task_output']


col1, col2, col3 = st.columns(3)
with col1:
    html5 = st.text_area("Enter HTML code", height=300)

with col2:
    css3 = st.text_area("Enter CSS Code", height=300)

with col3:
    js = st.text_area("Enter JS code", height=300)


if st.button("Convert"):
    solution = reactjs_conversion(html5, css3, js)
    st.markdown(solution)
