# main.py

import streamlit as st
from parse import prase_with_ollama
from scrape import (
    scrape_website,
    split_dom_content,
    clean_bodycontent,
    extract_body_content
)

st.title("AI Web Scraper")

# URL Input
url = st.text_input("Enter the URL of the website to scrape:")

if st.button("Scrape"):
    if not url:
        st.error("Please enter a URL.")
    else:
        st.write(f"Scraping the website: {url}")

        with st.spinner("Fetching website..."):
            try:
                result = scrape_website(url)
            except Exception as e:
                st.error(f"Failed to scrape: {e}")
                result = None

        if result:
            body_html = extract_body_content(result)
            cleaned_text = clean_bodycontent(body_html)

            st.session_state.dom_content = cleaned_text

            with st.expander("View DOM Content"):
                st.text_area("DOM Content", cleaned_text, height=300)

# Parsing section
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to extract:")

    if st.button("Parse Content"):
        if not parse_description:
            st.error("Please enter what you want to extract.")
        else:
            with st.spinner("Parsing the content..."):
                try:
                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    parsed_output = prase_with_ollama(dom_chunks, parse_description)

                    st.session_state.parsed_result = parsed_output
                    st.success("Parsing completed.")

                except Exception as e:
                    st.error(f"Parsing failed: {e}")

# Display parsed result
if "parsed_result" in st.session_state:
    with st.expander("Parsed Result", expanded=True):
        st.text_area("Result", st.session_state.parsed_result, height=300)
