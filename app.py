
import streamlit as st
import pandas as pd
import altair as alt

# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(
    page_title="Merchant Weekly Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# DESIGN SYSTEM — aligned with the presentation
# ============================================================

DEEP_GREEN = "#07583B"
MID_GREEN = "#168A5B"
LIGHT_GREEN = "#EAF4EE"
SOFT_GREEN = "#DCEEE4"
PALE_GREEN = "#BFDCCB"
OFF_WHITE = "#F8FAF7"
TEXT = "#183029"
MUTED = "#56665F"
AMBER = "#C8892B"
LIGHT_AMBER = "#FFF5E6"
BORDER = "#DDE7E1"

st.markdown(
    f"""
    <style>
        .stApp {{
            background: {OFF_WHITE};
            color: {TEXT};
        }}

        .block-container {{
            max-width: 1120px;
            padding-top: 1rem;
            padding-bottom: 2.5rem;
        }}

        h1, h2, h3 {{
            color: {DEEP_GREEN};
            letter-spacing: -0.02em;
        }}

        h1 {{
            font-weight: 800;
        }}

        h2 {{
            font-weight: 750;
            margin-top: 1.1rem;
        }}

        p, div, span, label {{
            line-height: 1.42;
        }}

        /* Smaller hero */
        .hero {{
            background: {DEEP_GREEN};
            color: white;
            border-radius: 20px;
            padding: 24px 30px 22px 30px;
            margin-bottom: 20px;
        }}

        .hero-kicker {{
            font-size: 0.72rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: #BED8CA;
            font-weight: 800;
            margin-bottom: 5px;
        }}

        .hero-title {{
            font-size: 2rem;
            line-height: 1.08;
            font-weight: 800;
            margin: 0;
            color: white;
        }}

        .hero-subtitle {{
            margin-top: 6px;
            color: #E7F0EB;
            font-size: 0.96rem;
        }}

        .hero-meta {{
            margin-top: 12px;
            display: inline-block;
            background: rgba(255,255,255,0.10);
            border: 1px solid rgba(255,255,255,0.16);
            border-radius: 999px;
            padding: 5px 10px;
            font-size: 0.79rem;
            color: white;
        }}

        .section-kicker {{
            display: inline-block;
            background: {SOFT_GREEN};
            color: {DEEP_GREEN};
            border-radius: 999px;
            padding: 5px 10px;
            text-transform: uppercase;
            letter-spacing: 0.085em;
            font-size: 0.68rem;
            font-weight: 800;
            margin-bottom: 6px;
        }}

        /* Tighter insight cards */
        .insight-card {{
            background: {LIGHT_GREEN};
            border: 1px solid {BORDER};
            border-radius: 15px;
            padding: 16px 18px;
            min-height: 112px;
            margin-bottom: 10px;
        }}

        .insight-card.good {{
            border-left: 5px solid {MID_GREEN};
        }}

        .insight-card.neutral {{
            border-left: 5px solid {DEEP_GREEN};
        }}

        .insight-card.warn {{
            background: {LIGHT_AMBER};
            border-left: 5px solid {AMBER};
        }}

        .insight-label {{
            color: {DEEP_GREEN};
            font-weight: 800;
            font-size: 0.92rem;
            margin-bottom: 4px;
        }}

        .insight-big {{
            color: {DEEP_GREEN};
            font-size: 1.55rem;
            font-weight: 800;
            line-height: 1.05;
            margin-bottom: 6px;
        }}

        .insight-copy {{
            color: {TEXT};
            font-size: 0.90rem;
        }}

        .status-pill {{
            display: inline-block;
            margin-top: 7px;
            background: {SOFT_GREEN};
            color: {DEEP_GREEN};
            border-radius: 999px;
            padding: 5px 9px;
            font-size: 0.76rem;
            font-weight: 800;
        }}

        .assistant-intro {{
            background: white;
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 15px 17px;
            margin-bottom: 10px;
        }}

        .assistant-badge {{
            display: inline-block;
            background: {DEEP_GREEN};
            color: white;
            border-radius: 999px;
            padding: 4px 9px;
            font-size: 0.70rem;
            font-weight: 800;
            margin-bottom: 6px;
        }}

        .assistant-copy {{
            color: {TEXT};
            font-size: 0.91rem;
        }}

        .chat-shell {{
            background: white;
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 12px 14px 6px 14px;
            margin-top: 8px;
            margin-bottom: 8px;
        }}

        div.stButton > button {{
            border-radius: 999px;
            border: 1px solid {DEEP_GREEN};
            color: {DEEP_GREEN};
            background: white;
            font-weight: 700;
            padding: 0.42rem 0.8rem;
            min-height: 2.35rem;
        }}

        div.stButton > button:hover {{
            background: {LIGHT_GREEN};
            border-color: {MID_GREEN};
            color: {DEEP_GREEN};
        }}

        div[data-testid="stForm"] {{
            border: 0;
            padding: 0;
        }}

        [data-testid="stChatMessage"] {{
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 0.15rem 0.4rem;
            margin-bottom: 0.45rem;
            background: white;
        }}

        details {{
            background: white;
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 4px 10px;
        }}

        /* Improve muted text contrast */
        .stCaption, [data-testid="stCaptionContainer"] {{
            color: {MUTED} !important;
        }}

        /* Hide Streamlit chrome */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# REPRESENTATIVE MERCHANT DATA FROM THE POC
# ============================================================

SNAPSHOT_DATE = "6 Oct 2019"

sales_change = 11.8
transactions_change = 10.2
avg_ticket_change = 1.4
sales_yoy_change = 1.3

previous_4w_sales = 25.011
recent_4w_sales = 27.797
forecast_4w_sales = 27.140
forecast_change = -2.9
forecast_status = "Within your usual historical range"

retention_rate = 32.2
active_cards = 421
regular_sales_share = 67.8

payment_error_rate = 1.6
previous_error_rate = 1.4
refund_rate = 0.0

# ============================================================
# HERO
# ============================================================

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-kicker">Merchant intelligence · weekly briefing</div>
        <div class="hero-title">Merchant Weekly Intelligence</div>
        <div class="hero-subtitle">Your weekly payment-data briefing.</div>
        <div class="hero-meta">Week ending {SNAPSHOT_DATE} · POC demo</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# THIS WEEK AT A GLANCE
# ============================================================

st.markdown('<div class="section-kicker">Weekly briefing</div>', unsafe_allow_html=True)
st.subheader("This week at a glance")

c1, c2 = st.columns(2, gap="medium")

with c1:
    st.markdown(
        f"""
        <div class="insight-card good">
            <div class="insight-label">What changed?</div>
            <div class="insight-big">Sales +{sales_change:.1f}%</div>
            <div class="insight-copy">
                Driven mainly by <b>{transactions_change:.1f}% more transactions</b>.
                Average ticket changed <b>{avg_ticket_change:.1f}%</b>.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="insight-card neutral">
            <div class="insight-label">4-week outlook</div>
            <div class="insight-big">{forecast_4w_sales:.1f}K</div>
            <div class="insight-copy">
                <b>{abs(forecast_change):.1f}% below</b> the recent four weeks.
            </div>
            <div class="status-pill">{forecast_status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div class="insight-card neutral">
            <div class="insight-label">Regular payment activity</div>
            <div class="insight-big">{regular_sales_share:.1f}% of sales</div>
            <div class="insight-copy">
                Active regular cards generate most sales.
                <b>{retention_rate:.1f}%</b> of previous-period cards returned.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="insight-card neutral">
            <div class="insight-label">Payment health</div>
            <div class="insight-big">Broadly stable</div>
            <div class="insight-copy">
                Errors: <b>{payment_error_rate:.1f}%</b>
                (previously {previous_error_rate:.1f}%).
                Refunds: <b>{refund_rate:.1f}%</b>.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# SALES TREND + OUTLOOK
# ============================================================

st.markdown('<div class="section-kicker">Outlook</div>', unsafe_allow_html=True)
st.subheader("Sales trend and 4-week outlook")

chart_df = pd.DataFrame(
    {
        "Period": [
            "Previous 4 weeks",
            "Recent 4 weeks",
            "Next 4 weeks\nForecast",
        ],
        "Sales": [
            previous_4w_sales,
            recent_4w_sales,
            forecast_4w_sales,
        ],
        "Label": [
            f"{previous_4w_sales:.1f}K",
            f"{recent_4w_sales:.1f}K",
            f"{forecast_4w_sales:.1f}K",
        ],
        "Type": ["Actual", "Actual", "Forecast"],
    }
)

bar = (
    alt.Chart(chart_df)
    .mark_bar(cornerRadiusTopLeft=7, cornerRadiusTopRight=7)
    .encode(
        x=alt.X(
            "Period:N",
            sort=[
                "Previous 4 weeks",
                "Recent 4 weeks",
                "Next 4 weeks\nForecast",
            ],
            title=None,
            axis=alt.Axis(
                labelAngle=0,
                labelColor=MUTED,
                labelFontSize=12,
                labelPadding=8,
            ),
        ),
        y=alt.Y(
            "Sales:Q",
            title="Card sales (000s)",
            axis=alt.Axis(
                titleColor=MUTED,
                labelColor=MUTED,
            ),
            scale=alt.Scale(zero=True),
        ),
        color=alt.Color(
            "Type:N",
            scale=alt.Scale(
                domain=["Actual", "Forecast"],
                range=[MID_GREEN, PALE_GREEN],
            ),
            legend=alt.Legend(
                title=None,
                orient="top-right",
            ),
        ),
        tooltip=[
            alt.Tooltip("Period:N", title="Period"),
            alt.Tooltip("Sales:Q", title="Card sales", format=".1f"),
            alt.Tooltip("Type:N", title="Type"),
        ],
    )
)

labels = (
    alt.Chart(chart_df)
    .mark_text(
        dy=-12,
        fontSize=14,
        fontWeight="bold",
        color=DEEP_GREEN,
    )
    .encode(
        x=alt.X(
            "Period:N",
            sort=[
                "Previous 4 weeks",
                "Recent 4 weeks",
                "Next 4 weeks\nForecast",
            ],
        ),
        y="Sales:Q",
        text="Label:N",
    )
)

chart = (
    (bar + labels)
    .properties(height=285)
    .configure_view(strokeWidth=0)
    .configure_axis(
        gridColor="#E6ECE8",
        domain=False,
        tickSize=0,
    )
)

st.altair_chart(chart, use_container_width=True)

# ============================================================
# MERCHANT INSIGHTS ASSISTANT
# ============================================================

st.markdown('<div class="section-kicker">Experiential AI interface</div>', unsafe_allow_html=True)
st.subheader("Merchant Insights Assistant")

st.markdown(
    """
    <div class="assistant-intro">
        <div class="assistant-badge">MERCHANT INSIGHTS</div>
        <div class="assistant-copy">
            Ask about this week's performance, the 4-week outlook,
            regular payment activity, or payment health.
            The assistant explains calculated facts only.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

def merchant_answer(prompt: str) -> str:
    q = prompt.lower().strip()

    if (
        "attention" in q
        or "summary" in q
        or ("this week" in q and "changed" not in q)
    ):
        return (
            f"Sales increased {sales_change:.1f}% versus the previous four weeks, "
            f"mainly because transactions increased {transactions_change:.1f}%. "
            f"The next four weeks are forecast at about {forecast_4w_sales:.1f}K "
            f"and remain within the merchant's usual historical range. "
            f"Active regular cards generate about {regular_sales_share:.1f}% of sales. "
            f"Payment health is broadly stable."
        )

    if (
        "changed" in q
        or "change" in q
        or "sales" in q
        or "transactions" in q
        or "ticket" in q
    ):
        return (
            f"Sales increased {sales_change:.1f}% versus the previous four weeks. "
            f"Transactions increased {transactions_change:.1f}%, while average ticket "
            f"increased only {avg_ticket_change:.1f}%. "
            f"So the recent sales increase came mainly from higher transaction volume. "
            f"Sales are also {sales_yoy_change:.1f}% above the same period last year."
        )

    if (
        "expect" in q
        or "forecast" in q
        or "outlook" in q
        or "next" in q
        or "future" in q
    ):
        return (
            f"The next four weeks are forecast at about {forecast_4w_sales:.1f}K "
            f"in card sales. That is {abs(forecast_change):.1f}% below the recent "
            f"four weeks, but the forecast remains within this merchant's usual "
            f"historical range. This is a forecast, not a certainty."
        )

    if (
        "regular" in q
        or "return" in q
        or "card" in q
        or "relationship" in q
        or "retention" in q
        or "customer" in q
    ):
        return (
            f"Active regular cards generate about {regular_sales_share:.1f}% of sales. "
            f"{retention_rate:.1f}% of cards seen in the previous four weeks were "
            f"seen again in the recent four weeks, and there are {active_cards:,} "
            f"active cards in the recent period. "
            f"These are payment-card relationships, not verified unique customers."
        )

    if (
        "payment" in q
        or "error" in q
        or "refund" in q
        or "issue" in q
        or "wrong" in q
    ):
        return (
            f"Payment health is broadly stable. The payment error rate is "
            f"{payment_error_rate:.1f}% versus {previous_error_rate:.1f}% in the "
            f"previous period. The recent refund rate is {refund_rate:.1f}%. "
            f"No refund issue is visible in this snapshot."
        )

    return (
        "I can explain four things from the current payment-data analysis: "
        "what changed, the next four-week outlook, regular payment activity, "
        "and payment health. I do not have evidence in this POC to explain "
        "external causes such as inventory, marketing, competitors, or economic events."
    )

def submit_prompt(prompt_text: str):
    prompt_text = prompt_text.strip()
    if not prompt_text:
        return

    st.session_state.messages.append(
        {"role": "user", "content": prompt_text}
    )

    st.session_state.messages.append(
        {"role": "assistant", "content": merchant_answer(prompt_text)}
    )

    # Keep only the latest 3 user/assistant exchanges = 6 messages.
    st.session_state.messages = st.session_state.messages[-6:]

# Quick prompts — 2x2 to avoid truncation
q1, q2 = st.columns(2)
with q1:
    if st.button("What changed?", use_container_width=True):
        submit_prompt("What changed?")
        st.rerun()
with q2:
    if st.button("4-week outlook?", use_container_width=True):
        submit_prompt("What should I expect next?")
        st.rerun()

q3, q4 = st.columns(2)
with q3:
    if st.button("Regular cards?", use_container_width=True):
        submit_prompt("How important are regular cards?")
        st.rerun()
with q4:
    if st.button("Payment issues?", use_container_width=True):
        submit_prompt("Are there any payment issues?")
        st.rerun()

# Conversation + input kept together
st.markdown('<div class="chat-shell">', unsafe_allow_html=True)

if not st.session_state.messages:
    with st.chat_message("assistant", avatar="💬"):
        st.write("What would you like to know about your business this week?")
else:
    for message in st.session_state.messages:
        avatar = "●" if message["role"] == "user" else "💬"
        with st.chat_message(message["role"], avatar=avatar):
            st.write(message["content"])

with st.form("merchant_chat_form", clear_on_submit=True):
    input_col, send_col = st.columns([8, 1])
    with input_col:
        typed_prompt = st.text_input(
            "Ask about your business this week",
            placeholder="Ask about your business this week...",
            label_visibility="collapsed",
        )
    with send_col:
        send = st.form_submit_button(
            "Send",
            use_container_width=True,
        )

    if send and typed_prompt.strip():
        submit_prompt(typed_prompt)
        st.rerun()

clear_col, spacer = st.columns([1, 5])
with clear_col:
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

st.caption(
    "The assistant does not invent causes, identify individual cards, "
    "give financial advice, or present forecasts as certainty."
)

# ============================================================
# DETAILS — SECONDARY, COLLAPSED BY DEFAULT
# ============================================================

with st.expander("Explore details"):

    st.markdown("### What changed?")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Sales", f"+{sales_change:.1f}%", "vs previous 4 weeks")
    m2.metric("Transactions", f"+{transactions_change:.1f}%", "vs previous 4 weeks")
    m3.metric("Average ticket", f"+{avg_ticket_change:.1f}%", "vs previous 4 weeks")
    m4.metric("Sales vs last year", f"+{sales_yoy_change:.1f}%")

    st.markdown("### Regular payment activity")

    r1, r2, r3 = st.columns(3)

    r1.metric("Cards returning from previous period", f"{retention_rate:.1f}%")
    r2.metric("Active cards", f"{active_cards:,}")
    r3.metric("Sales from active regular cards", f"{regular_sales_share:.1f}%")

    segment_df = pd.DataFrame(
        {
            "Card group": [
                "Active regular cards",
                "Less recent cards",
                "Occasional cards",
            ],
            "Share of cards": [30.8, 46.2, 23.0],
            "Share of sales": [67.8, 28.6, 3.6],
        }
    )

    long_segments = segment_df.melt(
        id_vars="Card group",
        value_vars=["Share of cards", "Share of sales"],
        var_name="Measure",
        value_name="Share",
    )

    segment_chart = (
        alt.Chart(long_segments)
        .mark_bar(cornerRadiusEnd=4)
        .encode(
            y=alt.Y(
                "Card group:N",
                title=None,
                sort=[
                    "Active regular cards",
                    "Less recent cards",
                    "Occasional cards",
                ],
            ),
            x=alt.X("Share:Q", title="Share (%)"),
            yOffset="Measure:N",
            color=alt.Color(
                "Measure:N",
                scale=alt.Scale(
                    domain=["Share of cards", "Share of sales"],
                    range=["#A9D4BE", DEEP_GREEN],
                ),
                legend=alt.Legend(title=None, orient="top"),
            ),
            tooltip=[
                "Card group:N",
                "Measure:N",
                alt.Tooltip("Share:Q", format=".1f"),
            ],
        )
        .properties(height=235)
        .configure_view(strokeWidth=0)
        .configure_axis(
            gridColor="#E6ECE8",
            domain=False,
            tickSize=0,
        )
    )

    st.altair_chart(segment_chart, use_container_width=True)

    st.markdown("### Payment details")

    p1, p2 = st.columns(2)

    p1.metric(
        "Payment error rate",
        f"{payment_error_rate:.1f}%",
        f"{payment_error_rate - previous_error_rate:+.1f} pp vs previous period",
        delta_color="inverse",
    )

    p2.metric("Refund rate", f"{refund_rate:.1f}%")

    st.caption(
        "Cards represent anonymous payment-card relationships, not verified unique "
        "customers. Refunds are estimated from negative transaction amounts in this POC."
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.caption(
    "POC demo using a public synthetic payment dataset. "
    "The assistant is limited to calculated payment-data facts and model outputs."
)
