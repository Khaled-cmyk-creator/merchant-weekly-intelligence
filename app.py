
import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# Merchant Weekly Intelligence — simple one-merchant MVP
# Uses the representative merchant results from the POC.
# No live bank data and no LLM/API are used in this version.
# ---------------------------------------------------------

st.set_page_config(
    page_title="Merchant Weekly Intelligence",
    page_icon="📊",
    layout="wide"
)

# Representative merchant snapshot from the analysis
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

# -------------------------
# Header
# -------------------------

st.title("Merchant Weekly Intelligence")
st.caption(
    "A simple weekly view built from payment data • "
    f"Representative merchant snapshot: {SNAPSHOT_DATE}"
)

st.info(
    "POC demo using a public synthetic payment dataset. "
    "Values are shown in the dataset's original currency."
)

# -------------------------
# 1. What changed?
# -------------------------

st.subheader("1. What changed?")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Sales", f"+{sales_change:.1f}%", "vs previous 4 weeks")
c2.metric("Transactions", f"+{transactions_change:.1f}%", "vs previous 4 weeks")
c3.metric("Average ticket", f"+{avg_ticket_change:.1f}%", "vs previous 4 weeks")
c4.metric("Sales", f"+{sales_yoy_change:.1f}%", "vs same period last year")

st.caption(
    "Recent growth came mainly from higher transaction volume rather than "
    "a major increase in average ticket."
)

# -------------------------
# 2. Next 4 weeks
# -------------------------

st.divider()
st.subheader("2. What should I expect next?")

left, right = st.columns([1, 2])

with left:
    st.metric(
        "Next 4 weeks forecast",
        f"{forecast_4w_sales:.1f}K",
        f"{forecast_change:.1f}% vs recent 4 weeks"
    )
    st.success(forecast_status)

with right:
    forecast_df = pd.DataFrame({
        "Period": ["Previous 4 weeks", "Recent 4 weeks", "Next 4 weeks forecast"],
        "Sales (000s)": [previous_4w_sales, recent_4w_sales, forecast_4w_sales]
    }).set_index("Period")

    st.bar_chart(forecast_df, use_container_width=True)

# -------------------------
# 3. Relationship health
# -------------------------

st.divider()
st.subheader("3. Are my regular payment relationships healthy?")

r1, r2, r3 = st.columns(3)

r1.metric("Previous-period card retention", f"{retention_rate:.1f}%")
r2.metric("Active cards", f"{active_cards:,}")
r3.metric("Sales from active regular cards", f"{regular_sales_share:.1f}%")

st.caption(
    "Cards are anonymous payment-card relationships, not verified unique customers. "
    "One person may use more than one card."
)

segments = pd.DataFrame({
    "Card group": ["Active regular cards", "Less recent cards", "Occasional cards"],
    "Share of cards": [30.8, 46.2, 23.0],
    "Share of sales": [67.8, 28.6, 3.6]
})

st.dataframe(
    segments,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Share of cards": st.column_config.ProgressColumn(
            "Share of cards", min_value=0, max_value=100, format="%.1f%%"
        ),
        "Share of sales": st.column_config.ProgressColumn(
            "Share of sales", min_value=0, max_value=100, format="%.1f%%"
        ),
    }
)

# -------------------------
# 4. Payment health
# -------------------------

st.divider()
st.subheader("4. Is anything going wrong in payments?")

p1, p2 = st.columns(2)

p1.metric(
    "Payment error rate",
    f"{payment_error_rate:.1f}%",
    f"{payment_error_rate - previous_error_rate:+.1f} pp vs previous period"
)

p2.metric(
    "Refund rate",
    f"{refund_rate:.1f}%"
)

st.caption(
    "Payment health is broadly stable in this representative snapshot. "
    "Refunds are estimated from negative transaction amounts in the POC dataset."
)

# -------------------------
# Merchant Insights Assistant
# -------------------------

st.divider()
st.subheader("Merchant Insights Assistant")
st.caption(
    "The assistant explains calculated facts only. "
    "It does not invent causes, identify individual cards, or give financial advice."
)

questions = [
    "What deserves my attention this week?",
    "What changed?",
    "What should I expect next?",
    "How healthy are my regular payment relationships?",
    "Is anything going wrong in payments?"
]

question = st.selectbox("Choose a question", questions)

if st.button("Ask", type="primary"):
    if question == "What changed?":
        answer = (
            f"Sales increased {sales_change:.1f}% versus the previous 4 weeks. "
            f"Transactions increased {transactions_change:.1f}% and average ticket "
            f"increased {avg_ticket_change:.1f}%. Sales are {sales_yoy_change:.1f}% "
            f"above the same period last year."
        )

    elif question == "What should I expect next?":
        answer = (
            f"The next 4-week card-sales forecast is about {forecast_4w_sales:.1f}K, "
            f"which is {abs(forecast_change):.1f}% below the recent 4 weeks. "
            f"The forecast remains within this merchant's usual historical range."
        )

    elif question == "How healthy are my regular payment relationships?":
        answer = (
            f"Previous-period card retention is {retention_rate:.1f}%. "
            f"There are {active_cards:,} active cards in the recent 4 weeks. "
            f"Active regular cards account for about {regular_sales_share:.1f}% "
            f"of trailing-12-month card sales."
        )

    elif question == "Is anything going wrong in payments?":
        answer = (
            f"The payment error rate is {payment_error_rate:.1f}%, compared with "
            f"{previous_error_rate:.1f}% in the previous period. "
            f"The refund rate is {refund_rate:.1f}%. Payment health is broadly stable."
        )

    else:
        answer = (
            f"Sales increased {sales_change:.1f}% versus the previous 4 weeks, "
            f"mainly because transactions increased {transactions_change:.1f}%. "
            f"The next 4 weeks are forecast at about {forecast_4w_sales:.1f}K and "
            f"remain within the merchant's usual historical range. "
            f"Previous-period card retention is {retention_rate:.1f}%, while "
            f"payment errors are broadly stable at {payment_error_rate:.1f}%."
        )

    st.write(answer)

st.divider()
st.caption(
    "MVP scope: one representative established merchant. "
    "Next version can connect these same components to outputs for all eligible merchants."
)
