import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu, ttest_ind, f_oneway, wilcoxon, kruskal, chi2_contingency

st.set_page_config(page_title="Generic Performance Dashboard", layout="centered")
st.title("📊 Generic Performance Dashboard")

# File upload
uploaded = st.file_uploader("Upload your CSV file", type="csv")
if not uploaded:
    st.warning("👈 Please upload a CSV file to get started.")
    st.stop()

# Load the uploaded CSV
try:
    df = pd.read_csv(uploaded)
except Exception as e:
    st.error(f"❌ Could not read the file: {e}")
    st.stop()

num_cols = df.select_dtypes(include='number').columns.tolist()
if len(num_cols) < 2:
    st.error("❌ Your file needs at least two numeric columns.")
    st.stop()

# Dropdowns
col1 = st.selectbox("X-axis", num_cols, index=0)
col2 = st.selectbox("Y-axis", num_cols, index=1)

# Plot Type
plot_type = st.radio("Plot Type", ["Boxplot", "Violin", "Histogram", "KDE"])

# Plot
st.subheader(f"{plot_type} of {col1} and {col2}")
fig, ax = plt.subplots()
if plot_type == "Boxplot":
    sns.boxplot(data=df[[col1, col2]], ax=ax)
elif plot_type == "Violin":
    sns.violinplot(data=df[[col1, col2]], ax=ax)
elif plot_type == "Histogram":
    sns.histplot(df[col1], label=col1, kde=True, ax=ax)
    sns.histplot(df[col2], label=col2, kde=True, ax=ax)
    ax.legend()
elif plot_type == "KDE":
    sns.kdeplot(df[col1], fill=True, label=col1, ax=ax)
    sns.kdeplot(df[col2], fill=True, label=col2, ax=ax)
    ax.legend()
st.pyplot(fig)

# Statistical Test
test_choice = st.selectbox("Statistical Test", ["Mann-Whitney U", "T-test", "ANOVA", "Wilcoxon", "Kruskal-Wallis", "Chi-Square"])

x, y = df[col1].dropna(), df[col2].dropna()
try:
    if test_choice == "Mann-Whitney U":
        stat, p = mannwhitneyu(x, y)
    elif test_choice == "T-test":
        stat, p = ttest_ind(x, y)
    elif test_choice == "ANOVA":
        stat, p = f_oneway(x, y)
    elif test_choice == "Wilcoxon":
        stat, p = wilcoxon(x, y)
    elif test_choice == "Kruskal-Wallis":
        stat, p = kruskal(x, y)
    elif test_choice == "Chi-Square":
        table = pd.crosstab(df[col1], df[col2])
        stat, p, _, _ = chi2_contingency(table)

    st.markdown(f"### {test_choice} Result")
    st.write(f"**Statistic**: {stat:.3f}")
    st.write(f"**P-value**: {p:.5f}")
except Exception as e:
    st.error(f"Error running test: {e}")
