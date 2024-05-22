import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="SBAC Tagalog Translator",
)

# clear translations when a new term is entered
def clear_translations():
    if 'english_term' in st.session_state and not st.session_state['english_term']:
        st.session_state['tagalog_translation'] = 'Tagalog translation will appear here.'
        st.session_state['context'] = 'Context will appear here after translating a term.'
        st.session_state['other_translations'] = pd.DataFrame()
        st.session_state['input_disabled'] = True

# css code
st.markdown("""
                        
<style>

.stTextInput input, .stTextArea textarea {
    border: 2px solid #4FA1F3; /* Blue border */
    border-radius: 5px;
}

div[data-baseweb="select"] {
    border: 2px solid #4FA1F3 !important; /* Blue border for the select box */
    border-radius: 5px !important;
    background-color: white; /* Ensures the background is white */
}           
            
button {
    border: 1px solid #28a745 !important;
    color: white !important;
    background-color: #28a745 !important;
    border-radius: 5px !important;
}

.css-2trqyj:hover {
    background-color: #218838;
    border-color: #1e7e34;
}

.stTextInput, .stTextArea {
    margin-bottom: 1rem;
}

.stTable {
    width: 100%;
    border-collapse: collapse;
}

.stTable th {
    background-color: #4FA1F3;
    color: white;
}

.stTable td, .stTable th {
    padding: 0.5rem;
    border: 1px solid #ddd;
}

.stTable tr:nth-child(odd) {
    background-color: #f8f8f8;
}

.fixed-logo {
    position: fixed;
    right: 50px;
    top: 100px;
    z-index: 10;
}                

</style>
""", unsafe_allow_html=True)

logo_url = "https://smarterbalanced.org/wp-content/uploads/2020/07/SmarterBalanced_Logo_Horizontal_Color_R.png"

# SB logo
st.markdown(f"""
    <div class="fixed-logo">
        <img src="{logo_url}" alt="Company logo" style="width:200px;">  <!-- Adjust width as needed -->
    </div>
""", unsafe_allow_html=True)

# load CSVs !CHANGE PATH!
csv_file_path = 'sample_tfidf.csv'
data = pd.read_csv(csv_file_path)
data.columns = data.columns.str.strip()
english_terms = data['Term in English'].dropna().unique().tolist()

# session state variables
if 'selected_english_term' not in st.session_state:
    st.session_state['selected_english_term'] = ''
if 'english_term' not in st.session_state:
    st.session_state['english_term'] = ''
if 'tagalog_translation' not in st.session_state:
    st.session_state['tagalog_translation'] = 'Tagalog translation will appear here.'
if 'context' not in st.session_state:
    st.session_state['context'] = 'Context will appear here after translating a term.'
if 'other_translations' not in st.session_state:
    st.session_state['other_translations'] = pd.DataFrame()
if 'input_disabled' not in st.session_state:
    st.session_state['input_disabled'] = True

# find translation function
def find_translations(term):
    return data[data['Term in English'].str.lower() == term.lower()]

# on button click function
def handle_translate():
    term = st.session_state.selected_english_term.strip().lower()
    if term:
        translations = data[data['Term in English'].str.lower() == term]
        if not translations.empty:
            st.session_state['tagalog_translation'] = translations.iloc[0]['Term in Tagalog']
            st.session_state['context'] = translations.iloc[0]['Example Prompt']
            other_translations = translations.reset_index(drop=True)
            other_translations.index += 1
            st.session_state['other_translations'] = other_translations
            st.session_state['input_disabled'] = False
        else:
            st.session_state['tagalog_translation'] = 'No translation found'
            st.session_state['context'] = 'No context available for this term.'
            st.session_state['other_translations'] = pd.DataFrame()
            st.session_state['input_disabled'] = True
    else:
        # Clear previous results if the input is empty
        st.session_state['tagalog_translation'] = 'Tagalog translation will appear here.'
        st.session_state['context'] = 'Context will appear here after translating a term.'
        st.session_state['other_translations'] = pd.DataFrame()
        st.session_state['input_disabled'] = True

# UI layout
with st.container():
    st.title('Context-aware Term Translation for Tagalog')

    # input and output columns
    col1, col2 = st.columns(2)
    
    with col1:
        # english term input box
        st.session_state.selected_english_term = st.selectbox(
            '🇺🇸 English (EN)', 
            english_terms,
            index=english_terms.index(st.session_state.selected_english_term) if st.session_state.selected_english_term in english_terms else 0,
            format_func=lambda x: x if x else "Select an English term"
        )

    with col2:
        # tagalog term output box
        st.text_input('🇵🇭 Tagalog (TL) - Preferred Translation', value=st.session_state['tagalog_translation'], 
                      disabled=st.session_state['input_disabled'], help="Type or select an English term in the input field below '🇺🇸 English (EN)' to generate the preferred Tagalog translation.")

    # translate button
    translate_button = st.button('Translate', on_click=handle_translate)

    # context box
    st.text_area('Example of Preferred Translation in Context:', value=st.session_state['context'], height=100)

    # other candidate translations table
    if not st.session_state['other_translations'].empty:
        st.subheader('Other Candidate Translations')
        html_table = """
        <style>
            .custom-table {
                width: 100%;
                border-collapse: collapse;
            }
            .custom-table th {
                background-color: #4FA1F3; /* Blue header */
                color: white;
                padding: 10px;
            }
            .custom-table td, .custom-table th {
                padding: 10px;
                border: 1px solid #ddd; /* Light grey border */
            }
            .custom-table tbody tr:nth-child(odd) {
                background-color: #f8f8f8; /* Light grey for odd rows */
            }
            .custom-table tbody tr:nth-child(even) {
                background-color: #ffffff; /* White for even rows */
            }
            .custom-table tbody tr:first-child {
                background-color: #e6f7ff; /* Light blue background for the first row */
            }
            .custom-table tr:hover {
                background-color: #e8e8e8; /* Slightly darker row highlight on hover */
            }
        </style>
        <table class="custom-table">
            <thead>
                <tr><th>#</th><th>Term in Tagalog</th><th>Example Prompt</th><th># of Instances of Translation</th></tr>
            </thead>
            <tbody>
        """
        # underline terms
        term_to_highlight = re.escape(st.session_state.selected_english_term)
        for idx, row in st.session_state['other_translations'].iterrows():
            term_in_context = re.sub(f"(?i){term_to_highlight}", 
                                    lambda match: f"<u>{match.group(0)}</u>", 
                                    row['Example Prompt'])
            html_table += f"<tr><td>{idx}</td><td>{row['Term in Tagalog']}</td><td>{term_in_context}</td><td>{row['# of Occurrences of the Word Pair']}</td></tr>"
        html_table += "</tbody></table>"
        st.markdown(html_table, unsafe_allow_html=True)

