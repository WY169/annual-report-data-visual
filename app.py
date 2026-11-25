import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="年报数据可视化", page_icon="📊", layout="wide")
st.title("📈 上市公司年报数据分析看板")
st.markdown("本项目基于年报财务指标，进行多维度趋势与分布可视化")

@st.cache_data
def load_data(file_path="annual_report.csv"):
    try:
        df = pd.read_csv(file_path, encoding="utf-8-sig")
        return df
    except FileNotFoundError:
        return None

df = load_data()

st.sidebar.subheader("数据导入")
uploaded_file = st.sidebar.file_uploader("上传年报 CSV", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="utf-8-sig")

if df is not None:
    st.success("✅ 数据加载成功")
    with st.expander("🔍 原始数据预览"):
        st.dataframe(df.head(20), use_container_width=True)

    st.subheader("📋 描述性统计")
    st.dataframe(df.describe(), use_container_width=True)

    st.sidebar.divider()
    st.sidebar.subheader("筛选条件")
    if "年份" in df.columns:
        year_list = sorted(df["年份"].unique().tolist())
        selected_years = st.sidebar.multiselect("选择年份", year_list, default=year_list)
        df_filter = df[df["年份"].isin(selected_years)]
    else:
        df_filter = df

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("营收变化趋势")
        if "年份" in df_filter.columns and "营业收入" in df_filter.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(data=df_filter, x="年份", y="营业收入", marker="o", ax=ax)
            ax.set_xlabel("年份")
            ax.set_ylabel("营业收入")
            ax.set_title("营业收入趋势图")
            st.pyplot(fig)
        else:
            st.info("缺少【年份 / 营业收入】字段")

    with col2:
        st.subheader("净利润分布")
        if "净利润" in df_filter.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(df_filter["净利润"], kde=True, ax=ax)
            ax.set_xlabel("净利润")
            ax.set_title("净利润分布直方图")
            st.pyplot(fig)
        else:
            st.info("缺少【净利润】字段")

    st.subheader("利润率散点图")
    if "年份" in df_filter.columns and "销售利润率" in df_filter.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.scatterplot(data=df_filter, x="年份", y="销售利润率", s=120, alpha=0.7, ax=ax)
        ax.set_title("销售利润率散点")
        st.pyplot(fig)
    else:
        st.info("缺少【年份 / 销售利润率】")

    st.divider()
    st.subheader("📌 核心指标速览")
    metric_cols = st.columns(3)
    if "营业收入" in df_filter.columns:
        metric_cols[0].metric("总营收", f"{df_filter['营业收入'].sum():,.0f}")
    if "净利润" in df_filter.columns:
        metric_cols[1].metric("平均净利润", f"{df_filter['净利润'].mean():,.2f}")
    if "资产负债率" in df_filter.columns:
        metric_cols[2].metric("平均资产负债率", f"{df_filter['资产负债率'].mean():,.2%}")

else:
    st.warning("⚠️ 没有找到 annual_report.csv")
    st.markdown("表头：`年份,公司名称,营业收入,净利润,销售利润率,资产负债率`")

st.divider()
st.caption("年报可视化项目｜Streamlit")
