import streamlit as st
import pandas as pd
from src.lead_analyzer import analyze_companies

def short_text(text: str, limit: int) -> str:
    text = str(text).strip()
    if len(text) <= limit:
        return text

    trimmed = text[:limit].rstrip()
    last_punctuation = max(trimmed.rfind("."), trimmed.rfind(","), trimmed.rfind(";"))

    if last_punctuation > int(limit * 0.6):
        trimmed = trimmed[: last_punctuation + 1]
    else:
        last_space = trimmed.rfind(" ")
        if last_space > 0:
            trimmed = trimmed[:last_space]

    return trimmed.rstrip() + "..."


def metric_card(title: str, value: str, subtitle: str):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg,#0f172a,#1e293b);
            padding:14px;
            border-radius:16px;
            color:white;
            border:1px solid rgba(255,255,255,0.06);
            box-shadow:0 4px 12px rgba(0,0,0,0.12);
            text-align:left;
            min-height:110px;
        ">
            <div style="font-size:12px;color:#94a3b8;margin-bottom:6px;">{title}</div>
            <div style="font-size:26px;font-weight:900;margin-bottom:4px;">{value}</div>
            <div style="font-size:11px;color:#64748b;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def lead_card(rank: int, company: str, industry: str, score: str, summary: str):
    st.markdown(
        f"""
        <div style="
            background:white;
            padding:14px;
            border-radius:16px;
            border:1px solid #e2e8f0;
            box-shadow:0 6px 18px rgba(0,0,0,0.06);
            min-height:180px;
        ">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <span style="
                    background:#e0f2fe;
                    color:#0369a1;
                    padding:5px 10px;
                    border-radius:999px;
                    font-size:12px;
                    font-weight:700;
                ">Rank #{rank}</span>
                <span style="
                    background:#dcfce7;
                    color:#166534;
                    padding:5px 10px;
                    border-radius:999px;
                    font-size:12px;
                    font-weight:700;
                ">{score}</span>
            </div>
            <div style="font-size:18px;font-weight:800;color:#0f172a;margin-bottom:4px;">{company}</div>
            <div style="font-size:13px;color:#64748b;font-weight:700;margin-bottom:10px;">{industry}</div>
            <div style="font-size:14px;color:#334155;line-height:1.6;">
                {short_text(summary, 125)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def normalize_key(value: str) -> str:
    return str(value).strip().lower()


st.set_page_config(page_title="AI Growth Agent", page_icon="🚀", layout="wide")

st.markdown(
    """
    <style>
        .block-container {
            max-width: 1360px;
            padding-top: 1rem;
            padding-bottom: 1.6rem;
        }
        .stButton > button {
            width: 100%;
            height: 3rem;
            border-radius: 12px;
            font-weight: 700;
            border: none;
        }
        .stDownloadButton > button {
            width: 100%;
            height: 3rem;
            border-radius: 12px;
            font-weight: 700;
        }
        section[data-testid="stSidebar"] {
            background: #f8fafc;
            border-right: 1px solid #e2e8f0;
        }
        div[data-testid="stDataFrame"] {
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## Controls")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    top_n = st.selectbox("Top leads", [3, 5], index=0)

    st.markdown("---")
    st.markdown("### Overview")
    st.markdown(
        """
        <div style="
            background:white;
            border:1px solid #e2e8f0;
            border-radius:14px;
            padding:14px;
            font-size:14px;
            line-height:1.8;
            color:#334155;
        ">
            • Analyze leads<br>
            • Rank opportunities<br>
            • Find best company<br>
            • Generate outreach
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### Required Data")
    st.markdown(
        """
        <div style="
            background:#fefce8;
            border:1px solid #e5e7eb;
            border-radius:14px;
            padding:14px;
            font-size:14px;
            line-height:1.8;
            color:#334155;
        ">
            company_name<br>
            website<br>
            industry
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div style="
        background:linear-gradient(135deg,#020617,#0f172a 45%,#1e293b 100%);
        padding:28px;
        border-radius:22px;
        color:white;
        margin-bottom:18px;
        box-shadow:0 10px 24px rgba(0,0,0,0.16);
    ">
        <div style="font-size:40px;font-weight:900;line-height:1.15;margin-bottom:10px;">
            AI Growth Agent for Startup Outreach
        </div>
        <div style="font-size:17px;color:#dbeafe;max-width:850px;line-height:1.6;">
            Analyze startup leads, prioritize the highest-value opportunities, and generate personalized outreach in seconds.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if uploaded_file is None:
    st.info("Upload your CSV from the left sidebar to generate insights.")
    st.stop()

try:
    source_df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"Could not read the CSV file: {e}")
    st.stop()

required_columns = {"company_name", "website", "industry"}
if not required_columns.issubset(source_df.columns):
    st.error("CSV must contain these columns: company_name, website, industry")
    st.stop()

source_df = source_df.copy()
source_df["company_name"] = source_df["company_name"].astype(str).str.strip()
source_df["website"] = source_df["website"].astype(str).str.strip()
source_df["industry"] = source_df["industry"].astype(str).str.strip()

if "results_df" not in st.session_state:
    st.session_state.results_df = None

preview_df = source_df.copy()
preview_df.index = preview_df.index + 1
preview_df.insert(0, "Lead No.", preview_df.index)

with st.expander("Preview uploaded leads", expanded=False):
    st.dataframe(preview_df, use_container_width=True, hide_index=True)

if st.button("🚀 Generate Lead Intelligence"):
    progress_bar = st.progress(0)
    status_text = st.empty()

    company_records = source_df[["company_name", "website", "industry"]].to_dict(orient="records")

    try:
        status_text.info("Analyzing all companies comparatively...")
        analyzed = analyze_companies(company_records)

        progress_bar.progress(0.5)

        company_lookup = {
            normalize_key(row["company_name"]): row
            for _, row in source_df.iterrows()
        }

        cleaned_results = []
        seen = set()

        for item in analyzed:
            company_name = str(item.get("company_name", "")).strip()
            key = normalize_key(company_name)

            if not company_name or key not in company_lookup or key in seen:
                continue

            lookup_row = company_lookup[key]

            raw_score = item.get("score", -1)
            try:
                score_num = int(raw_score)
            except Exception:
                score_num = -1

            cleaned_results.append(
                {
                    "Company": lookup_row["company_name"],
                    "Industry": lookup_row["industry"],
                    "Website": lookup_row["website"],
                    "Score": f"{score_num}/10" if score_num >= 0 else "N/A",
                    "Score_num": float(score_num),
                    "Summary": str(item.get("summary", "No summary generated")).strip(),
                    "Reason": str(item.get("reason", "No reason generated")).strip(),
                    "Message": str(item.get("message", "No outreach message generated")).strip(),
                }
            )
            seen.add(key)

        # fill any missing companies once, without duplicating anything
        missing_rows = []
        for _, row in source_df.iterrows():
            key = normalize_key(row["company_name"])
            if key not in seen:
                missing_rows.append(
                    {
                        "Company": row["company_name"],
                        "Industry": row["industry"],
                        "Website": row["website"],
                        "Score": "5/10",
                        "Score_num": 5.0,
                        "Summary": f"{row['company_name']} is a company in the {row['industry']} space.",
                        "Reason": "Added as a fallback because the model did not return a valid unique result for this company.",
                        "Message": f"Hi {row['company_name']} team, I’d love to explore whether there may be a relevant collaboration opportunity with your business.",
                    }
                )

        results = cleaned_results + missing_rows

        if not results:
            raise Exception("No valid analysis results were returned.")

        results_df = (
            pd.DataFrame(results)
            .drop_duplicates(subset=["Company"], keep="first")
            .sort_values(by=["Score_num", "Company"], ascending=[False, True])
            .reset_index(drop=True)
        )

        results_df["Rank"] = results_df.index + 1
        results_df["Lead No."] = results_df.index + 1

        results_df = results_df[
            ["Rank", "Lead No.", "Company", "Industry", "Website", "Score", "Score_num", "Summary", "Reason", "Message"]
        ]

        st.session_state.results_df = results_df
        results_df.to_csv("output/results.csv", index=False)
        progress_bar.progress(1.0)
        status_text.success("Lead intelligence generation completed.")

    except Exception as e:
        st.error(str(e))
        st.stop()

if st.session_state.results_df is None:
    st.stop()

df = st.session_state.results_df.copy()
valid_df = df[df["Score_num"] >= 0].copy()
top = valid_df.head(top_n).copy()

if valid_df.empty:
    st.warning("No valid results to display.")
    st.stop()

best = valid_df.iloc[0]

avg_score = valid_df["Score_num"].mean()
strong_leads = int((valid_df["Score_num"] >= 7).sum())

st.markdown("## Executive Overview")
st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4, gap="large")

with c1:
    metric_card("Total Leads", str(len(df)), "Analyzed")

with c2:
    metric_card("Avg Score", f"{avg_score:.1f}/10", "Quality")

with c3:
    metric_card("Strong Leads", str(strong_leads), "7+ score")

with c4:
    metric_card("Industries", str(valid_df["Industry"].nunique()), "Covered")

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
st.markdown("## Top Opportunities")
st.caption("Comparative ranking based on market potential, B2B value, scalability, and outreach fit")
st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

card_cols = st.columns(3, gap="large")
for col, (_, row) in zip(card_cols, top.head(3).iterrows()):
    with col:
        lead_card(
            rank=int(row["Rank"]),
            company=row["Company"],
            industry=row["Industry"],
            score=row["Score"],
            summary=row["Summary"],
        )

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
st.markdown("## Best Opportunity to Contact First")
st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.markdown(
        f"""
        <div style="
            background:#ecfdf5;
            padding:18px;
            border-radius:18px;
            border:1px solid #bbf7d0;
            min-height:220px;
        ">
            <div style="font-size:12px;color:#15803d;font-weight:800;letter-spacing:0.5px;margin-bottom:10px;">
                TOP PRIORITY LEAD
            </div>
            <div style="font-size:30px;font-weight:900;color:#111827;margin-bottom:8px;">
                {best['Company']}
            </div>
            <div style="font-size:14px;color:#334155;font-weight:700;margin-bottom:14px;">
                {best['Industry']} • {best['Score']}
            </div>
            <div style="font-size:15px;color:#374151;line-height:1.7;margin-bottom:14px;">
                {short_text(best['Reason'], 170)}
            </div>
            <div style="
                background:white;
                border:1px solid #bbf7d0;
                color:#166534;
                padding:10px 12px;
                border-radius:12px;
                font-size:14px;
                font-weight:700;
            ">
                Suggested action: Start outreach with {best['Company']} first.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        f"""
        <div style="
            background:white;
            padding:18px;
            border-radius:16px;
            border:1px solid #e2e8f0;
            min-height:220px;
            display:flex;
            flex-direction:column;
        ">
            <div style="
                font-size:13px;
                color:#64748b;
                font-weight:700;
                margin-bottom:10px;
            ">
                Outreach message
            </div>
            <div style="
                font-size:14px;
                color:#334155;
                line-height:1.7;
            ">
                {best['Message']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
st.markdown("## Priority Shortlist")
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

for _, row in top.iterrows():
    st.markdown(
        f"""
        <div style="
            padding:14px 16px;
            border:1px solid #e2e8f0;
            border-radius:14px;
            margin-bottom:10px;
            background:linear-gradient(135deg,#ffffff,#f8fafc);
            font-size:14px;
            display:flex;
            justify-content:space-between;
            align-items:center;
            box-shadow:0 4px 10px rgba(0,0,0,0.04);
        ">
            <div style="max-width:80%;">
                <div style="font-weight:700;color:#0f172a;">
                    {int(row['Rank'])}. {row['Company']} — {row['Score']}
                </div>
                <div style="margin-top:4px;">
                    <a href="{row['Website']}" target="_blank" style="color:#2563eb;text-decoration:none;">
                        {row['Website']}
                    </a>
                </div>
            </div>
            <div style="
                font-size:12px;
                background:#e2e8f0;
                padding:6px 12px;
                border-radius:999px;
                font-weight:600;
                color:#334155;
                white-space:nowrap;
            ">
                {row['Industry']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

csv_data = valid_df.drop(columns=["Score_num"]).to_csv(index=False).encode("utf-8")

col1, col2 = st.columns([1, 2])

with col1:
    st.download_button(
        label="⬇️ Download Shortlist CSV",
        data=csv_data,
        file_name="lead_results.csv",
        mime="text/csv",
    )

with col2:
    st.markdown(
        "<div style='padding-top:12px;color:#64748b;font-size:13px;'>"
        "A full copy is also saved locally as output/results.csv"
        "</div>",
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)
