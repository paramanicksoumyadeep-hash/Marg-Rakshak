import streamlit as st
import pandas as pd
import json
import os
from PIL import Image

st.set_page_config(page_title="Eagle's Eye Dashboard", layout="wide")

st.title("🦅 Eagle's Eye: Traffic Violation Command Center")

# The user runs this from the project root, so the path should just be outputs/evidence
EVIDENCE_DIR = "outputs/evidence"

def load_data():
    if not os.path.exists(EVIDENCE_DIR):
        return pd.DataFrame()
        
    records = []
    for f in os.listdir(EVIDENCE_DIR):
        if f.endswith('.json'):
            with open(os.path.join(EVIDENCE_DIR, f), 'r') as file:
                data = json.load(file)
                for v in data.get('violations', []):
                    records.append({
                        "evidence_id": data['evidence_id'],
                        "camera_id": data['camera_id'],
                        "timestamp": data['timestamp'],
                        "violation_type": v['type'],
                        "confidence": v['confidence'],
                        "needs_review": v['needs_human_review'],
                        "status": data['reviewer_status'],
                        "plate_number": v.get('plate_number', 'N/A')
                    })
    return pd.DataFrame(records)

df = load_data()

if df.empty:
    st.warning("No evidence data found. Run the batch pipeline first.")
else:
    # Top level metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Violations", len(df))
    col2.metric("Pending Review", len(df[df['status'] == 'PENDING']))
    col3.metric("Auto-Challans Issued", len(df[df['status'] == 'APPROVED']))
    col4.metric("False Positives Rejected", len(df[df['status'] == 'REJECTED']))
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Analytics", "📋 Human Review Queue", "🔍 Search & Export"])
    
    with tab1:
        st.subheader("Violation Trends")
        if not df.empty:
            type_counts = df['violation_type'].value_counts()
            st.bar_chart(type_counts)
            
    with tab2:
        st.subheader("Human Review Queue (Low Confidence Detections)")
        queue = df[(df['needs_review'] == True) & (df['status'] == 'PENDING')]
        
        if queue.empty:
            st.success("Queue is empty! All high-confidence.")
        else:
            for idx, row in queue.iterrows():
                with st.expander(f"Review {row['evidence_id']} - {row['violation_type']}"):
                    img_path = os.path.join(EVIDENCE_DIR, f"{row['evidence_id']}.jpg")
                    if os.path.exists(img_path):
                        img = Image.open(img_path)
                        st.image(img, caption=f"Conf: {row['confidence']:.2f} | Plate: {row['plate_number']}")
                    
                    c1, c2 = st.columns(2)
                    if c1.button("✅ Approve (Issue Challan)", key=f"app_{row['evidence_id']}"):
                        # Logic to update JSON would go here
                        st.success("Approved!")
                    if c2.button("❌ Reject (False Positive)", key=f"rej_{row['evidence_id']}"):
                        # Logic to update JSON would go here
                        st.error("Rejected.")
                        
    with tab3:
        st.subheader("Search Records")
        plate_search = st.text_input("Search by License Plate")
        if plate_search:
            filtered_df = df[df['plate_number'].str.contains(plate_search, case=False, na=False)]
            st.dataframe(filtered_df)
        else:
            st.dataframe(df)
            
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="eagles_eye_export.csv",
            mime="text/csv",
        )
