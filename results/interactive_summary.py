import pandas as pd
import streamlit as st

st.set_page_config(page_title='Supply Chain Defect Dashboard', layout='wide')

st.title('Supply Chain Defect Analysis Dashboard')
st.caption('Interactive summary for the generated supply-chain defect project')

@st.cache_data
def load_data():
    suppliers = pd.read_csv('data/suppliers.csv')
    batches = pd.read_csv('data/component_batches.csv')
    qc = pd.read_csv('data/qc_results.csv')
    defects = pd.read_csv('data/defects.csv')
    analysis = pd.read_csv('data/analytical_dataset.csv')
    return suppliers, batches, qc, defects, analysis

suppliers, batches, qc, defects, analysis = load_data()

st.subheader('Dataset Overview')
col1, col2, col3, col4 = st.columns(4)
col1.metric('Suppliers', len(suppliers))
col2.metric('Batches', len(batches))
col3.metric('QC Units', len(qc))
col4.metric('Defects', len(defects))

st.subheader('Business Insight Filters')
selected_component = st.selectbox('Choose component', ['All'] + sorted(analysis['component_name'].unique().tolist()))
selected_supplier = st.selectbox('Choose supplier', ['All'] + sorted(analysis['supplier_id'].astype(int).unique().tolist()))

filtered = analysis.copy()
if selected_component != 'All':
    filtered = filtered[filtered['component_name'] == selected_component]
if selected_supplier != 'All':
    filtered = filtered[filtered['supplier_id'] == int(selected_supplier)]

if filtered.empty:
    st.warning('No data available for the selected combination.')
else:
    st.subheader('Filtered Metrics')
    col1, col2, col3 = st.columns(3)
    col1.metric('Average Defect Rate', f"{filtered['defect_rate'].mean():.6f}")
    col2.metric('Median Defect Rate', f"{filtered['defect_rate'].median():.6f}")
    col3.metric('Defect Rate Max', f"{filtered['defect_rate'].max():.6f}")

    st.dataframe(filtered[['supplier_id', 'component_name', 'quantity_produced', 'defect_rate', 'quality_score', 'lead_time_days']].head(20), use_container_width=True)

st.subheader('Supplier Risk Ranking')
risk = analysis.groupby('supplier_id')['defect_rate'].mean().sort_values(ascending=False).reset_index()
risk.columns = ['supplier_id', 'avg_defect_rate']
st.bar_chart(risk.head(10).set_index('supplier_id'))

st.subheader('Component Risk Ranking')
component_risk = analysis.groupby('component_name')['defect_rate'].mean().sort_values(ascending=False).reset_index()
component_risk.columns = ['component_name', 'avg_defect_rate']
st.bar_chart(component_risk.head(10).set_index('component_name'))

st.subheader('Operational Notes')
st.markdown('''
- Supplier quality varies meaningfully across production partners.
- A small subset of suppliers and component families deserve early inspection.
- The model should be used as a pre-emptive QA trigger rather than a final release decision.
''')
