
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Merchant Weekly Intelligence",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------------
# Representative merchant snapshot from the POC
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.title("Merchant Weekly Intelligence")
st.caption(f"Week ending {SNAPSHOT_DATE}")

# ---------------------------------------------------------
# Weekly attention summary
# ---------------------------------------------------------
st.subheader("What needs attention this week?")

c1, c2 = st.columns(2)

with c1:
    st.success(
        f"**Sales increased {sales_change:.1f}%** vs previous 4 weeks  \n"
        f"Mainly driven by **{transactions_change:.1f}% more transactions**; "
        f"average ticket changed only **{avg_ticket_change:.1f}%**."
    )

    st.info(
        f"**4-week outlook: {forecast_4w_sales:.1f}K**  \n"
        f"{forecast_status}. "
        f"Forecast is **{abs(forecast_change):.1f}% below** the recent 4 weeks."
    )

with c2:
    st.info(
        f"**Regular payment activity remains important**  \n"
        f"Active regular cards generate about **{regular_sales_share:.1f}% of sales**. "
        f"Returning-card rate: **{retention_rate:.1f}%**."
    )

    st.info(
        f"**Payments are broadly stable**  \n"
        f"Error rate: **{payment_error_rate:.1f}%** "
        f"(previous period: {previous_error_rate:.1f}%). "
        f"Refund rate: **{refund_rate:.1f}%**."
    )

# ---------------------------------------------------------
# Simple trend + forecast chart
# ---------------------------------------------------------
st.subheader("Sales trend and 4-week outlook")

chart_df = pd.DataFrame({
    "Period": ["Previous 4 weeks", "Recent 4 weeks", "Next 4 weeks"],
    "Sales": [previous_4w_sales, recent_4w_sales, forecast_4w_sales],
    "Label": [f"{previous_4w_sales:.1f}K",
              f"{recent_4w_sales:.1f}K",
              f"{forecast_4w_sales:.1f}K"]
})

base = alt.Chart(chart_df).encode(
    x=alt.X(
        "Period:N",
        sort=["Previous 4 weeks", "Recent 4 weeks", "Next 4 weeks"],
        title=None,
        axis=alt.Axis(labelAngle=0)
    ),
    y=alt.Y("Sales:Q", title="Card sales (000s)")
)

bars = base.mark_bar().encode(
    tooltip=[
        alt.Tooltip("Period:N"),
        alt.Tooltip("Sales:Q", format=".1f")
    ]
)

labels = base.mark_text(dy=-10, fontSize=14).encode(
    text="Label:N"
)

st.altair_chart(
    (bars + labels).properties(height=300),
    use_container_width=True
)

# ---------------------------------------------------------
# Ask Merchant Insights — moved up
# ---------------------------------------------------------
st.subheader("Ask Merchant Insights")

question = st.selectbox(
    "Choose a question",
    [
        "What deserves my attention this week?",
        "What changed?",
        "What should I expect next?",
        "How healthy is my regular payment activity?",
        "Are there any payment issues?"
    ],
    label_visibility="collapsed"
)

if st.button("Ask", type="primary"):
    if question == "What changed?":
        answer = (
            f"Sales increased {sales_change:.1f}% versus the previous 4 weeks. "
            f"Transactions increased {transactions_change:.1f}%, while average ticket "
            f"increased only {avg_ticket_change:.1f}%. Sales are {sales_yoy_change:.1f}% "
            f"above the same period last year."
        )
    elif question == "What should I expect next?":
        answer = (
            f"The next 4-week card-sales forecast is about {forecast_4w_sales:.1f}K. "
            f"This is {abs(forecast_change):.1f}% below the recent 4 weeks, "
            f"but still {forecast_status.lower()}."
        )
    elif question == "How healthy is my regular payment activity?":
        answer = (
            f"Active regular cards account for about {regular_sales_share:.1f}% of sales. "
            f"The returning-card rate is {retention_rate:.1f}%, with {active_cards:,} "
            f"active cards in the recent 4 weeks."
        )
    elif question == "Are there any payment issues?":
        answer = (
            f"Payment health is broadly stable. The error rate is {payment_error_rate:.1f}% "
            f"versus {previous_error_rate:.1f}% previously. "
            f"The refund rate is {refund_rate:.1f}%."
        )
    else:
        answer = (
            f"Sales increased {sales_change:.1f}% versus the previous 4 weeks, mainly "
            f"because transactions increased {transactions_change:.1f}%. "
            f"The next 4 weeks are forecast at about {forecast_4w_sales:.1f}K and remain "
            f"within the merchant's usual historical range. "
            f"Regular payment activity generates about {regular_sales_share:.1f}% of sales, "
            f"while payment health remains broadly stable."
        )
    st.write(answer)

# ---------------------------------------------------------
# Details — hidden unless merchant wants them
# ---------------------------------------------------------
with st.expander("Explore details"):

    st.markdown("### What changed?")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Sales", f"+{sales_change:.1f}%", "vs previous 4 weeks")
    m2.metric("Transactions", f"+{transactions_change:.1f}%", "vs previous 4 weeks")
    m3.metric("Average ticket", f"+{avg_ticket_change:.1f}%", "vs previous 4 weeks")
    m4.metric("Sales vs last year", f"+{sales_yoy_change:.1f}%")

    st.markdown("### Regular payment activity")
    r1, r2, r3 = st.columns(3)
    r1.metric("Returning-card rate", f"{retention_rate:.1f}%")
    r2.metric("Active cards", f"{active_cards:,}")
    r3.metric("Sales from active regular cards", f"{regular_sales_share:.1f}%")

    segments = pd.DataFrame({
        "Card group": ["Active regular cards", "Less recent cards", "Occasional cards"],
        "Share of cards": [30.8, 46.2, 23.0],
        "Share of sales": [67.8, 28.6, 3.6]
    })

    seg_long = segments.melt(
        id_vars="Card group",
        value_vars=["Share of cards", "Share of sales"],
        var_name="Measure",
        value_name="Share"
    )

    seg_chart = alt.Chart(seg_long).mark_bar().encode(
        y=alt.Y("Card group:N", title=None),
        x=alt.X("Share:Q", title="Share (%)"),
        xOffset="Measure:N",
        color=alt.Color("Measure:N", legend=alt.Legend(title=None)),
        tooltip=[
            "Card group:N",
            "Measure:N",
            alt.Tooltip("Share:Q", format=".1f")
        ]
    ).properties(height=220)

    st.altair_chart(seg_chart, use_container_width=True)

    st.markdown("### Payment details")
    p1, p2 = st.columns(2)
    p1.metric(
        "Payment error rate",
        f"{payment_error_rate:.1f}%",
        f"{payment_error_rate - previous_error_rate:+.1f} pp vs previous period",
        delta_color="inverse"
    )
    p2.metric("Refund rate", f"{refund_rate:.1f}%")

    st.caption(
        "Cards represent anonymous payment-card relationships, not verified unique customers. "
        "Refunds are estimated from negative transaction amounts in this POC dataset."
    )

st.caption(
    "POC demo using a public synthetic payment dataset. "
    "The assistant explains calculated facts only and does not invent causes or give financial advice."
)
