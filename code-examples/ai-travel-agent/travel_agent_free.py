"""AI Travel Planner — free-LLM edition.

Adapted from Shubhamsaboo/awesome-llm-apps (starter_ai_agents/ai_travel_agent).
Instead of GPT-4o + SerpAPI, this version runs on any OpenAI-compatible free
provider from https://freellm.net (Groq, OpenRouter, Mistral, Cerebras, ...)
and uses DuckDuckGo for web search, so a single free API key is all you need.
"""

from textwrap import dedent
from datetime import datetime, timedelta
import re

import streamlit as st
from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.models.openai.like import OpenAILike
from agno.tools.duckduckgo import DuckDuckGoTools
from icalendar import Calendar, Event

# Free OpenAI-compatible providers — base URLs and model IDs from
# https://github.com/boristrade/awesome-freellm-apis (data: freellm.net)
PROVIDER_PRESETS = {
    "Groq (no credit card)": {
        "base_url": "https://api.groq.com/openai/v1",
        "model": "llama-3.3-70b-versatile",
        "key_url": "https://console.groq.com/keys",
    },
    "OpenRouter (free models)": {
        "base_url": "https://openrouter.ai/api/v1",
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "key_url": "https://openrouter.ai/settings/keys",
    },
    "Mistral AI (no credit card)": {
        "base_url": "https://api.mistral.ai/v1",
        "model": "mistral-small-latest",
        "key_url": "https://console.mistral.ai/api-keys",
    },
    "Cerebras (no credit card)": {
        "base_url": "https://api.cerebras.ai/v1",
        "model": "llama-3.3-70b",
        "key_url": "https://cloud.cerebras.ai/",
    },
    "Custom (any OpenAI-compatible)": {
        "base_url": "",
        "model": "",
        "key_url": "https://freellm.net/free-llm-api-keys/",
    },
}


def generate_ics_content(plan_text: str, start_date: datetime = None) -> bytes:
    """
        Generate an ICS calendar file from a travel itinerary text.

        Args:
            plan_text: The travel itinerary text
            start_date: Optional start date for the itinerary (defaults to today)

        Returns:
            bytes: The ICS file content as bytes
        """
    cal = Calendar()
    cal.add('prodid', '-//AI Travel Planner//github.com//')
    cal.add('version', '2.0')

    if start_date is None:
        start_date = datetime.today()

    # Split the plan into days
    day_pattern = re.compile(r'Day (\d+)[:\s]+(.*?)(?=Day \d+|$)', re.DOTALL)
    days = day_pattern.findall(plan_text)

    if not days:  # If no day pattern found, create a single all-day event with the entire content
        event = Event()
        event.add('summary', "Travel Itinerary")
        event.add('description', plan_text)
        event.add('dtstart', start_date.date())
        event.add('dtend', start_date.date())
        event.add("dtstamp", datetime.now())
        cal.add_component(event)
    else:
        # Process each day
        for day_num, day_content in days:
            day_num = int(day_num)
            current_date = start_date + timedelta(days=day_num - 1)

            # Create a single event for the entire day
            event = Event()
            event.add('summary', f"Day {day_num} Itinerary")
            event.add('description', day_content.strip())

            # Make it an all-day event
            event.add('dtstart', current_date.date())
            event.add('dtend', current_date.date())
            event.add("dtstamp", datetime.now())
            cal.add_component(event)

    return cal.to_ical()


# Set up the Streamlit app
st.title("AI Travel Planner — Free LLM Edition")
st.caption(
    "Plan your next adventure on a 100% free stack: any free LLM API from "
    "[freellm.net](https://freellm.net) for planning, DuckDuckGo for research. "
    "No OpenAI or SerpAPI key required."
)

# Initialize session state to store the generated itinerary
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None

with st.sidebar:
    st.header("LLM Provider")
    preset_name = st.selectbox("Free provider", list(PROVIDER_PRESETS))
    preset = PROVIDER_PRESETS[preset_name]
    base_url = st.text_input("Base URL", value=preset["base_url"])
    model_id = st.text_input("Model ID", value=preset["model"])
    api_key = st.text_input("API key", type="password", help=f"Get a free key: {preset['key_url']}")
    st.markdown(f"[Get a free API key →]({preset['key_url']})")
    st.caption("Browse all 30 free providers at [freellm.net/models](https://freellm.net/models/)")

if api_key and base_url and model_id:
    model_kwargs = dict(id=model_id, api_key=api_key, base_url=base_url)

    researcher = Agent(
        name="Researcher",
        role="Searches for travel destinations, activities, and accommodations based on user preferences",
        model=OpenAILike(**model_kwargs),
        description=dedent(
            """\
        You are a world-class travel researcher. Given a travel destination and the number of days the user wants to travel for,
        generate a list of search terms for finding relevant travel activities and accommodations.
        Then search the web for each term, analyze the results, and return the 10 most relevant results.
        """
        ),
        instructions=[
            "Given a travel destination and the number of days the user wants to travel for, first generate a list of 3 search terms related to that destination and the number of days.",
            "For each search term, use `web_search` and analyze the results.",
            "From the results of all searches, return the 10 most relevant results to the user's preferences.",
            "Remember: the quality of the results is important.",
        ],
        tools=[DuckDuckGoTools()],
        add_datetime_to_context=True,
    )
    planner = Agent(
        name="Planner",
        role="Generates a draft itinerary based on user preferences and research results",
        model=OpenAILike(**model_kwargs),
        description=dedent(
            """\
        You are a senior travel planner. Given a travel destination, the number of days the user wants to travel for, and a list of research results,
        your goal is to generate a draft itinerary that meets the user's needs and preferences.
        """
        ),
        instructions=[
            "Given a travel destination, the number of days the user wants to travel for, and a list of research results, generate a draft itinerary that includes suggested activities and accommodations.",
            "Ensure the itinerary is well-structured, informative, and engaging.",
            "Ensure you provide a nuanced and balanced itinerary, quoting facts where possible.",
            "Remember: the quality of the itinerary is important.",
            "Focus on clarity, coherence, and overall quality.",
            "Never make up facts or plagiarize. Always provide proper attribution.",
        ],
        add_datetime_to_context=True,
    )

    # Input fields for the user's destination and the number of days they want to travel for
    destination = st.text_input("Where do you want to go?")
    num_days = st.number_input("How many days do you want to travel for?", min_value=1, max_value=30, value=7)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Itinerary"):
            with st.spinner("Researching your destination..."):
                # First get research results
                research_results: RunOutput = researcher.run(f"Research {destination} for a {num_days} day trip", stream=False)

                # Show research progress
                st.write(" Research completed")

            with st.spinner("Creating your personalized itinerary..."):
                # Pass research results to planner
                prompt = f"""
                Destination: {destination}
                Duration: {num_days} days
                Research Results: {research_results.content}

                Please create a detailed itinerary based on this research.
                """
                response: RunOutput = planner.run(prompt, stream=False)
                # Store the response in session state
                st.session_state.itinerary = response.content
                st.write(response.content)

    # Only show download button if there's an itinerary
    with col2:
        if st.session_state.itinerary:
            # Generate the ICS file
            ics_content = generate_ics_content(st.session_state.itinerary)

            # Provide the file for download
            st.download_button(
                label="Download Itinerary as Calendar (.ics)",
                data=ics_content,
                file_name="travel_itinerary.ics",
                mime="text/calendar"
            )
else:
    st.info("Enter your free provider details in the sidebar to get started. Groq keys take under a minute — no credit card.")
