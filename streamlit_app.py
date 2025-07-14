import streamlit as st
import requests
import tempfile
import os

# Page config
st.set_page_config(page_title="📄 Intelligent Document Processor", layout="centered")
st.markdown(
    """
    <style>
        .main {
            background-color: #111827;
            color: #F9FAFB;
        }
        .stTextInput > div > div > input {
            color: white;
            background-color: #1F2937;
            border: 1px solid #374151;
        }
        .stFileUploader {
            border: 1px dashed #4B5563;
        }
        .stButton > button {
            background-color: #EF4444;
            color: white;
            border-radius: 6px;
            padding: 0.5rem 1rem;
        }
        .stDownloadButton {
            margin-top: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='color: #F9FAFB;'>📄Technical Document Analyzer</h1>", unsafe_allow_html=True)

# Upload + Instruction
uploaded_file = st.file_uploader(
    "📎 Upload a document (PDF, PNG, JPG, etc.)",
    type=["pdf", "png", "jpg", "jpeg", "tif", "tiff"]
)

instruction = st.text_input(
    "✍️ Enter your instruction (e.g., 'Extract termination clause', 'Explain this diagram')"
)

if uploaded_file and instruction:
    if st.button("🔍 Extract"):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            files = {"file": (uploaded_file.name, open(tmp_path, "rb"), uploaded_file.type)}
            data = {"instruction": instruction}
            response = requests.post("http://localhost:8000/extract-text/", files=files, data=data)

            if response.status_code == 200:
                result = response.json()

                if "summary" in result:
                    st.markdown("### 🧾 Summary")
                    st.success(result["summary"])

                if "output" in result and isinstance(result["output"], dict):
                    st.markdown("### 📌 Parsed Instruction Output")
                    for key, value in result["output"].items():
                        if isinstance(value, dict) and "text" in value:
                            st.markdown(f"**{key}:** {value['text']}")
                            if "confidence" in value:
                                st.markdown(f"🧠 Confidence: `{value['confidence'] * 100:.1f}%`")
                        else:
                            st.markdown(f"**{key}:** {value}")

                if "flagged" in result and result["flagged"]:
                    st.markdown("### ⚠️ Risk Flags")
                    for flag in result["flagged"]:
                        st.error(flag)

                if "tables" in result and result["tables"]:
                    st.markdown("### 📊 Extracted Tables")
                    for i, table in enumerate(result["tables"]):
                        st.markdown(f"**Table {i+1}**")
                        st.dataframe(table)

                if "csv_path" in result:
                    with open(result["csv_path"], "rb") as f:
                        st.download_button("📥 Download CSV", f, file_name="vlm_output.csv")

        except Exception as e:
            st.error(f"❌ Error: {e}")
