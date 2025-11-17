import streamlit as st
import requests
from openai import OpenAI
import json
import plotly.express as px
import requests
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO  
import seaborn as sns
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import textwrap
import tiktoken

Mode='static' #options : 'static', 'dynamic'

# Page 1: Search
def page_search():
    try:
        st.markdown(
            """
            <h1 style='color: #FFD700; text-align:center; font-weight: bold; margin-top:30px;'>
                🚀 Brand Visibility & AI Engine Optimisation
            </h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <h6 style='color: #9E9E9E; text-align:center; margin-top:30px;'>
                "Monitor how your brand is being discussed and turn insights into smart, tactical actions that boost visibility."
            </h6>
            """,
            unsafe_allow_html=True
        )

        # --- Main UI ---
        st.markdown(
            """
            <style>
            .stTextInput> div>div>input {
                background-color:white;
                border:1px solid #FFD700;
                border-radius:10px;
                padding: 10px;
                font-size:16px;
            }
            ::placeholder{
                color:#cccccc;
            }
            .stButton>button{
                background-color: #FFD700;
                color: black;
                font-weight: 600;
                border-radius: 10px;
                border: none;
                padding: 10px 18 px;
                width: 100px;
                transition: all 0.3s ease;
            }
            .stButton>button:hover{
                background-color:#FFD700;
                box-shadow: 0 0 10px #FFD700;
                transform: scale(1.05);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='margin-top:30px'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([8, 1])
        with col1:
            title_input = st.text_input("", placeholder="🔎 Enter a brand name", label_visibility="collapsed")
        with col2:
            search_clicked = st.button("GO")

        if search_clicked and title_input.strip():
            st.session_state.brand_title = title_input.strip()
            st.session_state.page = 2
            st.rerun()
        elif search_clicked:
            st.warning("Please enter a brand name.")
    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")

def summary(data):
    # --- Navigation buttons ---
    try:
        col1, _, col2 = st.columns([1, 12, 1])
        with col1:
            if st.button("⬅ Back"):
                st.session_state.page = 1
                st.rerun()
        with col2:
            if st.button("Next ➡"):
                st.session_state.page = 3
                st.rerun()

        # --- Header ---
        st.markdown(
            "<h2 style='color:#FFD700; font-weight:bold; text-align:center; margin-top:20px;'>Verify Brand Details</h2>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='color:#9E9E9E; text-align:center;'>Make updates to ensure accuracy.</p>",
            unsafe_allow_html=True,
        )

    except Exception as e:
        st.error(f"⚠️ An error occurred while rendering this section: {e}")

    # --- Brand Details Section ---
    if data:
        st.markdown("""
        <style>
        /* Text input styling */
        .stTextInput>div>div>input {
            background-color: white;
            border: 1px solid #FFD700;
            border-radius: 10px;
            padding: 10px 18 px;
            font-size: 16px;
        }

        .stTextInput input::placeholder {
            color: #cccccc;
        }

        /* Text area styling */
        .stTextArea>div>div>textarea {
            background-color: white;
            border: 1px solid #FFD700;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        }

        </style>
    """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        try:
            with col1:
                st.markdown("<h4 style='color:#FFD700;'>Brand Title</h4>", unsafe_allow_html=True)
                st.session_state.brand_title = st.text_input(
                    "", 
                    value=st.session_state.brand_title, 
                    label_visibility="collapsed"
                )

            with col2:
                st.markdown("<h4 style='color:#FFD700;'>Brand URL</h4>", unsafe_allow_html=True)
                st.session_state.url = st.text_input(
                    "", 
                    value=data["url"], 
                    label_visibility="collapsed"
                )

            st.markdown("<h4 style='color:#FFD700;'>Brand Summary</h4>", unsafe_allow_html=True)
            st.session_state.summary = st.text_area(
                "", 
                value=data["summary"], 
                height=120, 
                label_visibility="collapsed"
            )

            # --- Generate Button ---
            col1, col2, col3 = st.columns([8, 1, 1])
            with col3:
                st.session_state.brand_confirm_clicked = st.button(
                    "Confirm",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"⚠️ An error occurred while loading brand data: {e}")

    else:
        st.warning(data["message"])
        st.session_state.brand_confirm_clicked = False

def website_analysis(Score_output):
    
    st.markdown(
    "<h2 style='color:#FFD700; font-weight:bold; text-align:center; margin-top:20px;'>Website Analysis Results</h2>",
    unsafe_allow_html=True,
    )
    # --- Styling for tabs ---
    st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        border: none !important;
        gap: 10px !important;
        justify-content: center !important;
    }
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #001f3f !important;
        color: #FFFFFF !important;
        border: 1px solid #FFD700 !important;
        border-radius: 10px !important;
        padding: 6px 14px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #FFD700 !important;
        color: black !important;
        box-shadow: 0 0 10px #FFD700 !important;
    }
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: #FFD700 !important;
        color: black !important;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Tabs ---
    try:
        tab_labels = list(Score_output.keys())
        tabs = st.tabs(tab_labels)
    except Exception as e:
        st.error(f"⚠️ An error occurred while creating tabs: {e}")

    try:
        for i, label in enumerate(tab_labels):
            section_data = Score_output[label]
            score = section_data.get("Score", 0)
            rating = section_data.get("Rating", "N/A")

            with tabs[i]:
                st.markdown(f"<h4 style='color:#FFD700;text-align:center;'>{label}</h4>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align:center;color:#FFD700; font-weight: 600;'> {rating}</p>", unsafe_allow_html=True)

                progress_html = f"""
                <div style='width:70%;margin:10px auto;background-color:white;border-radius:8px;height:15px;position:relative;border: 2px solid #FFD700;'>
                    <div style='width:{score}%;background-color:#FFD700;height:100%;border-radius:8px;'></div>
                    <div style='position:absolute;top:-20px;left:50%;transform:translateX(-50%);color:#FFD700;font-weight:600;font-size:12px;'>
                        Score: {score}%
                    </div>
                </div>
                """
                st.markdown(progress_html, unsafe_allow_html=True)

                for section, color in [("Highlights", "#FFD700"), ("Recommendations", "#FFD700")]:
                    html = f"""
                    <div style='background-color:#001f3f;color:white;padding:12px; 
                                border-radius:10px;margin:10px 0;text-align:left;'>
                        <h5 style='color:{color};margin-bottom:5px;'>{section}:</h5>
                        <ul style='padding-left:20px;'>
                            {''.join(f"<li>{item}</li>" for item in section_data.get(section, []))}
                        </ul>
                    </div>
                    """
                    st.markdown(html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"⚠️ An error occurred while displaying the tab content: {e}")

def page_focus():
    try:
        brand_offerings_output = st.session_state.BrandOfferings
    except Exception as e:
        st.error(f"⚠️ An error occurred while accessing BrandOfferings: {e}")

    try:
        # --- Navigation buttons ---
        col1, _, col2 = st.columns([1, 12, 1])
        with col1:
            if st.button("⬅ Back"):
                if "BrandOfferings" in st.session_state:
                    del st.session_state["BrandOfferings"]
                st.session_state.page = 2
                st.rerun()
        with col2:
            if st.button("Next ➡"):
                st.session_state.page = 4
                st.rerun()

    except Exception as e:
        st.error(f"⚠️ An error occurred while handling navigation: {e}")


    # --- Title ---
    st.markdown(
    "<h2 style='color:#FFD700; font-weight:bold; text-align:center; margin-top:20px;'>Select Analysis Focus</h2>",
    unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin-top: 20px; color: #9E9E9E; font-size: 16px; line-height: 1.5;'>
        Defining a clear focus product line or service improves the relevance and accuracy of your results.
    </div>
    """, unsafe_allow_html=True)

    # --- Render radio buttons if data exists ---
    try:
        if brand_offerings_output:
            # Add an extra option to proceed with brand only
            brand_offerings_output = ["Proceed with brand only"] + brand_offerings_output    

            # Ensure first item selected by default
            default_index = 0
            if st.session_state.get("selectedProduct") in brand_offerings_output:
                default_index = brand_offerings_output.index(st.session_state.selectedProduct)

            st.session_state.selectedProduct = st.radio(
                "",
                brand_offerings_output,
                index=default_index,
                key="focus_radio",
                horizontal=True 
            )

            st.markdown(
                f"<p class='selected-text'>You selected: {st.session_state.selectedProduct}</p>",
                unsafe_allow_html=True
            )
        else:
            st.info("No products found.")

    except Exception as e:
        st.error(f"⚠️ An error occurred while displaying brand offerings: {e}")


    # --- CSS for card-style radio buttons ---
    st.markdown("""
    <style>
    /* Make the radio group container wrap tightly */
    [data-testid="stRadio"] div[role="radiogroup"] {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 20px;
        padding: 0 !important;
        margin: 0 !important; /* remove extra margin */
        height: auto !important; /* shrink container height */
    }

    [data-testid="stRadio"] input[type="radio"] {
        opacity: 0 !important;
        width: 100% !important;
        height: 100% !important;
        cursor: pointer;
    }


    /* Card-style labels (only real radio buttons) */
    [data-testid="stRadio"] label:has(input[type="radio"]) {
        display: inline-flex !important;
        align-items: center;
        justify-content: center;
        min-width: 220px;
        min-height: 80px;
        background: #777C6D;
        border: 1px solid #444;
        border-radius: 16px;
        padding: 16px 20px;
        cursor: pointer;
        transition: all 0.25s ease-in-out;
        font-size: 18px;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        text-align: center;
    }
    [data-testid="stRadio"] label:has(input[type="radio"]) * {
        color: #FFFFFF !important;
    }
    /* Hover effect (without transform) */
    [data-testid="stRadio"] label:has(input[type="radio"]):hover {
        background: linear-gradient(145deg, #272727, #2A2A2A);
        color: #FFD700; !important;
        box-shadow: 0 8px 16px rgba(255,215,0,0.25);
    }

    /* Selected card effect */
    [data-testid="stRadio"] label:has(input[type="radio"]:checked) {
        background: #748873;
        border-left: 4px solid #FFD700;
        color: #FFD700 !important;
        box-shadow: 0 8px 18px rgba(255,215,0,0.4);
        transform: scale(1.04);
    }
    /* Selected text below cards */
    .selected-text {
        color: #FFD700;
        font-weight: 500;
        margin-top: 15px;
        text-align: center;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <style>
    /* Center the radio group container */
    [data-testid="stRadio"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin-top: 20px !important;
    }

    /* Ensure buttons wrap neatly in the center */
    [data-testid="stRadio"] div[role="radiogroup"] {
        justify-content: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

def page_persona():
    try:
        # --- Navigation buttons ---
        col1, _, col2 = st.columns([1, 12, 1])
        with col1:
            if st.button("⬅ Back"):
                if "personas" in st.session_state:
                    del st.session_state["personas"]
                st.session_state.page = 3
                st.rerun()
        with col2:
            if st.button("Next ➡"):
                st.session_state.page = 5
                st.rerun()

    except Exception as e:
        st.error(f"⚠️ An error occurred while handling navigation: {e}")

    # --- Title ---
    st.markdown(
        "<h2 style='color:#FFD700; font-weight:bold; text-align:center; margin-top:20px;'>Review Target Personas</h2>",
        unsafe_allow_html=True,
    )
    st.markdown("""
    <div style='text-align: center; margin-top: 20px; color: #9E9E9E; font-size: 16px; line-height: 1.5;'>
        These personas were generated from your report focus. They help simulate different customer types in AI responses.
    </div>
    """, unsafe_allow_html=True)
    
    # --- Display personas as cards ---
    st.markdown("""
    <style>
    .card {
        width: 100%;
        background: #777C6D;
        color: black;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        margin-bottom: 20px;
    }
    .persona-name {
        font-size: 20px;
        font-weight: 700;
        color: #FFD700;
        display: flex;
        align-items: center;
        margin-bottom: 8px;
    }
    .persona-avatar {
        font-size: 26px;
        margin-right: 10px;
    }
    .persona-desc {
        font-size: 15px;
        color: black;
        margin-bottom: 12px;
    }
    .persona-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    .persona-tag {
        background-color: white;
        color: black;
        border: 1px solid #FFD700;
        font-size: 13px;
        border-radius: 12px;
        padding: 5px 12px;
    }
    </style>
    """, unsafe_allow_html=True)

    try:
        for p in st.session_state.personas:
            st.markdown(f"""
            <div class="card">
                <div class="persona-name">
                    <span class="persona-avatar">{p['Avatar']}</span>{p['Name']}
                </div>
                <div class="persona-desc">{p['Description']}</div>
                <div class="persona-tags">
                    {''.join([f"<div class='persona-tag'>{c}</div>" for c in p['Characteristics']])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"⚠️ An error occurred while displaying personas: {e}")

    try:
        # --- Add Persona ---
        st.markdown("""
        <style>
        /* Make ONLY the expander header white */
        details > summary {
            background-color: white !important;
            color: black !important;
            border-radius: 8px !important;
            padding: 8px !important;
        }

        /* Optional: make the inside area white as well */
        details[open] > div {
            background-color: #777C6D !important;
            padding: 10px !important;
            border-radius: 0 0 8px 8px !important;
            
        }
        
        /* Make labels inside the expander visible */
        details[open] label {
            color: white !important;
            font-weight: 500 !important;
        }

        </style>
        """, unsafe_allow_html=True)
        with st.expander("➕ Add New Persona", expanded=False):
            avatar = st.text_input("Avatar (emoji)", value="👤")
            name = st.text_input("Name")
            description = st.text_area("Description")
            characteristics = st.text_area("Characteristics (comma-separated)")
            if st.button("Add Persona"):
                if name.strip():
                    st.session_state.personas.append({
                        "Avatar": avatar or "👤",
                        "Name": name.strip(),
                        "Description": description.strip(),
                        "Characteristics": [c.strip() for c in characteristics.split(",") if c.strip()]
                    })
                    st.success(f"Added {name.strip()}")
                    st.rerun()

    except Exception as e:
        st.error(f"⚠️ An error occurred while adding a new persona: {e}")

    try:
        # --- Delete Persona ---
        if st.session_state.personas:
            with st.expander("🗑️ Delete Persona", expanded=False):
                del_name = st.selectbox("Select persona to delete", [p["Name"] for p in st.session_state.personas])
                if st.button("Delete Persona"):
                    st.session_state.personas = [p for p in st.session_state.personas if p["Name"] != del_name]
                    st.success(f"Deleted {del_name}")
                    st.rerun()

    except Exception as e:
        st.error(f"⚠️ An error occurred while deleting a persona: {e}")


    # Topics section
    st.markdown(
        "<h2 style='color:#FFD700; font-weight:bold; text-align:center; margin-top:20px;'>Topics</h2>",
        unsafe_allow_html=True,
    )
    st.markdown("""
    <div style='text-align: center; margin-top: 20px; color: #9E9E9E; font-size: 16px; line-height: 1.5;'>
        Topics are broad areas of interest. We combine them with personas to generate prompts that reflect how your customers might engage with AI.
    </div>
    """, unsafe_allow_html=True)

    # Render topics as cards
    try:
        # Render topics as cards
        for i in range(0, len(st.session_state.topics), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(st.session_state.topics):
                    topic_name = st.session_state.topics[i + j]
                    col.markdown(f"""
                        <div style='
                            border: 1px solid #FFD700;
                            border-radius: 12px;
                            padding: 15px;
                            margin: 10px 0;
                            background-color: #777C6D;
                            font-size: 16px;
                            color: black;
                            text-align: center;
                            cursor: pointer;
                            transition: all 0.2s ease-in-out;
                        '>{topic_name}</div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"⚠️ An error occurred while rendering topics: {e}")


    # --- Add Topic ---
    try:
        # --- Add Topic ---
        with st.expander("➕ Add New Topic"):
            new_topic = st.text_input("Topic Name", key="new_topic")
            if st.button("Add Topic", key="add_topic"):
                if new_topic.strip():
                    st.session_state.topics.append(new_topic.strip())
                    st.success(f"Added {new_topic.strip()}")
                    st.rerun()

    except Exception as e:
        st.error(f"⚠️ An error occurred while adding a new topic: {e}")

    # --- Delete Topic ---
    try:
        if st.session_state.topics:
            with st.expander("🗑️ Delete Topic"):
                del_topic = st.selectbox("Select Topic to delete", st.session_state.topics, key="del_topic")
                if st.button("Delete Topic", key="delete_topic"):
                    st.session_state.topics = [t for t in st.session_state.topics if t != del_topic]
                    st.success(f"Deleted {del_topic}")
                    st.rerun()

    except Exception as e:
        st.error(f"⚠️ An error occurred while deleting a topic: {e}")

def page_prompt():
    # --- Navigation buttons ---
    try:
        col1, _, col2 = st.columns([1, 12, 1])
        with col1:
            if st.button("⬅ Back"):
                if "brandprompts" in st.session_state:
                    del st.session_state["brandprompts"]
                st.session_state.page = 4
                st.rerun()
        with col2:
            if st.button("Next ➡"):
                st.session_state.page = 6
                st.rerun()

    except Exception as e:
        st.error(f"⚠️ An error occurred while handling navigation: {e}")

  
    # --- Page title ---
    st.markdown(
        "<h2 style='color:#FFD700; font-weight:bold; text-align:center; margin-top:20px;'>Prompts by Persona</h2>",
        unsafe_allow_html=True
    )

    # --- CSS styling ---
    st.markdown("""
    <style>

    .prompt-box {
        background-color: #777C6D;
        border: 1px solid #444;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        color: black;
    }
    .prompt-question {
        font-weight: 600;
        margin-bottom: 10px;
        font-size: 16px;
    }
    .response-box {
        background-color: white;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 8px;
        font-size: 14px;
        box-shadow: inset 0 0 3px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        /* Make ONLY the expander header white */
        details > summary {
            background-color: white !important;
            color: black !important;
            border-radius: 8px !important;
            padding: 8px !important;
        }

        /* Optional: make the inside area white as well */
        details[open] > div {
            background-color: #777C6D !important;
            padding: 10px !important;
            border-radius: 0 0 8px 8px !important;
            
        }
        
        /* Make labels inside the expander visible */
        details[open] label {
            color: white !important;
            font-weight: 500 !important;
        }

        </style>
        """, unsafe_allow_html=True)

    # --- Render prompts ---
    try:
        for persona in st.session_state.brandprompts:
            with st.expander(f"👤 {persona['Persona Role']}", expanded=True):
                # Two prompts per row
                for i in range(0, len(persona["Prompts"]), 2):
                    cols = st.columns(2)
                    for j, col in enumerate(cols):
                        if i + j < len(persona["Prompts"]):
                            p = persona["Prompts"][i + j]
                            with col:
                                st.markdown(
                                    f"""
                                    <div class="prompt-box">
                                        <div class="prompt-question">{p['Prompt']}</div>
                                        {''.join(f'<div class="response-box">{r}</div>' for r in p['Relevant Topics'])}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                # --- Delete Prompt (specific to this persona) ---
                if persona["Prompts"]:
                    with st.expander("🗑️ Delete Prompt"):
                        prompt_texts = [p["Prompt"] for p in persona["Prompts"]]
                        selected_prompt = st.selectbox(
                            "Select Prompt to Delete",
                            prompt_texts,
                            key=f"del_prompt_{persona['Persona Role']}"
                        )

                        if st.button("Delete Selected Prompt", key=f"delete_btn_{persona['Persona Role']}"):
                            persona["Prompts"] = [
                                p for p in persona["Prompts"] if p["Prompt"] != selected_prompt
                            ]
                            st.success(f"Deleted prompt: {selected_prompt}")
                            st.rerun()


    except json.JSONDecodeError:
        st.error("Invalid JSON. Check model output formatting.")

def page_Results(kpi_output):
    # --- Navigation buttons ---
    try:
        col1, _, col2 = st.columns([1, 12, 1])
        with col1:
            if st.button("⬅ Back"):
                if "kpi_output" not in st.session_state:
                    del st.session_state["kpi_output"]                
                st.session_state.page = 5 
                st.rerun()
        with col2:
            if st.button("Next ➡"):
                st.session_state.page = 7
                st.rerun()

    except Exception as e:
        st.error(f"⚠️ An error occurred while handling navigation: {e}")

    #................................................................................
    # Main UI UX

        # Function to render HTML table
    def make_table(df):
        try:
            table_html = '<table style="width:100%; border-collapse: collapse;">'
            # Header row with orange text
            table_html += '<tr style="text-align:center; color:black; background-color:#777C6D;">'
            for col in df.columns:
                table_html += f'<th>{col}</th>'
            table_html += '</tr>'
            # Data rows
            for _, row in df.iterrows():
                table_html += '<tr style="text-align:center; background-color:white; color:black;">'
                for val in row:
                    table_html += f'<td>{val}</td>'
                table_html += '</tr>'
            table_html += '</table>'
            return table_html
        
        except Exception as e:
            return f"<p style='color:red;'>⚠️ Error generating table: {e}</p>"

    #     st.pyplot(fig)
    def plot_visibility_chart(df, label_col):
        try:
            df["Visibility Percentage"] = (
                df["Visibility Percentage"].astype(str).str.replace("%", "").astype(float)
            )
            df = df.sort_values("Visibility Percentage", ascending=False)

            # Normalize colors
            norm = mcolors.Normalize(vmin=df["Visibility Percentage"].min(),
                                    vmax=df["Visibility Percentage"].max())
            cmap = cm.get_cmap("Oranges")
            colors = [cmap(norm(val)) for val in df["Visibility Percentage"]]

            fig, ax = plt.subplots(figsize=(7, 7), facecolor="none")
            ax.set_facecolor("black")

            # Wrap long labels
            wrapped_labels = [textwrap.fill(label, 25) for label in df[label_col]]

            wedges, texts, autotexts = ax.pie(
                df["Visibility Percentage"],
                labels=wrapped_labels,
                autopct="%1.1f%%",
                startangle=90,
                pctdistance=0.8,
                colors=colors,
                textprops={"color": "white", "fontsize": 10, "fontweight": "bold"},
                wedgeprops={"edgecolor": "black", "linewidth": 0.5}  # ← adds clear borders
            )

            # Donut hole
            centre_circle = plt.Circle((0, 0), 0.55, fc="white")
            fig.gca().add_artist(centre_circle)

            ax.set_title(f"{label_col} Visibility Share", pad=15, color="white", fontsize=20)

            ax.axis("equal")  # ensures circle shape
            plt.tight_layout()
            st.pyplot(fig)

        except Exception as e:
            st.error(f"⚠️ An error occurred while generating the pie chart: {e}")

    def styled_header(title: str, icon: str = "📊"):
        """
        Displays a styled centered header with orange background and white text.

        Args:
            title (str): Header text (e.g., 'Leaderboard', 'Persona Visibility').
            icon (str): Emoji icon to display before the title.
        """
        try:
            st.markdown(
                f"""
                <div style="
                    color: #FFD700;
                    padding: 10px 0;
                    border-radius: 8px;
                    text-align: center;
                    font-weight: 600;
                    font-size: 22px;
                    margin-bottom: 20px;
                ">
                    {icon} {title}
                </div>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"⚠️ An error occurred while displaying the header: {e}")

    # Brand Visibility
    try:
        if "Brand Visibility" in kpi_output:
            styled_header("Brand Visibility", "🔍")

            brand_count = int(kpi_output["Brand Visibility"][f"Count of {st.session_state.brand_title}"])
            competitor_count = int(kpi_output["Brand Visibility"]["Count of Brand's Competitors"])
            total_mentions = brand_count + competitor_count
            visibility = kpi_output["Brand Visibility"]["Brand Visibility %"]

            brand_visibility = kpi_output["Brand Visibility"]["Brand Visibility %"]
            
            # Progress bar background (100%)
            st.markdown(f"""
                <div style="
                    width: 100%;
                    height: 25px;
                    background-color: #f0f0f0;
                    border-radius: 20px;
                    overflow: hidden;
                    margin-bottom: 10px;
                ">
                    <div style="
                        width: {brand_visibility}%;
                        height: 100%;
                        background-color: #777C6D;
                        text-align: right;
                        padding-right: 10px;
                        color: white;
                        font-weight: bold;
                        border-radius: 20px;
                    ">
                        {brand_visibility}%
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Close the outer container
            st.markdown("</div>", unsafe_allow_html=True)

            # Display in Streamlit - Paraphrased text
            brand_visibility_text = (
                f"Insights: Out of all the AI responses for prompts & conversations, {total_mentions} brand mentions were identified, "
                f"out of which {st.session_state.brand_title} appeared {brand_count} times, representing {visibility}% of the total mentions."
            )
            st.markdown(f"<span style='color:white'>{brand_visibility_text}</span>", unsafe_allow_html=True)


    except Exception as e:
        st.error(f"⚠️ An error occurred while displaying Brand Visibility: {e}")

    try:
        if "Leaderboard" in kpi_output:
            styled_header("Competitive Benchmarking / Rank", "🏆")
            
            leaderboard_data = kpi_output["Leaderboard"]
            leaderboard_df = pd.DataFrame(leaderboard_data)

            # Ensure numeric columns
            leaderboard_df["Mention Count"] = leaderboard_df["Mention Count"].astype(int)
            leaderboard_df["Rank"] = leaderboard_df["Mention Count"].rank(method="dense", ascending=False).astype(int)

            brand_info = next(
                (b for b in leaderboard_data if b["Brand Name"].lower() == st.session_state.brand_title.lower()),
                None
            )

            if brand_info:

                st.markdown(
                    f"<span style='color:white'>The brand <b>{st.session_state.brand_title}</b> received <b>{brand_info['Mention Count']}</b> mentions, "
                    f"ranking <b>#{brand_info['Rank']}</b> among all mentioned brands in the report.</span>",
                    unsafe_allow_html=True
                )

            else:
                st.markdown(
                    "<span style='color:white'>The table displays the most mentioned brands along with their rank and mention count based on AI responses.</span>",
                    unsafe_allow_html=True
                )

            leaderboard_df = leaderboard_df.rename(columns={
                "Brand Name": "Brand",
                "Percentage Share": "Visibility Percentage",
                "Mention Count": "Mention Count",
                "Rank": "Rank"
            }).sort_values(by="Rank").reset_index(drop=True)
            st.markdown(make_table(leaderboard_df), unsafe_allow_html=True)
           

    except Exception as e:
        st.error(f"⚠️ An error occurred while displaying the Leaderboard: {e}")


    col1,col2=st.columns(2)

    with col1:
        try:
            # Persona Visibility Table
            if "Persona Visibility" in kpi_output:
                styled_header("Persona Visibility", "👤")

                st.markdown(
                    "<span style='color:white'>We generate relevant personas and provide AI prompts from their perspective to analyze how often your brand appears in their responses.</span>",
                    unsafe_allow_html=True
                )
                # Convert to DataFrame
                persona_df = pd.DataFrame(kpi_output["Persona Visibility"])
                persona_df = persona_df.rename(columns={
                    "Persona Name": "Persona",
                    "Visibility Percentage": "Visibility Percentage"
                })

                plot_visibility_chart(persona_df, "Persona")

        except Exception as e:
            st.error(f"⚠️ An error occurred while displaying Persona Visibility: {e}")

    with col2:
        try:
            # Topic Visibility Table
            if "Topic Visibility" in kpi_output:
                styled_header("Topic Visibility", "💬")
                st.markdown(
                    "<span style='color:white'>This indicates how frequently your brand is mentioned in AI responses across important topics. Higher visibility reflects stronger alignment with your interests.</span>",
                    unsafe_allow_html=True
                )
                # Convert to DataFrame
                topic_df = pd.DataFrame(kpi_output["Topic Visibility"])
                topic_df = topic_df.rename(columns={
                    "Topic": "Topic",
                    "Visibility Percentage": "Visibility Percentage"
                })

                plot_visibility_chart(topic_df, "Topic")

        except Exception as e:
            st.error(f"⚠️ An error occurred while displaying Topic Visibility: {e}")


    try:
        # Consumer Attributes Chart
        if "Consumer Attributes" in kpi_output:
            styled_header("Consumer Attribute", "🛒")
            st.markdown(
                "<span style='color:white'>Through AI responses, we identify the key consumer attributes associated with the brand and their percentage weight among all mentions.</span>",
                unsafe_allow_html=True
            )

            data = kpi_output.get("Consumer Attributes", [])
            if not data:
                st.warning("No Consumer Attributes data available.")
            else:
                consumer_df = pd.DataFrame(data)

                # Normalize column names
                consumer_df.columns = consumer_df.columns.str.strip()
                rename_map = {}
                if "Consumer Attribute" in consumer_df.columns:
                    rename_map["Consumer Attribute"] = "Attribute"
                if "Visibility Percentage" in consumer_df.columns:
                    rename_map["Visibility Percentage"] = "Percentage"
                consumer_df = consumer_df.rename(columns=rename_map)

                # Convert percentage strings to floats
                if "Percentage" in consumer_df.columns:
                    consumer_df["Percentage"] = (
                        consumer_df["Percentage"].astype(str)
                        .str.replace("[^0-9.]", "", regex=True)
                        .replace("", np.nan)
                        .astype(float)
                    )

                consumer_df = consumer_df.dropna(subset=["Percentage"])
                if consumer_df.empty:
                    st.warning("No valid percentage data to plot.")
                else:
                    # Dynamic color shades based on number of rows
                    shades = px.colors.sample_colorscale(
                        "Oranges", [i/(len(consumer_df)-1 or 1) for i in range(len(consumer_df))]
                    )

                    # Plot pie chart
                    fig = px.pie(
                        consumer_df,
                        names="Attribute",
                        values="Percentage",
                        hole=0.0,
                        color_discrete_sequence=shades
                    )

                    fig.update_traces(
                        marker=dict(line=dict(color="#FFFFFF", width=2)),
                        textposition="outside",
                        textinfo="label+percent",
                        pull=[0.0]*len(consumer_df),
                        showlegend=True,
                        automargin=True
                    )

                    fig.update_layout(
                        legend=dict(
                            orientation="v",
                            yanchor="middle",
                            y=0.5,
                            xanchor="left",
                            x=1.05
                        ),
                        margin=dict(l=20, r=150, t=40, b=20),
                        height=300  # width is responsive with use_container_width=True
                    )

                    st.plotly_chart(fig, use_container_width=True)
            
    except :
        st.error(f"Consumer Attribute KPI error")

    try:
        # Top Sources Table
        if "Top Sources" in kpi_output:
            
            styled_header("Top Sources", "")

            st.markdown(
                    "<span style='color:white'>Discover the domains that are most commonly highlighted in AI responses alongside your brand.</span>",
                    unsafe_allow_html=True
                )

            # Create DataFrame
            sources_df = pd.DataFrame(kpi_output["Top Sources"])
            
            # Rename columns for display
            sources_df = sources_df.rename(columns={
                "Source": "Source",
                "Count": "Mention Count",
                "Url": "URL"
            })
            
            st.markdown(make_table(sources_df), unsafe_allow_html=True)
    except:
        st.error(f"Top Sources KPI error")


    # Sentiment Analysis
    sentiment_data = kpi_output.get("Sentiment Analysis", {})
    try:
        if sentiment_data:

            styled_header("Sentiment Analysis", "💖")

            st.markdown(
                    "<span style='color:white'>Understand the overall tone of AI responses about your brand, highlighting positive, neutral, and negative sentiments.</span>",
                    unsafe_allow_html=True
                )

            # Convert data to DataFrame
            sentiment_df = pd.DataFrame([
                {"Sentiment": "Positive", "Percentage": float(str(sentiment_data["Positive"]["Percentage"]).rstrip("%"))},
                {"Sentiment": "Neutral", "Percentage": float(str(sentiment_data["Neutral"]["Percentage"]).rstrip("%"))},
                {"Sentiment": "Negative", "Percentage": float(str(sentiment_data["Negative"]["Percentage"]).rstrip("%"))},
            ])
            
            # Create two equal-height columns (for alignment)
            col1, col2 = st.columns([0.4, 0.6], vertical_alignment="center")

            # --- LEFT COLUMN: Sentiment Descriptions ---
            with col1:
                for sentiment, details in sentiment_data.items():
                    if sentiment.lower() == "positive":
                        icon = "🟢"
                    elif sentiment.lower() == "neutral":
                        icon = "⚪"
                    else:
                        icon = "🔴"
                    st.markdown(
                        f"<p style='font-size:16px; line-height:1.5; margin-bottom:15px; color:white'>"
                        f"<b>{icon} {sentiment}</b> — {details['Description']}</p>",
                        unsafe_allow_html=True
                    )

            # --- RIGHT COLUMN: Pie Chart ---
            with col2:
                shades = ["#FB4E0B", "#FD916F", "#FEB49A"]
                fig = px.pie(
                    sentiment_df,
                    names="Sentiment",
                    values="Percentage",
                    color="Sentiment",
                    color_discrete_sequence=shades,
                    hole=0.3
                )

                # Update layout for better alignment and visual balance
                fig.update_layout(
                    legend=dict(
                        orientation="v",
                        yanchor="middle",
                        y=0.5,
                        xanchor="left",
                        x=1.05
                    ),
                    margin=dict(l=20, r=150, t=20, b=20),
                    width=500,
                    height=300
                )

                st.plotly_chart(fig, use_container_width=True)

            # Close the border div
            st.markdown("</div>", unsafe_allow_html=True)
    except :
        st.error(f"Sentiment Analysis KPI error")

    # --- WORD ASSOCIATION MAP ---

    try:
        if "Word Association Map" in kpi_output:

            styled_header("Word Association Map", "☁️")

            st.markdown(
                    "<span style='color:white'>Identify the top 10 words or short phrases most frequently associated with your brand in the AI responses.</span>",
                    unsafe_allow_html=True
                )

            # Convert JSON list into a frequency dictionary
            word_list = kpi_output["Word Association Map"]
            word_freq = {item["Word"]: int(item["Count"]) for item in word_list}
            
            # Create Word Cloud
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color="white",
                colormap="autumn",  # Orange-red tones
                prefer_horizontal=0.9,
                max_words=100,
                contour_color="#FB4E0B",
                contour_width=1
            ).generate_from_frequencies(word_freq)

            # Plot the Word Cloud
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")

            # Save the plot to memory buffer
            buf = BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
            buf.seek(0)

            st.image(buf, use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)
    except :
        st.error(f"Word Association Map KPI error")
   
    try:
        if "Persona vs Competitor Matrix" in kpi_output:
            styled_header("Persona vs Competitor Matrix", "📊") 

            # Extract data
            persona_data = kpi_output["Persona vs Competitor Matrix"]

            # Flatten data
            records = []
            for persona in persona_data:
                persona_name = persona["Persona Role"]
                for competitor, count in persona["Competitor Mentions"].items():
                    records.append({
                        "Competitor": competitor,
                        "Persona": persona_name,
                        "Mentions": int(float(count))  # Ensure integers
                    })

            # Create DataFrame and pivot (Competitors as rows, Personas as columns)
            df = pd.DataFrame(records)
            pivot_df = df.pivot_table(
                index="Persona",
                columns="Competitor",
                values="Mentions",
                fill_value=0
            )
            
            # Create a 6–7 shade pastel green palette
            pastel_green_palette = sns.light_palette("#4CAF50", n_colors=7, reverse=False, as_cmap=True)

            # Style function with gradient
            styled_table = (
                pivot_df.style
                .background_gradient(cmap=pastel_green_palette, axis=None)  # Apply pastel green gradient
                .set_properties(**{
                    "text-align": "center",
                    "color": "black",
                    # "font-weight": "bold"
                })
                .format("{:.0f}")  # No decimals
                .set_table_styles([
                    {"selector": "th", "props": [("background-color", "#f0f0f0"), ("color", "#FB4E0B"), ("text-align", "center")]}
                ])
            )

            # Show table (no index)
            st.dataframe(styled_table.hide(axis="index"), use_container_width=True)

            st.markdown(
            "<span style='color:white'>This matrix highlights how often your brand and competitors are mentioned across different personas in AI responses. Darker shades of pastel green indicate higher mention counts.</span>",
            unsafe_allow_html=True
        )
    except :
        st.error(f"Persona vs Competitor Matrix KPI error")
   

    try:
        if "Topic vs Competitor Matrix" in kpi_output:
            styled_header("Topic vs Competitor Matrix", "🧩")

            # Extract data
            topic_data = kpi_output["Topic vs Competitor Matrix"]

            # Flatten data
            records = []
            for topic in topic_data:
                topic_name = topic["Topic"]
                for competitor, count in topic["Competitor Mentions"].items():
                    records.append({
                        "Topic": topic_name,
                        "Competitor": competitor,
                        "Mentions": int(float(count))  # Ensure integer
                    })

            # Create DataFrame and pivot (Competitors as columns)
            df = pd.DataFrame(records)
            pivot_df = df.pivot_table(
                index="Topic",
                columns="Competitor",
                values="Mentions",
                fill_value=0
            )
            
            # Create a smooth pastel green gradient (white → light → dark green)
            pastel_green_palette = sns.light_palette("#4CAF50", n_colors=7, reverse=False, as_cmap=True)

            # Style table with pastel gradient, no index, centered black text
            styled_table = (
                pivot_df.style
                .background_gradient(cmap=pastel_green_palette, axis=None)
                .set_properties(**{
                    "text-align": "center",
                    "color": "black",
                    # "font-weight": "bold"
                })
                .format("{:.0f}")  # Remove decimals
                .set_table_styles([
                    {"selector": "th", "props": [("background-color", "#f0f0f0"),
                                                ("color", "#FB4E0B"),
                                                ("text-align", "center"),
                                                ("font-weight", "bold")]}
                ])
            )
            # Display heatmap table without index column
            st.dataframe(styled_table.hide(axis="index"), use_container_width=True)

            st.markdown(
            "<span style='color:white'>This matrix highlights how often your brand and competitors are mentioned across different personas in AI responses. Darker shades of pastel green indicate higher mention counts.</span>",
            unsafe_allow_html=True
        )
    except :
        st.error(f"Persona vs Competitor Matrix KPI error")

def personaXtopic(data):
    if st.button("⬅ Back"):
        st.session_state.page = 6
        st.rerun()
        
    st.markdown(
    "<h2 style='color:#FFD700; font-weight:bold; text-align:center; margin-top:20px;'>📈 Strategic Content Opportunities</h2>",
    unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin-top: 20px; color: white; font-size: 16px; line-height: 1.5;'>
        Select a cell where your brand has low visibility to view recommendations and create content to rank higher.
    </div>
    """, unsafe_allow_html=True)


 # --- Convert to DataFrame ---
    try: 
        persona_rows = []
        for persona in data["personas"]:
            row = {"Persona": persona["name"]}
            row.update(persona["topics"])
            persona_rows.append(row)

        df = pd.DataFrame(persona_rows)
        topics = [col for col in df.columns if col != "Persona"]
    
    except Exception as e:
        st.error(f"Error: {e}")

    # --- Session State ---

    if "selected_cell" not in st.session_state:
        st.session_state.selected_cell = None

    # --- Visibility Matrix ---
    st.markdown(
            "### <span style='color:white'>Visibility Matrix (click a cell for recommendations).</span>",
            unsafe_allow_html=True
        )
    # Build Streamlit table layout dynamically

    cols = st.columns(len(topics) + 1)
    cols[0].markdown("**<span style='color:white'>Persona**</span>", unsafe_allow_html=True)
    for i, topic in enumerate(topics):
        cols[i + 1].markdown(f"<span style='color:white;'>{topic}</span>", unsafe_allow_html=True)

    for _, row in df.iterrows():
        cols = st.columns(len(topics) + 1)
        cols[0].markdown(f"<span style='color:white;'>{row['Persona']}</span>", unsafe_allow_html=True)

        for i, topic in enumerate(topics):
            val = row[topic]
            button_key = f"{row['Persona']}::{topic}"
            if cols[i + 1].button(f"{val:.0f}%", key=button_key, use_container_width=True):
                st.session_state.selected_cell = button_key
def Recommendations(Recommendation_output):
    section_style = "color:white; font-family:sans-serif; margin-bottom:15px;"
    header_style = "color:#FFD700; font-size:24px; font-weight:bold; margin-top:25px; margin-bottom:10px;"

    # FAQ Section
    st.markdown(f"<h2 style='{header_style}'>💡 FAQ</h2>", unsafe_allow_html=True)
    try:
        for item in Recommendation_output.get("FAQ", []):
            st.markdown(f"<p style='{section_style}'><b>Q:</b> {item['question']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='{section_style}'><b>A:</b> {item['answer']}</p>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to load FAQs: {e}")

    # Knowledge Article Section
    st.markdown(f"<h2 style='{header_style}'>📖 Knowledge Article</h2>", unsafe_allow_html=True)
    try:
        content = Recommendation_output.get("Knowledge Article", {}).get("content", "")
        st.markdown(f"<p style='{section_style}'>{content}</p>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to load Article Knowledge: {e}")

    # Social Posts Section
    st.markdown(f"<h2 style='{header_style}'>📱 Social Posts</h2>", unsafe_allow_html=True)
    try:
        for post in Recommendation_output.get("Social Posts", []):
            st.markdown(f"<p style='{section_style}'>- {post}</p>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to load Social Posts {e}")

    # How-To Guide Section
    st.markdown(f"<h2 style='{header_style}'>🛠 How-To Guide</h2>", unsafe_allow_html=True)
    try:
        for idx, step in enumerate(Recommendation_output.get("How-To Guide", []), start=1):
            st.markdown(f"<p style='{section_style}'><b>Step {idx}:</b> {step['step']}</p>", unsafe_allow_html=True)
            if step.get("tip"):
                st.markdown(f"<p style='{section_style}'>💡 Tip: {step['tip']}</p>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to load How-To Guide: {e}")

    # AI-Optimized Version Section
    st.markdown(f"<h2 style='{header_style}'>🤖 AI-Optimized Version</h2>", unsafe_allow_html=True)
    try: 
        content = Recommendation_output.get("AI-Optimized Version", {}).get("content", "")
        st.markdown(f"<p style='{section_style}'>{content}</p>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to load AI-Optimized Version: {e}")

    # Brand Voice Version Section
    st.markdown(f"<h2 style='{header_style}'>🎤 Brand Voice Version</h2>", unsafe_allow_html=True)
    try:
        content = Recommendation_output.get("Brand Voice Version", {}).get("content", "")
        st.markdown(f"<p style='{section_style}'>{content}</p>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to load Brand Voice Version: {e}")

# Use markdown + HTML for colored title - Added
st.set_page_config(page_title="EXL Brand Visibility", layout="wide")
st.markdown("""<style>.stApp{background:linear-gradient(135deg,#141E30, #243B55);}</style> """,unsafe_allow_html=True)

# Initialize OpenAI client
# client = OpenAI(api_key=st.secrets["api_keys"]["Openai_API_KEY"])
#openai.api_key = st.secrets["api_keys"]["Openai_API_KEY"]
# Function to run prompts and collect responses
# def run_prompts(prompts, model="gpt-4-turbo", temperature=0.7):
#     response = client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant that outputs only valid JSON."},
#             {"role": "user", "content": f"{prompts}\n\nRespond only in JSON format."}
#         ],
#         temperature=temperature
#     )
    
#     output = response['choices'][0]['message']['content'].strip()

#     try:
#         output=json.loads(output)
#         #st.write(output)
#         # Token usage data
#         token_data = {
#             "input_tokens": response.usage.prompt_tokens,
#             "output_tokens": response.usage.completion_tokens,
#             "total_tokens": response.usage.total_tokens
#         }

#         return output,token_data
#     except json.JSONDecodeError:
#         st.error(f"Model did not return valid JSON:\n{output}")
#         return None
# Function to run prompts and collect responses
def run_prompts(prompts, model="gpt-4-turbo", temperature=0.7):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that outputs only valid JSON."},
            {"role": "user", "content": f"{prompts}\n\nRespond only in JSON format."}
        ],
        temperature=temperature
    )

    output = response.choices[0].message.content.strip()

    try:
        output = json.loads(output)
        token_data = {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        return output, token_data
    except json.JSONDecodeError:
        st.error(f"Model did not return valid JSON:\n{output}")
        return None, None
# Session state
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'brand_title' not in st.session_state:
    st.session_state.brand_title = ""

# Router
if st.session_state.page == 1:
    page_search()

elif st.session_state.page ==2:
    verify_prompt = f"""
        Given the brand name {st.session_state.brand_title}, find the official website page for this brand.
        Return the result as a JSON object with two keys:
        - url: the full URL of the brand website home page
        - summary: a concise 20 lines summary of the brand based on the page content.
        Provide output strictly as valid JSON only with these keys exactly.
        """

    try:
        if Mode=='static':
            verify_output={ "url": "https://www.sky.com", "summary": "Sky UK is a leading British provider of television, broadband, mobile, and streaming services. Its offerings include Sky TV platforms such as Sky Glass, Sky Stream, and Sky Q, along with premium content from Sky Sports, Sky Cinema, and Sky Originals. The company also delivers high-speed fibre broadband, Wi-Fi solutions, and flexible mobile plans through Sky Mobile. Sky is part of the wider Sky Group, owned by Comcast, and operates with a mission to deliver better entertainment, connectivity, and customer experiences. It also manages news, sports, and entertainment brands that play a major role across the UK media landscape while continuing to focus on innovation, sustainability, and high-quality content creation." }
            data_verify = {
            "input_tokens": 40,
            "output_tokens": 300,
            "total_tokens": 340
            }
        else:
            verify_output,data_verify = run_prompts(verify_prompt)    

        st.session_state.url = verify_output["url"]

        # Initialize session state if not already set
        if "url" not in st.session_state:
            st.session_state.url = verify_output["url"]
        if "summary" not in st.session_state:
            st.session_state.summary = verify_output["summary"]
        if "brand_title" not in st.session_state:
            st.session_state.brand_title = ""
    except Exception as e:
        st.error(f"Failed to fetch Brand Details: {e}")
    try:
        summary(verify_output)   

        c1, c2, c3 = st.columns(3)

        c1.metric("Input Tokens", f"{data_verify['input_tokens']:,}")
        c2.metric("Output Tokens", f"{data_verify['output_tokens']:,}")
        c3.metric("Total Tokens", f"{data_verify['total_tokens']:,}")

        st.markdown("""
            <style>
            [data-testid="stMetricLabel"] {
                color: white !important;
                font-size: 15px !important;  /* adjust size as needed */
            }
            [data-testid="stMetricValue"] {
                color: white !important;
                font-size: 15px !important;  /* adjust size as needed */
            }
            </style>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to retrieve Summary: {e}")

        # Stop here if button not clicked
    if not st.session_state.brand_confirm_clicked:
        st.warning('please confirm the brand')
    else:
        with st.spinner("Generating Website scores..."):
            
            Score_prompt = f"""
                Please analyze the following URL: {st.session_state.url} and provide a detailed assessment in the areas below.
                For each area, provide:
                - Score (0-100 in percentage)
                - Rating (Good, Very Good, Excellent, Needs Improvement) based on the score
                - Highlights (2-3 key observations)
                - Recommendations (3-4 actionable suggestions)
    
                The areas to assess are:
                1. AI Optimization: overall AI and SEO readiness, performance, and optimization opportunities.
                2. Structured Data Quality: correctness, completeness, and usefulness of structured data/markup.
                3. Page Layout & Structure: usability, hierarchy, and visual layout effectiveness.
                4. Schema Markup: presence, accuracy, and relevance of schema.org markup.
                5. Navigation: clarity, accessibility, and ease of finding content.
                6. Content Balance: ratio and relevance of text, images, media, and overall content distribution.
                7. Metadata: quality and completeness of title tags, meta descriptions, and other metadata.
    
                OUTPUT FORMAT:
                Return only a valid JSON with this exact structure:
    
                {{"AI Optimization":
                    {{ "Score": 90,
                    "Rating": "Excellent",
                    "Highlights": [ "", "" ]
                    }}
                }},...
    
                OUTPUT RULES:
                - Output strictly valid JSON (no markdown, no extra commentary)
                - Use double quotes for all keys and values
                - No nested objects or extra keys
                - Must be directly parsable by json.loads()
                """
        if Mode=='static':
            Score_output={ "AI Optimization": { "Score": 90, "Rating": "Excellent", "Highlights": [ "The website is well-optimized for search engines and it has high visibility on various search engines", "The website load time is quite fast, indicating good performance optimization" ], "Recommendations": [ "Improve the website's AI by integrating chatbots for better user interaction", "Consider implementing predictive search to enhance user experience", "Regularly monitor and update SEO strategies for better optimization" ] }, "Structured Data Quality": { "Score": 85, "Rating": "Very Good", "Highlights": [ "The data on the website is well structured and easy to understand", "The use of tables, headings, and lists is effective in presenting information" ], "Recommendations": [ "Check and correct any data inconsistencies", "Ensure all data is updated regularly", "Consider adding more internal and external links to enhance the data structure" ] }, "Page Layout & Structure": { "Score": 95, "Rating": "Excellent", "Highlights": [ "The website has a clean and intuitive design", "The visual hierarchy is effective, guiding the user's eye to important elements" ], "Recommendations": [ "Ensure the website is fully responsive on all devices", "Consider A/B testing for different layouts to see what works best", "Regularly update the design to keep it fresh and engaging" ] }, "Schema Markup": { "Score": 90, "Rating": "Excellent", "Highlights": [ "The website uses schema.org markup effectively to enhance its SEO", "The markup is accurate and relevant" ], "Recommendations": [ "Regularly review and update the schema markup", "Ensure all pages have relevant and accurate schema markup", "Use more specific schema types to provide more detailed information to search engines" ] }, "Navigation": { "Score": 85, "Rating": "Very Good", "Highlights": [ "The website has a clear and easy-to-use navigation system", "Content is easy to find with minimal clicks" ], "Recommendations": [ "Consider implementing a search function for easier navigation", "Ensure all links are working and lead to the correct pages", "Regularly review and update the navigation system to ensure it remains user-friendly" ] }, "Content Balance": { "Score": 80, "Rating": "Very Good", "Highlights": [ "The website has a good balance of text, images, and media", "The content is relevant and engaging" ], "Recommendations": [ "Ensure all images and media are optimized for faster loading", "Consider adding more interactive elements to engage users", "Regularly update content to keep it fresh and relevant" ] }, "Metadata": { "Score": 85, "Rating": "Very Good", "Highlights": [ "The website's title tags and meta descriptions are complete and informative", "Other metadata such as alt tags for images are also used effectively" ], "Recommendations": [ "Regularly review and update metadata to ensure it's accurate", "Ensure all images have alt tags for better SEO", "Consider using more specific keywords in the meta descriptions for better visibility on search engines" ] } }
            data = {
            "input_tokens": 500,
            "output_tokens": 50,
            "total_tokens": 550
            }
        else:
            Score_output,data = run_prompts(Score_prompt)

        try:
            website_analysis(Score_output)   

            c1, c2, c3 = st.columns(3)

            c1.metric("Input Tokens", f"{data['input_tokens']:,}")
            c2.metric("Output Tokens", f"{data['output_tokens']:,}")
            c3.metric("Total Tokens", f"{data['total_tokens']:,}")

            st.markdown("""
                <style>
                [data-testid="stMetricLabel"] {
                    color: white !important;
                    font-size: 15px !important;  /* adjust size as needed */
                }
                [data-testid="stMetricValue"] {
                    color: white !important;
                    font-size: 15px !important;  /* adjust size as needed */
                }
                </style>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Failed to retrieve Scores: {e}")

elif st.session_state.page == 3:
    
    brand_offerings_prompt = f"""
        You are an expert AI visibility analyst specializing in AI Engine Optimization (AEO).

        Task:
        Identify the specific products and services offered by the given brand, based only on the provided data.

        Brand Information:
        - Brand name: {st.session_state.brand_title}
        - Official website: {st.session_state.url}
        - Brand summary: {st.session_state.summary}

        Output Instructions:
        1. Return output strictly as valid JSON:
        ["Product or Service 1", "Product or Service 2", ...]
        
        2. Include only concrete, named offerings (e.g., "Microsoft 365", "LinkedIn", "Azure").
        3. Do NOT include:
        - Generic terms like “cloud solutions” or “consulting services”
        - Marketing or descriptive phrases
        - Duplicate or overlapping items
        4. If offerings cannot be confidently identified from the provided data, return:
            []

        Example:
        Input summary: "Microsoft develops software such as Windows, Office 365, and Azure cloud platform."
        Output:
        ["Windows", "Office 365", "Azure"]

        Return only valid JSON with no extra text or commentary.
        """
    if "BrandOfferings" not in st.session_state:
        if Mode=='static':
            brand_offerings_output=[ "Sky Glass", "Sky Stream", "Sky Q", "Sky Sports", "Sky Cinema", "Sky Originals", "Sky Mobile" ]
            data = {
            "input_tokens": 1000,
            "output_tokens": 500,
            "total_tokens": 1500
        }
        else:
            brand_offerings_output,data = run_prompts(brand_offerings_prompt)
        st.session_state.BrandOfferings=brand_offerings_output
    try:
        page_focus()
        try:
            c1, c2, c3 = st.columns(3)

            c1.metric("Input Tokens", f"{data['input_tokens']:,}")
            c2.metric("Output Tokens", f"{data['output_tokens']:,}")
            c3.metric("Total Tokens", f"{data['total_tokens']:,}")

            st.markdown("""
                <style>
                [data-testid="stMetricLabel"] {
                    color: white !important;
                    font-size: 15px !important;  /* adjust size as needed */
                }
                [data-testid="stMetricValue"] {
                    color: white !important;
                    font-size: 15px !important;  /* adjust size as needed */
                }
                </style>
                """, unsafe_allow_html=True)
        except:
            pass
    except Exception as e:
        st.error(f"Failed to retrieve Brand Products: {e}")

elif st.session_state.page == 4:
    with st.spinner("Generating personas..."):
        Personas = f"""
        You are an AI assistant helping to analyze market audiences and user perceptions for a given brand and product.

        INPUT:
        - Brand Name: {st.session_state.brand_title}
        - Brand Product: {st.session_state.selectedProduct}

        TASK:
        Generate 3 realistic and diverse user personas who represent actual or potential users of this {st.session_state.brand_title}'s product or service — without explicitly naming or referencing the brand in their descriptions.

        GUIDELINES:
        - Each persona should represent a distinct type of consumer or user (not just a demographic or job title).
        - Each persona must highlight different motivations, goals, and frustrations related to {st.session_state.selectedProduct}.
        - Keep the tone objective and descriptive. Do NOT mention or describe the brand directly (e.g., do not say “They like Nike’s X initiative” or similar).
        - Focus on the user’s needs, mindset, and behaviors within the product category, not the brand itself.

        For each persona, include:
        1. "Name": A short, creative label (e.g., "Performance-Focused Athlete", "Style-Driven Urban Explorer", "Comfort-Seeking Commuter").
        2. "Avatar": A single emoji or icon representing this persona’s mindset or lifestyle.
        3. "Description": A 2-3 sentence summary covering:
        - Their age range, lifestyle, and motivation
        - How they use or might use products like {st.session_state.selectedProduct}
        - Their goals, expectations, and frustrations within this product category
        4. "Characteristics": A list (4-5 bullet points) describing their traits, habits, shopping behavior, decision-making style, and what they value most in such products.

        OUTPUT FORMAT:
        Return only a valid JSON array of personas with this exact structure:

        [
        {{
            "Name": "",
            "Avatar": "",
            "Description": "",
            "Characteristics": ["", "", ""]
        }},
        ...
        ]

        OUTPUT RULES:
        - Output strictly valid JSON (no markdown, no extra commentary)
        - Use double quotes for all keys and values
        - Each list item must be a plain string
        - No nested objects or extra keys
        - Must be directly parsable by json.loads()

        """
        if "personas" not in st.session_state:
            if Mode=='static':
                Personas_output= [ { "Name": "Connected Home Streamer",
"Avatar": "📺",
"Description": "A tech-comfortable adult in their 30s–40s who enjoys creating a seamless entertainment setup at home. They want reliable access to a wide range of shows, films, and live events. Their biggest frustration is dealing with interruptions, device incompatibility, or limited viewing options.",
"Characteristics": [
"Prefers integrated home entertainment ecosystems",
"Values high-quality streaming and intuitive interfaces",
"Often bundles multiple digital services",
"Makes decisions based on convenience and performance",
"Researches features before committing to long-term plans"
]
},
{
"Name": "On-the-Go Multitasker",
"Avatar": "📱",
"Description": "A busy professional in their late 20s–30s who frequently relies on mobile connectivity for work, entertainment, and communication. They expect consistent performance whether at home, commuting, or traveling. They become frustrated with slow data speeds or services that don’t align with their flexible lifestyle.",
"Characteristics": [
"Constant user of mobile data and hotspot features",
"Prioritizes reliability and coverage over price",
"Looks for flexible contracts and rolling plans",
"Adopts new tech quickly if it solves daily pain points",
"Prefers seamless switching between devices"
]
},
{
"Name": "Family-Centric Planner",
"Avatar": "🏡",
"Description": "A parent in their 40s–50s who manages household entertainment and internet needs. They seek dependable services that keep kids entertained, support remote work or school, and avoid household disruptions. They dislike complicated setups, surprise fees, or anything that causes family downtime.",
"Characteristics": [
"Focuses on value-for-money bundles",
"Prefers simple installation and easy parental controls",
"Balances entertainment needs across different age groups",
"Compares options extensively before switching providers",
"Highly motivated by dependability and customer support"
] },
{
"Name": "Budget-Savvy Entertainment Seeker",
"Avatar": "💷",
"Description": "A young adult in their mid-20s who enjoys watching films, sports, and series but must balance entertainment with financial constraints. They look for affordable options that still provide variety and decent performance. They grow frustrated when pricing feels confusing or when key features are locked behind expensive upgrades.",
"Characteristics": [
"Compares multiple providers before choosing",
"Prefers flexible monthly costs over long contracts",
"Wants strong value without sacrificing content variety",
"Frequently streams on multiple devices",
"Sensitive to unexpected fees or price increases"
]
} ]        
                Personas_data = {
                "input_tokens": 2000,
                "output_tokens": 1000,
                "total_tokens": 3000
            }
            else:
                Personas_output,Personas_data = run_prompts(Personas)

            st.session_state.personas = Personas_output
            
    with st.spinner("Generating brand-related topics..."):

        Topics = f"""
        You are an AI assistant that analyzes audience interests and identifies relevant discussion themes.

            INPUT:              
            - Brand Name: {st.session_state.brand_title}
            - Product or Service: {st.session_state.selectedProduct}
            - Personas: {st.session_state.personas}  

            TASK:
            Analyze the provided {st.session_state.personas} and identify their shared areas of curiosity, motivation, and decision-making related to the **product category** that {st.session_state.selectedProduct} belongs to.

            Then, based on these overlaps, generate **5 broad and search-friendly topics** that:
            - Represent themes relevant to **all {st.session_state.personas} collectively**.
            - Are applicable to the general product category, not tied to any single brand.
            - Are phrased as short, natural keyword phrases or questions (max 10 words each).
            - Reflect a balance between **SEO-friendly topics** and **authentic consumer intent**.
            - Focus on real-world considerations like usability, value, performance, sustainability, comparison, and lifestyle fit.

            OUTPUT FORMAT:
            [
            "Topic 1",
            "Topic 2",
            "Topic 3",
            "Topic 4",
            "Topic 5"
            ]

            OUTPUT RULES:
            - Do NOT mention or describe the brand directly.
            - Topics must appeal to all personas collectively.
            - Avoid specific product names or model references.
            - Keep phrasing conversational, natural, and search-oriented.
            - Do NOT include commentary, markdown, or explanations.
            - Return only valid JSON.
            - Each list item must be a plain string.
            - Must be directly parsable with json.loads().

        """
   
    if "topics" not in st.session_state:
        if Mode=='static':
            Topics_output=["Home entertainment services overview", "Internet speed and reliability features", "Comparing streaming and broadband providers", "Device compatibility with modern entertainment services", "Cost-effectiveness of bundled digital services", "User-friendly features in home entertainment platforms", "Performance and stability of streaming services", "Reliability of broadband for remote work and gaming", "Managing family usage across digital services", "Customer support quality for internet and streaming services"]
            data = {
            "input_tokens": 1000,
            "output_tokens": 400,
            "total_tokens": 1400
        }
        else:
            Topics_output,data= run_prompts(Topics)

        st.session_state.topics = Topics_output
    try:
        page_persona()
    except Exception as e:
        st.error(f"Failed to retrieve Personas with Topics: {e}")
    try:
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Input Tokens", f"{Personas_data['input_tokens']:,}")
        c2.metric("Output Tokens", f"{Personas_data['output_tokens']:,}")
        c3.metric("Total Tokens", f"{Personas_data['total_tokens']:,}")
        st.markdown("<span style='color:white'>Persona tokens</span>", unsafe_allow_html=True)
        st.markdown("""
        <style>
        [data-testid="stMetricLabel"] {
            color: white !important;
            font-size: 15px !important;  /* adjust size as needed */
        }
        [data-testid="stMetricValue"] {
            color: white !important;
            font-size: 15px !important;  /* adjust size as needed */
        }
        </style>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Input Tokens", f"{data['input_tokens']:,}")
        c2.metric("Output Tokens", f"{data['output_tokens']:,}")
        c3.metric("Total Tokens", f"{data['total_tokens']:,}")
        st.markdown("<span style='color:white'>Topic tokens</span>", unsafe_allow_html=True)
        st.markdown("""
            <style>
            [data-testid="stMetricLabel"] {
                color: white !important;
                font-size: 15px !important;  /* adjust size as needed */
            }
            [data-testid="stMetricValue"] {
                color: white !important;
                font-size: 15px !important;  /* adjust size as needed */
            }
            </style>
            """, unsafe_allow_html=True)
    except :
        pass

elif st.session_state.page == 5:

    with st.spinner("Prompts by persona..."):
        Prompts_Persona = f"""
            You are an AI assistant that generates realistic, comparison-focused consumer prompts and responses for any type of product or brand category.
 
            Input:
            - Personas: {st.session_state.personas}
            - Topics: {st.session_state.topics}
            - Brand Name: {st.session_state.brand_title}
            - Brand Product: {st.session_state.selectedProduct}
 
            TASK:
                For each persona, analyze their motivations, needs, and goals from {st.session_state.personas}, and combine them with relevant topics from {st.session_state.topics} to create thoughtful product comparison prompts and responses.
 
                1. Generate **3–4 realistic, search-style prompts per persona**:
                    - Each prompt must clearly relate to **one or more topics** from the provided list.
                    - Combine the persona’s intent, tone, and needs with relevant topics.
                    - Prompts should sound natural — like real user search queries when comparing or choosing between products in the {st.session_state.selectedProduct} category.
                    - Do NOT include brand names in the question itself.
                    - Prompts should be practical, decision-oriented, and concise (e.g., “Which running shoes are best for daily training?”).
 
                2. For each prompt, write a **2-sentence response** that:
                    - Objectively compares well-known brands or product types within the {st.session_state.selectedProduct} category.
                    - Always include **at least two relevant brands or competitors** in each response (e.g., “Nike, Adidas, and Asics” for shoes; “Apple, Samsung, and Google” for smartphones).
                    - Mention {st.session_state.brand_title} **only if it is a recognized or relevant brand** in that category.
                    - Responses must remain consistent and neutral, regardless of what value {st.session_state.brand_title} takes — changing the brand name should not alter the structure, meaning, or balance of the response.
                    - The comparison does not have to center on {st.session_state.brand_title}; include it only when naturally fitting within the brand list.
                    - Keep tone factual, consumer-friendly, and unbiased (no marketing or promotional language).
                    - Highlight key differentiators briefly (e.g., “offers longer battery life” or “has better cushioning”).
 
                3. Tagging Requirement:
                    - Each prompt must include a "Relevant Topics" field listing one or more exact topics from {st.session_state.topics}.
                    - Example: "Relevant Topics": ["durability", "comfort"]
 
            Output format:
            [
            {{
                "Persona Role": "<Role Name>",
                "Prompts": [
                {{ "Prompt": "<Question 1>", "Response": "<Response 1>", "Relevant Topics": ["", "", ""] }},
                {{ "Prompt": "<Question 2>", "Response": "<Response 2>", "Relevant Topics": ["", "", ""] }},
                {{ "Prompt": "<Question 3>", "Response": "<Response 3>", "Relevant Topics": ["", "", ""] }},
                {{ "Prompt": "<Question 4>", "Response": "<Response 4>", "Relevant Topics": ["", "", ""] }}
                ]
            }},
            ...
            ]
 
            OUTPUT RULES:
            - Output must be valid JSON only (no markdown or extra text)
            - Use double quotes for all keys and values
            - Lists must contain only strings
            - Must be parsable directly with json.loads()
            """
     
    if "brandprompts" not in st.session_state:
        if Mode=='static':
            #brandprompts = [ { "Persona Role": "Tech-Savvy Developer", "Prompts": [ { "Prompt": "How does the software compatibility of Windows OS compare with other operating systems?", "Response": "Windows OS is renowned for its extensive software compatibility, supporting a wider range of software compared to Linux or macOS. However, Linux offers better compatibility for open-source and developer-specific software.", "Relevant Topics": ["Windows OS compatibility with various software", "Comparing Windows OS with other operating systems"] }, { "Prompt": "What are the latest updates and features in Windows OS that can benefit developers?", "Response": "The latest updates in Windows OS include features like Windows Subsystem for Linux (WSL) and improved PowerShell that provide developers with more robust development environments. However, their utility might vary based on your specific development requirements.", "Relevant Topics": ["Latest updates and features in Windows OS"] }, { "Prompt": "How does Windows OS security features stack up against Linux for development purposes?", "Response": "While Windows OS has made significant improvements in security features, Linux generally has a stronger reputation in this area due to its open-source nature and active community. This makes Linux a go-to choice for developers who prioritize security.", "Relevant Topics": ["Windows OS security features", "Comparing Windows OS with other operating systems"] }, { "Prompt": "How does the performance and stability of Windows OS compare with Linux for high workloads?", "Response": "Windows OS is generally user-friendly and capable of handling high workloads, but it can occasionally suffer from stability issues. On the other hand, Linux is known for its stability and efficient resource management, especially under high workloads.", "Relevant Topics": ["Performance and stability of Windows OS", "Comparing Windows OS with other operating systems"] }, { "Prompt": "How user-friendly is Windows OS for someone comfortable with advanced tech topics?", "Response": "Windows OS offers a user-friendly interface, but it also provides advanced features and extensive customization options for those comfortable with advanced tech topics. However, some tech-savvy users prefer the command-line interface and flexibility offered by Linux.", "Relevant Topics": ["How user-friendly is Windows OS?"] } ] }, { "Persona Role": "Budget-Conscious Student", "Prompts": [ { "Prompt": "How cost-effective are Windows OS upgrades for students?", "Response": "Windows OS upgrades are generally cost-effective, often including features that improve functionality and security. However, the cost-effectiveness might be influenced by the specific needs of a student and the type of academic software they use.", "Relevant Topics": ["Cost-effectiveness of Windows OS upgrades"] }, { "Prompt": "How user-friendly is Windows OS for academic purposes?", "Response": "Windows OS is known for its user-friendly interface and versatility, making it a popular choice for academic purposes. However, the ease of use might vary based on the specific academic software in use.", "Relevant Topics": ["How user-friendly is Windows OS?"] }, { "Prompt": "What's the reliability of Windows OS for running academic software?", "Response": "Windows OS is generally reliable for running academic software due to its wide compatibility. However, some niche academic software may run more smoothly on other operating systems like Linux or macOS.", "Relevant Topics": ["Windows OS compatibility with various software", "Reliability and efficiency of Windows OS for multitasking"] }, { "Prompt": "What are the latest updates in Windows OS that can benefit students?", "Response": "Latest updates in Windows OS often include improved features and security updates that can benefit students. However, their usefulness may vary depending on the specific academic needs of the student.", "Relevant Topics": ["Latest updates and features in Windows OS"] }, { "Prompt": "How does Windows OS compare with other operating systems in terms of price and reliability for students?", "Response": "Windows OS is generally affordable and reliable, making it a popular choice amongst students. However, Linux, being free and known for its reliability, could be a strong alternative for budget-conscious students.", "Relevant Topics": ["Comparing Windows OS with other operating systems"] } ] }, { "Persona Role": "Corporate Professional", "Prompts": [ { "Prompt": "How secure is Windows OS for professional work?", "Response": "Windows OS has robust security features including Windows Defender, BitLocker, and a built-in firewall, making it a secure choice for professional work. However, regular updates are required to keep the system secure.", "Relevant Topics": ["Windows OS security features"] }, { "Prompt": "How efficient is Windows OS for multitasking in a corporate environment?", "Response": "Windows OS is designed for multitasking and handles multiple applications running simultaneously well. However, system performance can be influenced by the hardware specs of the device.", "Relevant Topics": ["Reliability and efficiency of Windows OS for multitasking"] }, { "Prompt": "How does the compatibility of Windows OS with business software compare with other operating systems?", "Response": "Windows OS is highly compatible with a wide range of business software, more so than other operating systems like Linux or macOS. However, certain industry-specific software might run better on other operating systems.", "Relevant Topics": ["Windows OS compatibility with various software", "Comparing Windows OS with other operating systems"] }, { "Prompt": "How frequent are system updates in Windows OS and how do they impact work efficiency?", "Response": "Windows OS updates are frequent and are designed to improve system functionality and security. However, these updates can sometimes cause temporary disruptions, impacting work efficiency.", "Relevant Topics": ["Latest updates and features in Windows OS"] }, { "Prompt": "How good is the customer support for Windows OS?", "Response": "Windows OS has extensive customer support, including online forums, tutorials, and direct support channels. However, the quality of support can sometimes vary based on the complexity of the issue.", "Relevant Topics": ["Customer support quality for Windows OS"] } ] }, { "Persona Role": "Casual User", "Prompts": [ { "Prompt": "How user-friendly is Windows OS for casual activities like browsing and gaming?", "Response": "Windows OS is known for its user-friendly interface and wide range of applications, making it suitable for casual activities like browsing and gaming. However, the performance can vary based on the system's hardware.", "Relevant Topics": ["How user-friendly is Windows OS?"] }, { "Prompt": "How stable is Windows OS for running games and multimedia applications?", "Response": "Windows OS generally provides a stable platform for running games and multimedia applications. However, users might experience occasional slowdowns during heavy gaming or multitasking.", "Relevant Topics": ["Performance and stability of Windows OS"] }, { "Prompt": "What are the latest updates in Windows OS that can enhance my casual usage?", "Response": "Latest updates in Windows OS often include improved features, security updates, and performance enhancements that can enhance casual usage. However, the impact of these updates on user experience can vary.", "Relevant Topics": ["Latest updates and features in Windows OS"] }, { "Prompt": "How does the cost-effectiveness of Windows OS upgrades compare for casual users?", "Response": "Windows OS upgrades are generally cost-effective and include features that improve functionality and security. However, casual users might not require all the advanced features provided in the upgrades.", "Relevant Topics": ["Cost-effectiveness of Windows OS upgrades"] }, { "Prompt": "How good is the customer support for Windows OS for resolving common issues?", "Response": "Windows OS provides extensive customer support, including online resources and direct support channels. However, the effectiveness of resolving common issues can vary based on the nature of the problem.", "Relevant Topics": ["Customer support quality for Windows OS"] } ] } ]
            brandprompts = [
                                {
                                "Persona Role": "Connected Home Streamer",
                                "Prompts": [
                                {
                                "Prompt": "Which home entertainment services offer the most stable streaming quality?",
                                "Response": "Platforms like Netflix and Amazon Prime Video are often praised for consistent streaming, while some users find Disney+ slightly more variable depending on device load. Broadband providers such as BT and Virgin Media typically influence overall stability, offering different performance levels depending on the area.",
                                "Relevant Topics": ["Performance and stability of streaming services", "Internet speed and reliability features"]
                                },
                                {
                                "Prompt": "How do different entertainment providers compare in device compatibility?",
                                "Response": "Services like Netflix and Amazon Prime Video support nearly all major smart TVs and streaming devices, while Apple TV+ may be more limited on certain older models. Broadband providers such as BT and Virgin Media also differ in router compatibility with home setups.",
                                "Relevant Topics": ["Device compatibility with modern entertainment services", "Home entertainment services overview"]
                                },
                                {
                                "Prompt": "Which entertainment bundles offer the best value for heavy streamers?",
                                "Response": "Many users compare bundles from Virgin Media and BT, which combine broadband with TV channels, while streaming-only options like Netflix or Disney+ may be cheaper but less comprehensive. Hybrid solutions provide more content variety but can cost significantly more.",
                                "Relevant Topics": ["Cost-effectiveness of bundled digital services", "Comparing streaming and broadband providers"]
                                },
                                {
                                "Prompt": "What affects the reliability of streaming during peak hours?",
                                "Response": "Virgin Media and BT often differ in peak-time speeds, with variations tied to local infrastructure. Streaming services like Netflix and Disney+ adjust video quality dynamically, which influences user experience during high congestion.",
                                "Relevant Topics": ["What affects streaming quality and device performance", "Internet speed and reliability features"]
                                }
                                ]
                                },
                                {
                                "Persona Role": "On-the-Go Multitasker",
                                "Prompts": [
                                {
                                "Prompt": "Which mobile-friendly entertainment platforms perform best on slower connections?",
                                "Response": "Netflix and YouTube typically adapt well to slower speeds with efficient compression, while Disney+ may require slightly higher bandwidth for stable performance. Mobile carriers like Vodafone and EE also impact performance through network coverage.",
                                "Relevant Topics": ["Performance and stability of streaming services", "Reliability of broadband for remote work and gaming"]
                                },
                                {
                                "Prompt": "How do different providers compare in flexibility for month-to-month plans?",
                                "Response": "Streaming services such as Netflix and Amazon Prime Video offer easy month-to-month cancellation, while broadband services like BT or Virgin Media often require longer contracts. Users choosing mobile-based entertainment may prefer providers with minimal commitment requirements.",
                                "Relevant Topics": ["Cost-effectiveness of bundled digital services", "Home entertainment services overview"]
                                },
                                {
                                "Prompt": "Which broadband options are best for people who frequently work while traveling?",
                                "Response": "EE and Vodafone often provide strong portable hotspot performance, while fixed broadband providers like Virgin Media or BT may offer bundled add-ons for remote access. Reliability can vary significantly based on location and peak network usage.",
                                "Relevant Topics": ["Internet speed and reliability features", "Reliability of broadband for remote work and gaming"]
                                }
                                ]
                                },
                                {
                                "Persona Role": "Family-Centric Planner",
                                "Prompts": [
                                {
                                "Prompt": "Which entertainment services offer the best parental control options?",
                                "Response": "Netflix and Disney+ include robust parental controls with profile restrictions, while Amazon Prime Video offers a simpler but effective PIN-based system. Traditional TV providers like BT and Virgin Media differ in how customizable their parental controls are.",
                                "Relevant Topics": ["Managing family usage across digital services", "User-friendly features in home entertainment platforms"]
                                },
                                {
                                "Prompt": "How do different broadband providers compare for households with multiple users?",
                                "Response": "Virgin Media often provides higher maximum speeds for large households, while BT focuses on stable performance across many devices. Families choosing streaming platforms like Netflix or Disney+ may find higher speeds helpful for simultaneous viewing.",
                                "Relevant Topics": ["Internet speed and reliability features", "Performance and stability of streaming services"]
                                },
                                {
                                "Prompt": "Which service bundles are most cost-effective for large families?",
                                "Response": "Bundles from BT and Virgin Media usually combine broadband with TV channels for better overall value, while standalone streaming services such as Netflix or Amazon Prime Video may be cheaper but less comprehensive. The best choice depends on how much content variety the family needs.",
                                "Relevant Topics": ["Cost-effectiveness of bundled digital services", "Comparing streaming and broadband providers"]
                                },
                                {
                                "Prompt": "Which platforms are easiest for kids and adults to use together?",
                                "Response": "Disney+ and Netflix are known for clear navigation and profile separation, while Amazon Prime Video can feel more complex for younger users. TV-based services from providers like BT and Virgin Media vary in menu simplicity and remote control layout.",
                                "Relevant Topics": ["User-friendly features in home entertainment platforms", "Device compatibility with modern entertainment services"]
                                }
                                ]
                                },
                                {
                                "Persona Role": "Budget-Savvy Entertainment Seeker",
                                "Prompts": [
                                {
                                "Prompt": "Which entertainment options give the best value for a tight budget?",
                                "Response": "Netflix’s basic tier and Disney+ are often considered affordable choices, while Amazon Prime Video includes additional perks that may improve overall value. Broadband providers such as Vodafone and Plusnet offer budget-friendly plans that support standard streaming.",
                                "Relevant Topics": ["Cost-effectiveness of bundled digital services", "Home entertainment services overview"]
                                },
                                {
                                "Prompt": "How do low-cost broadband providers compare for streaming quality?",
                                "Response": "Plusnet and Vodafone usually deliver reliable speeds for standard streaming, though peak times may vary by area. This contrasts with typically faster but more expensive providers like Virgin Media or BT.",
                                "Relevant Topics": ["Internet speed and reliability features", "Performance and stability of streaming services"]
                                },
                                {
                                "Prompt": "Which services offer the most content variety for the price?",
                                "Response": "Amazon Prime Video includes a broad catalog plus additional membership benefits, while Netflix provides strong originals and consistent updates. Disney+ tends to be more specialized but offers strong value for families.",
                                "Relevant Topics": ["Home entertainment services overview", "Comparing streaming and broadband providers"]
                                },
                                {
                                "Prompt": "Are bundled TV and internet packages cheaper than standalone streaming apps?",
                                "Response": "Bundles from providers like BT and Virgin Media may save money for users needing faster broadband and live channels. However, standalone services such as Netflix and Disney+ often cost less overall for viewers who only want on-demand content.",
                                "Relevant Topics": ["Cost-effectiveness of bundled digital services", "Comparing streaming and broadband providers"]
                                }
                                ]
                                }
                            ]
            data = {
                "input_tokens": 5000,
                "output_tokens": 42,
                "total_tokens": 5042
            }
        else: 
            brandprompts,data= run_prompts(Prompts_Persona)
        st.session_state.brandprompts=brandprompts
    # st.write(st.session_state.brandprompts)
    try:
        page_prompt()
    except Exception as e:
        st.error(f"Failed to retrieve Prompts by Persona: {e}")
    try:
        c1, c2, c3 = st.columns(3)

        c1.metric("Input Tokens", f"{data['input_tokens']:,}")
        c2.metric("Output Tokens", f"{data['output_tokens']:,}")
        c3.metric("Total Tokens", f"{data['total_tokens']:,}")

        st.markdown("""
            <style>
            [data-testid="stMetricLabel"] {
                color: white !important;
                font-size: 15px !important;  /* adjust size as needed */
            }
            [data-testid="stMetricValue"] {
                color: white !important;
                font-size: 15px !important;  /* adjust size as needed */
            }
            </style>
            """, unsafe_allow_html=True)
        
    except: pass

elif st.session_state.page == 6:

    with st.spinner("Running Prompt 4: Generating KPI insights..."):
        # ---------------------------
        # PROMPT 4: KPI Analysis
        # ---------------------------
        KPIs= f"""
        You are an AI assistant. 

        Input: 
        A list of responses to multiple prompts, generated by different personas regarding a product category
        Brand Name: {st.session_state.brand_title}  
        Brand Product: {st.session_state.selectedProduct}  
        Personas: {st.session_state.personas}  
        Topics:  {st.session_state.topics}
        Responses: {st.session_state.brandprompts}

        1. Brand Visbility: Task: Calculate the **Brand Visibility** of {st.session_state.brand_title} compared to its competitors based on the given {st.session_state.brandprompts}.

            Instructions:
            1. Review all {st.session_state.brandprompts} and identify:
            - Mentions of the {st.session_state.brand_title}.
            - Mentions of any competitor brands.
            2. Count the total number of times {st.session_state.brand_title} is mentioned → `Count of {st.session_state.brand_title}`.
            3. Count the total mentions of all competitor brands combined → `Count of Brand's Competitors`.
            4. Calculate Brand Visibility % using the formula:
            Brand Visibility % = (Count of {st.session_state.brand_title} / (Count of {st.session_state.brand_title} + Count of Competitors)) × 100
            5. Round the percentage to one decimal place.
            6. Ensure the counts and percentages are consistent with the identified mentions.

            Output Format (JSON):
            {{
                "Brand Visibility": {{
                    "Count of {st.session_state.brand_title}": "number",
                    "Count of Brand's Competitors": "number",
                    "Brand Visibility %": "x.x"
                }}
            }}

            

        2. Leaderboard:
            From the responses given show:
            - Identify all distinct brand names mentioned across the {st.session_state.brandprompts}.
            - Count how many times each brand name appears (case-insensitive, include duplicates).
            - Calculate the **percentage share of mentions** for each brand:
            Percentage Share = (Brand Mentions / Total Brand Mentions) × 100
            - Rank the brands in **descending order of total mentions**.
            - If two brands have the same mention count, assign the same rank number.
            - Round percentages to one decimal place and include “%” in the value.

            Output Format (JSON):
            "Leaderboard": {{
                {{
                    "Brand Name": "<brand>",
                    "Mention Count": "<number>",
                    "Percentage Share": "<x.x>%",
                    "Rank": "<rank_number>"
                }}
            }}


        3. Persona Visibility:  
            Analyze the given {st.session_state.brandprompts} to determine how frequently the brand **{st.session_state.brand_title}** is mentioned across responses associated with each persona from {st.session_state.personas}.
            
            Instructions:
            1. For each persona in {st.session_state.personas}, review all responses within {st.session_state.brandprompts}.
            2. Count how many times the brand **{st.session_state.brand_title}** (case-insensitive) is mentioned within that persona’s responses.
            3. Calculate the **percentage share of brand mentions** for each persona using:
                ```
                Visibility Percentage = (Mentions of {st.session_state.brand_title} in Persona Responses / Total Mentions of {st.session_state.brand_title} across all Personas) × 100
                ```
            4. If the brand is **not mentioned** in a persona’s responses, assign **0.0%** visibility.
            5. Ensure the sum of visibility percentages across all personas equals **100%**.
            6. Use only personas listed in {st.session_state.personas}.
            7. Output must contain one entry per persona.
            
            Output Format (valid JSON only):
            {{
                "Persona Visibility": [
                {{
                    "Persona Name": "<Persona>",
                    "Visibility Percentage": "<x.x>%"
                }}
                ]
            }}
        
        Repeat the same for all personas in {st.session_state.personas}.

        4. Topic Visibility:  

            Analyze the given {st.session_state.brandprompts} to determine how frequently the brand **{st.session_state.brand_title}** is mentioned across each of the topics listed in {st.session_state.topics}.
            
            Instructions:
            - Identify every occurrence of **{st.session_state.brand_title}** (case-insensitive) within the {st.session_state.brandprompts}.
            - For each topic in {st.session_state.topics}, count how many times the brand is mentioned in relation to that topic or in prompts/responses that are clearly about that topic.
            - Calculate the **percentage share of brand mentions** per topic using the formula:
                ```
                Visibility Percentage = (Mentions of {st.session_state.brand_title} in Topic / Total Mentions of {st.session_state.brand_title} across all Topics) × 100
                ```
            - The sum of all topic visibility percentages must equal **100%**.
            - If the brand is not mentioned in a topic, assign **0.0%** visibility.
            Output Format (valid JSON):
            {{
                "Topic Visibility": [
                {{
                    "Topic": "<Topic>",
                    "Visibility Percentage": "<x.x>%"
                }}
                ]
            }}
            Repeat for all topics in {st.session_state.topics}.
           

        5. Consumer Attributes:
            From the given responses related to {st.session_state.brand_title}, extract and quantify the key product or experience attributes most frequently mentioned or emphasized by users.
            
            Instructions:
            1. Identify **distinct product or experience attributes** mentioned in the responses for {st.session_state.brand_title} 
                (examples: delivery, design, price, performance, battery life, durability, support, camera, service, speed, etc.).
            2. Count how many times each attribute (or its close synonyms) appears across all responses.
            3. Calculate each attribute’s **mention share** as:
                ```
                Attribute Percentage = (Mentions of Attribute / Total Mentions of All Attributes) × 100
                ```
            4. Round percentages to one decimal place and ensure they sum to 100%.
            5. Include **only attributes that directly describe or evaluate {st.session_state.brand_title}**.
            6. If no attributes are found, return an empty list.
            
            Output Format (valid JSON only):
            {{
                "Consumer Attributes": [
                {{
                    "Consumer Attribute": "<Attribute>",
                    "Visibility Percentage": "<x.x>%"
                }}
                ]
            }}
            
            Example Output:
            {{
                "Consumer Attributes": [
                {{"Consumer Attribute": "Design", "Visibility Percentage": "32.5%"}},
                {{"Consumer Attribute": "Performance", "Visibility Percentage": "25.0%"}},
                {{"Consumer Attribute": "Price", "Visibility Percentage": "20.0%"}},
                {{"Consumer Attribute": "Durability", "Visibility Percentage": "15.0%"}},
                {{"Consumer Attribute": "Customer Support", "Visibility Percentage": "7.5%"}}
                ]
            }}


        6. Top Sources: For all the {st.session_state.brandprompts} responses, provide a list of sources with the following details for each:
            - Website name or citation
            - Website URL
            - Mention count (number of times the source is referenced in the {st.session_state.brandprompts} responses)
            
            Output Format:

            "Top Sources": {{
                {{
                    "Top Sources": "<Website or Citation Name>",
                    "Mention Count": "<number>",
                    "URL": "<website url>"
                }}
            }}
            
            Repeat same for other Sources
        
        7. Sentiment Analysis: Analyze the sentiment of all given {st.session_state.brandprompts} only for {st.session_state.brand_title}.  
            Instructions:
            1. Consider all responses collectively, not per persona.
            2. Determine percentages for Positive, Neutral, and Negative sentiments.
            3. Describe each sentiment category briefly (10-15 words).
            4. Percentages must sum to 100%. 

            Output Format:

            {{
                "Sentiment Analysis": {{
                    "Positive": {{
                        "Percentage": "<x.x>%",
                        "Description": "<brief description>"
                    }},
                    "Neutral": {{
                        "Percentage": "<x.x>%",
                        "Description": "<brief description>"
                    }},
                    "Negative": {{
                        "Percentage": "<x.x>%",
                        "Description": "<brief description>"
                    }}
                }}
            }}

            

        
        8. Word Association Map: From all given {st.session_state.brandprompts}, extract the 10 most frequently mentioned words or short phrases that define {st.session_state.brand_title} only and give it as a list.
            Instructions:
            1. Consider all responses collectively, not per persona.
            2. Ignore common stopwords (like "the", "and", "is", etc.).
            3. Focus on meaningful words or short phrases that reflect the brand, product, or experience.
            4. Rank them by frequency in descending order.
            5. Output only 10 words or phrases. If multiple words have the same frequency, pick the most representative.
            6. Treat all responses equally; do not separate by person
            7. Also share the count of occurance even duplicates for each mentioned words or short phrases in the list

            Output Format (JSON):
            {{
                "Word Association Map": [
                    {{ "Word": "<word1>", "Count": "<number>" }},
                    {{ "Word": "<word2>", "Count": "<number>" }},
                    {{ "Word": "<word3>", "Count": "<number>" }}
                ]
            }}

        9. Matrix : Analyze the dataset and produce a single JSON object containing two key analyses:

            1. **Persona vs Competitor Matrix**
            2. **Topic vs Competitor Matrix**

            For each, identify competitor mentions, calculate counts and percentages, and summarize brand visibility.  
            Maintain neutrality — only include {st.session_state.brand_title} if it appears in the data.  

            ---

            ### Persona vs Competitor Matrix

            For each persona in the dataset:
            - Identify all competitor brands mentioned in responses (including {st.session_state.brand_title} if present).
            - Count how many responses mention each brand.
            - Calculate each brand’s percentage share of total mentions for that persona.
            - Add a summary:
            - "total_responses": total number of responses for that persona.
            - "responses_with_brand": number of responses mentioning {st.session_state.brand_title}.
            - "brand_mention_percentage": percentage of persona responses mentioning {st.session_state.brand_title}.
            - Always list {st.session_state.brand_title} first if it appears; exclude if not.

            ---

            ### Topic vs Competitor Matrix

            For each topic in {st.session_state.topics}:
            - Identify all competitor brands mentioned in responses related to that topic.
            - Count brand mentions and calculate their percentage of total mentions.
            - Add a summary:
            - "total_responses_with_topic": number of responses associated with the topic.
            - "responses_with_brand": number mentioning {st.session_state.brand_title}.
            - "brand_mention_percentage": percentage of topic responses mentioning {st.session_state.brand_title}.
            - Always list {st.session_state.brand_title} first if it appears; exclude if not.

            ---

            ### OUTPUT FORMAT
            Return only valid JSON in this structure:
            {{
            "Persona vs Competitor Matrix": [
                {{
                "Persona Role": "<Persona Name>",
                "Competitor Mentions": {{
                    "<Brand 1>": <mention count>,
                    "<Brand 2>": <mention count>,
                    "...": "..."
                }},
                "Total Responses": <total number>,
                "Responses with Brand": <number>,
                "Brand Mention Percentage": "<percentage string>"
                }}
                // Repeat for all personas
            ],
            "Topic vs Competitor Matrix": [
                {{
                "Topic": "<Topic Name>",
                "Competitor Mentions": {{
                    "<Brand 1>": <mention count>,
                    "<Brand 2>": <mention count>,
                    "...": "..."
                }},
                "Total Responses with Topic": <total number>,
                "Responses with Brand": <number>,
                "Brand Mention Percentage": "<percentage string>"
                }}
                // Repeat for all topics
            ]
            }}

            
        responses: {st.session_state.brandprompts}
        brands: {st.session_state.brand_title}
        persona: {st.session_state.personas}

        OUTPUT RULES:
        - Return only valid JSON (no markdown, no commentary, no explanations)
        - Use double quotes for all keys and values
        - Each list item must be a string (no nested objects)
        - Do NOT add extra keys or metadata
        - Ensure each section exactly matches the structure above
        - JSON must be directly parsable by json.loads()

        # """
        if Mode=='static':
            #kpi_output= { "Brand Visibility": { "Count of Sky UK": "19", "Count of Brand's Competitors": "25", "Brand Visibility %": "43.1" }, "Leaderboard": [ { "Brand Name": "Sky UK", "Mention Count": "19", "Percentage Share": "43.1%", "Rank": "1" }, { "Brand Name": "Adidas", "Mention Count": "6", "Percentage Share": "13.6%", "Rank": "2" }, { "Brand Name": "Saucony", "Mention Count": "2", "Percentage Share": "4.5%", "Rank": "3" }, { "Brand Name": "Hoka One One", "Mention Count": "3", "Percentage Share": "6.8%", "Rank": "4" }, { "Brand Name": "Under Armour", "Mention Count": "1", "Percentage Share": "2.3%", "Rank": "5" }, { "Brand Name": "PUMA", "Mention Count": "2", "Percentage Share": "4.5%", "Rank": "6" }, { "Brand Name": "Common Projects", "Mention Count": "1", "Percentage Share": "2.3%", "Rank": "7" }, { "Brand Name": "Vans", "Mention Count": "2", "Percentage Share": "4.5%", "Rank": "8" }, { "Brand Name": "Converse", "Mention Count": "2", "Percentage Share": "4.5%", "Rank": "9" }, { "Brand Name": "Skechers", "Mention Count": "2", "Percentage Share": "4.5%", "Rank": "10" }, { "Brand Name": "New Balance", "Mention Count": "4", "Percentage Share": "9.1%", "Rank": "11" }, { "Brand Name": "Brooks", "Mention Count": "2", "Percentage Share": "4.5%", "Rank": "12" }, { "Brand Name": "Cole Haan", "Mention Count": "2", "Percentage Share": "4.5%", "Rank": "13" }, { "Brand Name": "Timberland", "Mention Count": "2", "Percentage Share": "4.5%", "Rank": "14" }, { "Brand Name": "Clarks", "Mention Count": "1", "Percentage Share": "2.3%", "Rank": "15" }, { "Brand Name": "Ecco", "Mention Count": "1", "Percentage Share": "2.3%", "Rank": "16" }, { "Brand Name": "Merrell", "Mention Count": "2", "Percentage Share": "4.5%", "Rank": "17" }, { "Brand Name": "Salomon", "Mention Count": "1", "Percentage Share": "2.3%", "Rank": "18" }, { "Brand Name": "La Sportiva", "Mention Count": "1", "Percentage Share": "2.3%", "Rank": "19" }, { "Brand Name": "Columbia", "Mention Count": "1", "Percentage Share": "2.3%", "Rank": "20" }, { "Brand Name": "Lowa", "Mention Count": "1", "Percentage Share": "2.3%", "Rank": "21" }, { "Brand Name": "Superfeet", "Mention Count": "1", "Percentage Share": "2.3%", "Rank": "22" }, { "Brand Name": "Veja", "Mention Count": "1", "Percentage Share": "2.3%", "Rank": "23" }, { "Brand Name": "Allbirds", "Mention Count": "1", "Percentage Share": "2.3%", "Rank": "24" }, { "Brand Name": " tentree", "Mention Count": "1", "Percentage Share": "2.3%", "Rank": "25" } ], "Persona Visibility": [ { "Persona Name": "Performance-Focused Athlete", "Visibility Percentage": "42.3%" }, { "Persona Name": "Style-Driven Urban Explorer", "Visibility Percentage": "31.4%" }, { "Persona Name": "Comfort-Seeking Commuter", "Visibility Percentage": "17.5%" }, { "Persona Name": "Adventure-Seeking Explorer", "Visibility Percentage": "9.4%" } ], "Common Topics": [ { "Topic": "Best shoes for comfort during long hours", "Visibility Percentage": "27.9%" }, { "Topic": "How to choose shoes for urban style", "Visibility Percentage": "15.5%" }, { "Topic": "Top features to look for in performance footwear", "Visibility Percentage": "22.4%" }, { "Topic": "Tips for selecting durable hiking shoes", "Visibility Percentage": "20.3%" }, { "Topic": "Versatile shoes that transition from day to night", "Visibility Percentage": "6.2%" }, { "Topic": "Importance of fit and sizing in footwear", "Visibility Percentage": "4.7%" }, { "Topic": "Sustainable materials in modern shoe designs", "Visibility Percentage": "3.8%" }, { "Topic": "Finding budget-friendly yet stylish shoes", "Visibility Percentage": "2.4%" }, { "Topic": "Expert reviews on athletic shoe performance", "Visibility Percentage": "2.5%" }, { "Topic": "Maintaining shoes for longevity and comfort", "Visibility Percentage": "1.6%" } ], "Consumer Attributes": [ { "Consumer Attributes": "Comfort", "Visibility Percentage": "30.4%" }, { "Consumer Attributes": "Durability", "Visibility Percentage": "22.3%" }, { "Consumer Attributes": "Style", "Visibility Percentage": "15.7%" }, { "Consumer Attributes": "Performance", "Visibility Percentage": "19.2%" }, { "Consumer Attributes": "Sustainability", "Visibility Percentage": "12.4%" } ], "Top Sources": [ { "Top Sources": "Adidas", "Mention Count": "6", "URL": "https://www.adidas.com" }, { "Top Sources": "Saucony", "Mention Count": "2", "URL": "https://www.saucony.com" }, { "Top Sources": "Hoka One One", "Mention Count": "3", "URL": "https://www.hokaoneone.com" }, { "Top Sources": "PUMA", "Mention Count": "2", "URL": "https://www.puma.com" }, { "Top Sources": "Common Projects", "Mention Count": "1", "URL": "https://www.commonprojects.com" }, { "Top Sources": "Vans", "Mention Count": "2", "URL": "https://www.vans.com" }, { "Top Sources": "Converse", "Mention Count": "2", "URL": "https://www.converse.com" }, { "Top Sources": "Skechers", "Mention Count": "2", "URL": "https://www.skechers.com" }, { "Top Sources": "New Balance", "Mention Count": "4", "URL": "https://www.newbalance.com" }, { "Top Sources": "Brooks", "Mention Count": "2", "URL": "https://www.brooksrunning.com" }, { "Top Sources": "Cole Haan", "Mention Count": "2", "URL": "https://www.colehaan.com" }, { "Top Sources": "Timberland", "Mention Count": "2", "URL": "https://www.timberland.com" }, { "Top Sources": "Clarks", "Mention Count": "1", "URL": "https://www.clarks.com" }, { "Top Sources": "Ecco", "Mention Count": "1", "URL": "https://www.ecco.com" }, { "Top Sources": "Merrell", "Mention Count": "2", "URL": "https://www.merrell.com" }, { "Top Sources": "Salomon", "Mention Count": "1", "URL": "https://www.salomon.com" }, { "Top Sources": "La Sportiva", "Mention Count": "1", "URL": "https://www.lasportiva.com" }, { "Top Sources": "Columbia", "Mention Count": "1", "URL": "https://www.columbia.com" }, { "Top Sources": "Lowa", "Mention Count": "1", "URL": "https://www.lowa.com" }, { "Top Sources": "Superfeet", "Mention Count": "1", "URL": "https://www.superfeet.com" }, { "Top Sources": "Veja", "Mention Count": "1", "URL": "https://www.veja-store.com" }, { "Top Sources": "Allbirds", "Mention Count": "1", "URL": "https://www.allbirds.com" }, { "Top Sources": "tentree", "Mention Count": "1", "URL": "https://www.tentree.com" } ], "Sentiment Analysis": { "Positive": { "Percentage": "65.1%", "Description": "Overall positive comments about Sky UK's quality and performance." }, "Neutral": { "Percentage": "24.4%", "Description": "Objective comments regarding shoe features without strong opinions." }, "Negative": { "Percentage": "10.5%", "Description": "Criticism or complaints about durability and comfort." } }, "Word Association Map": [ { "Word": "Sky UK", "Count": "19" }, { "Word": "comfort", "Count": "11" }, { "Word": "durability", "Count": "9" }, { "Word": "performance", "Count": "8" }, { "Word": "style", "Count": "6" }, { "Word": "sustainability", "Count": "5" }, { "Word": "fit", "Count": "4" }, { "Word": "support", "Count": "4" }, { "Word": "features", "Count": "3" }, { "Word": "flexibility", "Count": "3" } ], "Persona vs Competitor Matrix": [ { "Persona Role": "Performance-Focused Athlete", "Competitor Mentions": { "Sky UK": 19, "Adidas": 6, "Saucony": 2, "Hoka One One": 3, "Under Armour": 1 }, "Total Responses": 5, "Responses with Brand": 5, "Brand Mention Percentage": "100%" }, { "Persona Role": "Style-Driven Urban Explorer", "Competitor Mentions": { "Sky UK": 10, "PUMA": 2, "Vans": 2, "Adidas": 2, "Common Projects": 1 }, "Total Responses": 5, "Responses with Brand": 4, "Brand Mention Percentage": "80%" }, { "Persona Role": "Comfort-Seeking Commuter", "Competitor Mentions": { "Sky UK": 7, "Skechers": 2, "New Balance": 4, "Brooks": 2, "Cole Haan": 2, "Adidas": 2, "Merrell": 2, "Ecco": 1 }, "Total Responses": 5, "Responses with Brand": 5, "Brand Mention Percentage": "100%" }, { "Persona Role": "Adventure-Seeking Explorer", "Competitor Mentions": { "Sky UK": 9, "Merrell": 2, "Salomon": 1, "Columbia": 1, "Lowa": 1, "La Sportiva": 1 }, "Total Responses": 5, "Responses with Brand": 4, "Brand Mention Percentage": "80%" } ], "Topic vs Competitor Matrix": [ { "Topic": "Best shoes for comfort during long hours", "Competitor Mentions": { "Sky UK": 6, "Skechers": 2, "New Balance": 1 }, "Total Responses with Topic": 6, "Responses with Brand": 6, "Brand Mention Percentage": "100%" }, { "Topic": "How to choose shoes for urban style", "Competitor Mentions": { "Sky UK": 4, "PUMA": 2, "Vans": 1 }, "Total Responses with Topic": 5, "Responses with Brand": 4, "Brand Mention Percentage": "80%" }, { "Topic": "Top features to look for in performance footwear", "Competitor Mentions": { "Sky UK": 5, "Adidas": 2 }, "Total Responses with Topic": 5, "Responses with Brand": 5, "Brand Mention Percentage": "100%" }, { "Topic": "Tips for selecting durable hiking shoes", "Competitor Mentions": { "Sky UK": 4, "Merrell": 2, "Columbia": 1 }, "Total Responses with Topic": 5, "Responses with Brand": 4, "Brand Mention Percentage": "80%" }, { "Topic": "Versatile shoes that transition from day to night", "Competitor Mentions": { "Sky UK": 2, "Clarks": 1, "Timberland": 1 }, "Total Responses with Topic": 4, "Responses with Brand": 2, "Brand Mention Percentage": "50%" }, { "Topic": "Importance of fit and sizing in footwear", "Competitor Mentions": { "Sky UK": 3, "New Balance": 1 }, "Total Responses with Topic": 2, "Responses with Brand": 2, "Brand Mention Percentage": "100%" }, { "Topic": "Sustainable materials in modern shoe designs", "Competitor Mentions": { "Sky UK": 2, "Allbirds": 1, "Veja": 1 }, "Total Responses with Topic": 2, "Responses with Brand": 2, "Brand Mention Percentage": "100%" }, { "Topic": "Finding budget-friendly yet stylish shoes", "Competitor Mentions": { "Sky UK": 2, "Vans": 1, "Converse": 1 }, "Total Responses with Topic": 2, "Responses with Brand": 2, "Brand Mention Percentage": "100%" }, { "Topic": "Expert reviews on athletic shoe performance", "Competitor Mentions": { "Sky UK": 3, "Hoka One One": 1 }, "Total Responses with Topic": 2, "Responses with Brand": 2, "Brand Mention Percentage": "100%" }, { "Topic": "Maintaining shoes for longevity and comfort", "Competitor Mentions": { "Sky UK": 1 }, "Total Responses with Topic": 1, "Responses with Brand": 1, "Brand Mention Percentage": "100%" } ] }
            kpi_output = {
  "Brand Visibility": {
    "Count of Sky UK": "12",
    "Count of Brand's Competitors": "16",
    "Brand Visibility %": "42.9"
  },
  "Leaderboard": [
    {"Brand Name": "Sky UK", "Mention Count": "12", "Percentage Share": "42.9%", "Rank": "1"},
    {"Brand Name": "Netflix", "Mention Count": "6", "Percentage Share": "21.4%", "Rank": "2"},
    {"Brand Name": "Amazon Prime Video", "Mention Count": "4", "Percentage Share": "14.3%", "Rank": "3"},
    {"Brand Name": "BT", "Mention Count": "3", "Percentage Share": "10.7%", "Rank": "4"},
    {"Brand Name": "Virgin Media", "Mention Count": "3", "Percentage Share": "10.7%", "Rank": "4"},
    {"Brand Name": "Disney+", "Mention Count": "2", "Percentage Share": "7.1%", "Rank": "6"},
    {"Brand Name": "Apple TV+", "Mention Count": "1", "Percentage Share": "3.6%", "Rank": "7"},
    {"Brand Name": "Vodafone", "Mention Count": "1", "Percentage Share": "3.6%", "Rank": "7"},
    {"Brand Name": "EE", "Mention Count": "1", "Percentage Share": "3.6%", "Rank": "7"},
    {"Brand Name": "Plusnet", "Mention Count": "1", "Percentage Share": "3.6%", "Rank": "7"}
  ],
  "Persona Visibility": [
    {"Persona Name": "Connected Home Streamer", "Visibility Percentage": "33.3%"},
    {"Persona Name": "On-the-Go Multitasker", "Visibility Percentage": "25.0%"},
    {"Persona Name": "Family-Centric Planner", "Visibility Percentage": "33.3%"},
    {"Persona Name": "Budget-Savvy Entertainment Seeker", "Visibility Percentage": "8.4%"}
  ],
  "Topic Visibility": [
    {"Topic": "Performance and stability of streaming services", "Visibility Percentage": "41.7%"},
    {"Topic": "Device compatibility with modern entertainment services", "Visibility Percentage": "16.7%"},
    {"Topic": "Cost-effectiveness of bundled digital services", "Visibility Percentage": "25.0%"},
    {"Topic": "Internet speed and reliability features", "Visibility Percentage": "16.6%"}
  ],
  "Consumer Attributes": [
    {"Consumer Attribute": "Performance", "Visibility Percentage": "25.0%"},
    {"Consumer Attribute": "Stability", "Visibility Percentage": "20.8%"},
    {"Consumer Attribute": "Compatibility", "Visibility Percentage": "16.7%"},
    {"Consumer Attribute": "Cost-effectiveness", "Visibility Percentage": "16.7%"},
    {"Consumer Attribute": "Ease of use", "Visibility Percentage": "20.8%"}
  ],
  "Top Sources": [
    {"Top Sources": "Netflix", "Mention Count": "6", "URL": "https://www.netflix.com"},
    {"Top Sources": "Amazon Prime Video", "Mention Count": "4", "URL": "https://www.amazon.com/primevideo"},
    {"Top Sources": "BT", "Mention Count": "3", "URL": "https://www.bt.com"},
    {"Top Sources": "Virgin Media", "Mention Count": "3", "URL": "https://www.virginmedia.com"},
    {"Top Sources": "Disney+", "Mention Count": "2", "URL": "https://www.disneyplus.com"},
    {"Top Sources": "Apple TV+", "Mention Count": "1", "URL": "https://tv.apple.com"},
    {"Top Sources": "Vodafone", "Mention Count": "1", "URL": "https://www.vodafone.com"},
    {"Top Sources": "EE", "Mention Count": "1", "URL": "https://www.ee.co.uk"},
    {"Top Sources": "Plusnet", "Mention Count": "1", "URL": "https://www.plus.net"}
  ],
  "Sentiment Analysis": {
    "Positive": {"Percentage": "70.0%", "Description": "Comments highlighting Sky UK's reliable service and streaming quality."},
    "Neutral": {"Percentage": "20.0%", "Description": "Objective remarks comparing Sky UK to other providers."},
    "Negative": {"Percentage": "10.0%", "Description": "Criticism regarding service coverage or peak-time performance."}
  },
  "Word Association Map": [
    {"Word": "Sky UK", "Count": "12"},
    {"Word": "streaming", "Count": "7"},
    {"Word": "performance", "Count": "5"},
    {"Word": "stability", "Count": "5"},
    {"Word": "broadband", "Count": "4"},
    {"Word": "compatibility", "Count": "3"},
    {"Word": "Netflix", "Count": "3"},
    {"Word": "Amazon Prime Video", "Count": "3"},
    {"Word": "cost-effective", "Count": "2"},
    {"Word": "Virgin Media", "Count": "2"}
  ],
  "Persona vs Competitor Matrix": [
    {
      "Persona Role": "Connected Home Streamer",
      "Competitor Mentions": {"Sky UK": 4, "Netflix": 3, "Amazon Prime Video": 2, "BT": 1, "Virgin Media": 1},
      "Total Responses": 4,
      "Responses with Brand": 4,
      "Brand Mention Percentage": "100%"
    },
    {
      "Persona Role": "On-the-Go Multitasker",
      "Competitor Mentions": {"Sky UK": 3, "Netflix": 2, "Amazon Prime Video": 1, "EE": 1, "Vodafone": 1},
      "Total Responses": 3,
      "Responses with Brand": 3,
      "Brand Mention Percentage": "100%"
    },
    {
      "Persona Role": "Family-Centric Planner",
      "Competitor Mentions": {"Sky UK": 4, "Netflix": 2, "Disney+": 1, "BT": 1, "Virgin Media": 1},
      "Total Responses": 4,
      "Responses with Brand": 4,
      "Brand Mention Percentage": "100%"
    },
    {
      "Persona Role": "Budget-Savvy Entertainment Seeker",
      "Competitor Mentions": {"Sky UK": 1, "Netflix": 1, "Amazon Prime Video": 1, "Disney+": 1, "Plusnet": 1},
      "Total Responses": 4,
      "Responses with Brand": 1,
      "Brand Mention Percentage": "25%"
    }
  ],
  "Topic vs Competitor Matrix": [
    {
      "Topic": "Performance and stability of streaming services",
      "Competitor Mentions": {"Sky UK": 5, "Netflix": 4, "Amazon Prime Video": 2, "Virgin Media": 1, "BT": 1},
      "Total Responses with Topic": 6,
      "Responses with Brand": 5,
      "Brand Mention Percentage": "83.3%"
    },
    {
      "Topic": "Device compatibility with modern entertainment services",
      "Competitor Mentions": {"Sky UK": 2, "Netflix": 2, "Amazon Prime Video": 1, "Apple TV+": 1},
      "Total Responses with Topic": 4,
      "Responses with Brand": 2,
      "Brand Mention Percentage": "50%"
    },
    {
      "Topic": "Cost-effectiveness of bundled digital services",
      "Competitor Mentions": {"Sky UK": 3, "Netflix": 2, "Amazon Prime Video": 1, "Plusnet": 1},
      "Total Responses with Topic": 4,
      "Responses with Brand": 3,
      "Brand Mention Percentage": "75%"
    },
    {
      "Topic": "Internet speed and reliability features",
      "Competitor Mentions": {"Sky UK": 2, "EE": 1, "Vodafone": 1, "BT": 1, "Virgin Media": 1},
      "Total Responses with Topic": 4,
      "Responses with Brand": 2,
      "Brand Mention Percentage": "50%"
    }
  ]
}


            data = {
                "input_tokens": 20000,
                "output_tokens": 10000,
                "total_tokens": 30000
            }
            st.session_state.kpi_output=kpi_output
        else:
            # ✅ Run LLM only once per session
            if "kpi_output" not in st.session_state:
                st.session_state.kpi_output, data = run_prompts(KPIs)

            # ✅ Use saved results every time page refreshes
            kpi_output = st.session_state.kpi_output

        try:
            page_Results(kpi_output)
        except Exception as e:
            st.error(f"Failed to retrieve KPIs: {e}")
        try:
            c1, c2, c3 = st.columns(3)

            c1.metric("Input Tokens", f"{data['input_tokens']:,}")
            c2.metric("Output Tokens", f"{data['output_tokens']:,}")
            c3.metric("Total Tokens", f"{data['total_tokens']:,}")

            st.markdown("""
                <style>
                [data-testid="stMetricLabel"] {
                    color: white !important;
                    font-size: 15px !important;  /* adjust size as needed */
                }
                [data-testid="stMetricValue"] {
                    color: white !important;
                    font-size: 15px !important;  /* adjust size as needed */
                }
                </style>
                """, unsafe_allow_html=True)
        except: pass

    
elif st.session_state.page == 7:
    try:
        PersonasXtopic = f"""
            You are an AI assistant analyzing structured market comparison data.
            
            INPUT:
            - Dataset: {st.session_state.brandprompts}
            - Brand Context: {st.session_state.brand_title}
            - Product Category: {st.session_state.selectedProduct}
            - Topics: {st.session_state.topics}
            - Personas: {st.session_state.personas}
            
            TASK:
            Analyze how frequently the brand "{st.session_state.brand_title}" is mentioned across all responses
            within each Persona–Topic combination.
            
            For each persona in {st.session_state.personas}:
            1. Review all responses linked to that persona.
            2. For each topic in {st.session_state.topics}
            - Count the total number of responses under this persona–topic combination.
            - Count how many of those responses explicitly mention the brand "{st.session_state.brand_title}" (case-insensitive).
            - Calculate the visibility percentage as:
                (Brand Mentions / Total Responses for that Persona–Topic) × 100
            3. If there are no responses for a Persona–Topic, assign 0.
            
            OUTPUT FORMAT (valid JSON only):
            {{
            "personas": [
                {{
                "name": "<Persona Name>",
                "topics": {{
                    "<Topic 1>": <x.x>,
                    "<Topic 2>": <x.x>,
                    "<Topic 3>": <x.x>
                }}
                }}
            ]
            }}
            
            OUTPUT RULES:
            - Output must be valid JSON only (no markdown or commentary).
            - Use double quotes for all keys and values.
            - Percentages must be numeric integers (0–100) without "%" symbol.
            - Ensure every persona–topic pair appears in the matrix.
            - Sum of percentages is NOT required to be 100; each value stands alone as share of mentions.
            """
        if Mode=='static':
            PersonaXtopic_output = {
                "personas": [
                    {
                        "name": "Connected Home Streamer",
                        "topics": {
                            "Cost-effectiveness of bundled digital services": 0,
                            "Comparing streaming and broadband providers": 0,
                            "Home entertainment services overview": 0
                        }
                    },
                    {
                        "name": "On-the-Go Multitasker",
                        "topics": {
                            "Cost-effectiveness of bundled digital services": 0,
                            "Comparing streaming and broadband providers": 43,
                            "Home entertainment services overview": 0
                        }
                    },
                    {
                        "name": "Family-Centric Planner",
                        "topics": {
                            "Cost-effectiveness of bundled digital services": 0,
                            "Comparing streaming and broadband providers": 0,
                            "Home entertainment services overview": 0
                        }
                    },
                    {
                        "name": "Budget-Savvy Entertainment Seeker",
                        "topics": {
                            "Cost-effectiveness of bundled digital services": 0,
                            "Comparing streaming and broadband providers": 17,
                            "Home entertainment services overview": 0
                        }
                    }
                ]
            }
            data = {
            "input_tokens": 1500,
            "output_tokens": 42,
            "total_tokens": 1542
            }
        else:
            PersonaXtopic_output,data = run_prompts(PersonasXtopic)
        personaXtopic(PersonaXtopic_output)

        c1, c2, c3 = st.columns(3)

        c1.metric("Input Tokens", f"{data['input_tokens']:,}")
        c2.metric("Output Tokens", f"{data['output_tokens']:,}")
        c3.metric("Total Tokens", f"{data['total_tokens']:,}")

        st.markdown("""
            <style>
            [data-testid="stMetricLabel"] {
                color: white !important;
                font-size: 15px !important;  /* adjust size as needed */
            }
            [data-testid="stMetricValue"] {
                color: white !important;
                font-size: 15px !important;  /* adjust size as needed */
            }
            </style>
            """, unsafe_allow_html=True)
    
        # --- Recommendations Display ---
        if st.session_state.selected_cell:
            persona, topic = st.session_state.selected_cell.split("::")
            st.session_state.selected_persona_recommandation=persona
            st.session_state.selected_topic_recommandation=topic
            st.markdown("---")
            st.markdown(
                f"<h3 style='color:white'>Recommendations for <b>{st.session_state.selected_persona_recommandation} → {st.session_state.selected_topic_recommandation}</b></h3>",
                unsafe_allow_html=True
            )

            Recommendation = f"""
            You are an expert content strategist and AI writer.
            Your task is to create multiple types of content for a given **persona** and **topic**.

            ---
            **Persona:** {st.session_state.selected_persona_recommandation}
            **Topic:** {st.session_state.selected_topic_recommandation}
            ---

            For this persona and topic, generate the following content:

            1. **FAQ**  
            - 4–6 common questions with concise, accurate answers.  
            - Format as a JSON array of objects with keys "question" and "answer".

            2. **Knowledge Article**  
            - 2–3 paragraphs of in-depth explanation or tutorial-style content.  
            - Format as a JSON object with key "content" containing the full text.

            3. **Social Posts**  
            - 3 short, catchy posts (max 280 characters each).  
            - Format as a JSON array of strings.

            4. **How-To Guide**  
            - Step-by-step instructions (4–7 steps) with optional brief tips.  
            - Format as a JSON array of objects with keys "step" and "tip".

            5. **AI-Optimized Version**  
            - Rewrite the key insights using authoritative, structured language suitable for LLM citation.  
            - Format as a JSON object with key "content".

            6. **Brand Voice Version**  
            - Adapt all content to match the brand’s unique tone and personality.  
            - Format as a JSON object with key "content".

            ---
            **Important Instructions:**
            - Output must be **valid JSON only** — no extra text, explanations, or markdown.
            - Ensure all arrays and objects are properly formatted.
            - Use concise, factual, and persona-appropriate language.
            - Do not add extra numbering or keys outside the specified format.

            **Output Example (JSON only):**
            ```json
            {{
            "FAQ": [{{"question": "...", "answer": "..."}}, {{"question": "...", "answer": "..."}}],
            "Knowledge Article": {{"content": "..."}},
            "Social Posts": ["...", "...", "..."],
            "How-To Guide": [{{"step": "...", "tip": "..."}}], 
            "AI-Optimized Version": {{"content": "..."}},
            "Brand Voice Version": {{"content": "..."}}
            }}"""
            if Mode=='static':
                Recommendation_output={
                "FAQ": [
                    {
                    "question": "What are the key features to look for in a broadband and TV package for families?",
                    "answer": "Look for high-speed internet, a generous data cap, family-friendly TV channels, parental controls, and reliable customer support."
                    },
                    {
                    "question": "How can I ensure the broadband speed is sufficient for my family?",
                    "answer": "Consider the number of devices used simultaneously and opt for a package offering speeds of at least 25 Mbps to support streaming, gaming, and browsing."
                    },
                    {
                    "question": "Are there any cost-effective broadband and TV packages ideal for families?",
                    "answer": "Yes, many providers offer bundles that include both services at a discounted rate. Compare multiple providers to find the best deals."
                    },
                    {
                    "question": "What parental control features should I look for in these packages?",
                    "answer": "Seek packages that offer comprehensive parental controls for both TV and internet, allowing you to manage access and set viewing limits."
                    }
                ],
                "Knowledge Article": {
                    "content": "Selecting the right broadband and TV package for families is crucial, as it impacts both entertainment and connectivity. Families should look for packages that offer a blend of high-speed internet and a variety of TV channels catering to all age groups. High-speed internet is essential for supporting multiple devices and activities such as online schooling, work from home setups, and streaming services. Additionally, consider packages with flexible upgrade options to easily adapt to changing needs. When it comes to TV, a good family package will include channels for children, educational content, and entertainment that appeals to adults as well. Bundling these services can often lead to cost savings and simplified customer service experiences."
                },
                "Social Posts": [
                    "Looking for a family-friendly broadband & TV bundle? Look no further! Our packages offer high-speed internet & channels everyone will love. #FamilyEntertainment #BroadbandDeals",
                    "Upgrade your family time with our top-rated broadband and TV packages! Fast speeds, great channels, and happy moments await! #StayConnected #FamilyFun",
                    "Stream, browse, and enjoy together! Our family packages are designed to keep everyone connected and entertained. Check them out now! #BroadbandForFamilies #FamilyTV"
                ],
                "How-To Guide": [
                    {
                    "step": "Determine your family's internet and TV usage needs, considering both the number of users and types of activities.",
                    "tip": "Make a list of all devices that will connect to your network to estimate needed speed."
                    },
                    {
                    "step": "Research and compare different broadband and TV packages available in your area.",
                    "tip": "Use comparison websites to find the best deals and read customer reviews for reliability insights."
                    },
                    {
                    "step": "Check for bundles offered by service providers that might include both internet and TV services at a discounted rate."
                    },
                    {
                    "step": "Consider the parental controls available with the packages to ensure safe viewing and browsing for your children."
                    },
                    {
                    "step": "Contact the service providers to discuss contract terms and installation processes before finalizing the deal."
                    }
                ],
                "AI-Optimized Version": {
                    "content": "For families, selecting an appropriate broadband and TV package is pivotal for ensuring sufficient entertainment and connectivity options. Ideal packages offer high-speed internet capable of handling multiple simultaneous connections and a diverse array of TV channels suitable for all family members. Bundles often provide cost efficiency and the convenience of a single provider. When choosing a package, it is advisable to consider the number of users, the types of digital activities engaged in, and any necessary parental control features to maintain a safe media environment."
                },
                "Brand Voice Version": {
                    "content": "Hey there, nostalgic families! Ready to throw it back with some modern convenience? Our broadband and TV packages are like a cozy blanket from the past, with all the warmth of today’s technology. We’ve wrapped up high-speed internet and captivating TV channels into one sweet bundle, just for you. With our deals, your family can connect, stream, and relive all those golden oldies without missing a beat. Dive into our family-friendly packages that are built on value, sprinkled with fun, and designed with love, ensuring every family moment is brilliantly connected."
                }
                }
                data = {
                    "input_tokens": 2000,
                    "output_tokens": 42,
                    "total_tokens": 2042
                }
            else:
                Recommendation_output,data = run_prompts(Recommendation)
            Recommendations(Recommendation_output)
            c1, c2, c3 = st.columns(3)

            c1.metric("Input Tokens", f"{data['input_tokens']:,}")
            c2.metric("Output Tokens", f"{data['output_tokens']:,}")
            c3.metric("Total Tokens", f"{data['total_tokens']:,}")

            st.markdown("""
            <style>
            [data-testid="stMetricLabel"] {
                color: white !important;
                font-size: 15px !important;  /* adjust size as needed */
            }
            [data-testid="stMetricValue"] {
                color: white !important;
                font-size: 15px !important;  /* adjust size as needed */
            }
            </style>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Failed to retrieve Recommendations: {e}")
