
import streamlit as st
import pandas as pd

# อ่านข้อมูลจากไฟล์ Excel
uploaded_file = 'ไฟล์รวมคะแนน.xlsx'
df = pd.read_excel(uploaded_file, sheet_name=None)

# รวมทุก sheet เข้าเป็น DataFrame เดียว
all_data = pd.DataFrame()
for sheet_name, sheet_data in df.items():
    sheet_data['เขตเลือกตั้ง'] = sheet_name  # เพิ่มชื่อเขตจากชื่อ sheet
    all_data = pd.concat([all_data, sheet_data], ignore_index=True)

# แสดงหัวตาราง
st.title("รายงานผลการนับคะแนนเลือกตั้ง")
st.write("แสดงรายชื่อผู้สมัครเรียงตามคะแนนที่ได้รับ")

# ตรวจสอบว่าคอลัมน์สำคัญมีอยู่จริง
required_columns = ['ชื่อ-สกุล', 'คะแนน', 'เขตเลือกตั้ง']
if not all(col in all_data.columns for col in required_columns):
    st.error("ไฟล์ข้อมูลไม่ตรงกับรูปแบบที่ระบบต้องการ กรุณาตรวจสอบชื่อคอลัมน์")
else:
    # แปลงคะแนนเป็นตัวเลข (บางกรณีอาจอ่านเป็นวัตถุหรือมีค่าว่าง)
    all_data['คะแนน'] = pd.to_numeric(all_data['คะแนน'], errors='coerce').fillna(0).astype(int)

    # เรียงข้อมูลตามคะแนนจากมากไปน้อย
    sorted_df = all_data.sort_values(by='คะแนน', ascending=False)

    # กรองตามเขตเลือกตั้ง
    district_list = sorted_df['เขตเลือกตั้ง'].unique().tolist()
    selected_district = st.selectbox("เลือกเขตเลือกตั้ง", options=["ทุกเขต"] + district_list)

    if selected_district != "ทุกเขต":
        sorted_df = sorted_df[sorted_df['เขตเลือกตั้ง'] == selected_district]

    # แสดงตารางเรียงตามคะแนน
    st.dataframe(sorted_df[['ชื่อ-สกุล', 'คะแนน', 'เขตเลือกตั้ง']])

    # สรุปคะแนนรวมต่อเขต
    st.subheader("คะแนนรวมแยกตามเขตเลือกตั้ง")
    summary = all_data.groupby('เขตเลือกตั้ง')['คะแนน'].sum().reset_index()
    st.bar_chart(summary.set_index('เขตเลือกตั้ง'))
