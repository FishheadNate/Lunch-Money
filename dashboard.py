#!/usr/bin/env python3
###########################################################
# Processes the CSV export of lunch-money.py and builds an
# interactive dashboard to view the results.
###########################################################
import altair as alt
import argparse
import logging
import pandas as pd
import streamlit as st

logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()


def run(args):
    db_title = 'MySchoolBucks Personal Dashboard'
    st.markdown(
        "<h1 style='text-align: center;'>{}</h1>".format(db_title),
        unsafe_allow_html=True
    )
    st.markdown("---", unsafe_allow_html=True)

    if args.demo:
        msb_csv = 'demo/demo_data.csv'
    else:
        msb_csv = 'meal_history.csv'

    try:
        df = pd.read_csv(msb_csv)
        df['Date'] = pd.to_datetime(df['Date'])

        students = students_list(df)

        balance_col, buffer, payments_col = st.columns([50, 3, 50])
        with balance_col:
            st.markdown("<h3 style='text-align: left'>Current Balances</h3>", unsafe_allow_html=True)
            st.markdown(current_balance(df, students), unsafe_allow_html=True)

        with payments_col:
            st.markdown("<h3 style='text-align: left'>Account Total Deposits</h3>", unsafe_allow_html=True)
            st.altair_chart(payments(df), use_container_width=True)
        st.markdown("---", unsafe_allow_html=True)

        st.markdown("<h3 style='text-align: left'>Daily Purchase Totals</h3>", unsafe_allow_html=True)
        buffer, student_dropdown, buffer = st.columns([1, 200, 1])
        with student_dropdown:
            dropdown_key = st.selectbox("Student", [''] + students)

        buffer, report, buffer = st.columns([1, 200, 1])
        with report:
            if dropdown_key != '':
                st.altair_chart(purchases(df, dropdown_key), use_container_width=True)
                st.markdown(meal_days(df, dropdown_key), unsafe_allow_html=True)
            else:
                st.write('Please select a student to report')

    except IOError:
        st.write('MySchoolBucks data is missing. Please run `lunch_money.py` and refresh the dashboard.')


def students_list(data):
    student_list = data["Student"].unique().tolist()

    return student_list


def current_balance(data, students):
    md_table_header = '| {} | {} | {} | {} |'.format("Student", "Date", "Time", "Balance")
    md_table_body_data = []

    for s in students:
        first_name = s.split(' ')[1]

        balances = data.loc[data["Student"] == s, ['Date', 'Balance']]
        current_balance = balances.iloc[balances["Date"].argmax()]
        balance_date = current_balance["Date"].strftime('%m/%d')
        balance_time = current_balance["Date"].strftime('%H:%M %p')
        balance_formatted = '${:,.2f}'.format(current_balance["Balance"])

        if current_balance["Balance"] <= 3:
            balance = '{} :rotating_light:'.format(balance_formatted)
        elif 3 < current_balance["Balance"] <= 6:
            balance = '{} :warning:'.format(balance_formatted)
        else:
            balance = balance_formatted

        md_table_body_data.append('| {} | {} | {} | {} |'.format(
            first_name,
            balance_date,
            balance_time,
            balance)
        )

    md_table = '{}\n|:--------|:--------|:--------|:-------:|\n{}'.format(
        md_table_header,
        "\n".join(md_table_body_data)
    )

    return md_table


def payments(data):
    payments = data.loc[data["Payment Method"] != 'Online Payment', ['Student', 'Amount']]

    payments["Amount"] = payments["Amount"].apply(lambda x: x * -1)
    payments["Student"] = payments["Student"].apply(lambda x: x.split(' ')[1])

    grouped_df = payments.groupby(["Student"]).sum().reset_index()

    bar_chart = alt.Chart(grouped_df).mark_bar().encode(
        x=alt.X('Student', axis=alt.Axis(format="", title='')),
        y=alt.Y('Amount', axis=alt.Axis(format="$.3", title='Amount')),
        color='Student'
    )

    return bar_chart


def purchases(data, student):
    purchases = data.loc[(data["Student"] == student) & (data["Payment Method"] != 'Online Payment'), ['Date', 'Item', 'Amount']]
    purchases["Date"] = purchases["Date"].dt.date
    purchases["Amount"] = purchases["Amount"].apply(lambda x: x * -1)

    area_chart = alt.Chart(purchases).mark_bar(
        line=True
    ).encode(
        x=alt.X('Date', axis=alt.Axis(format="", title='Date')),
        y=alt.Y('sum(Amount)', scale=alt.Scale(domain=(0, 6)), axis=alt.Axis(format="$.2f", title='Amount')),
        color='Item'
    ).properties(
        width='container',
        height=400
    )

    return area_chart


def meal_days(data, student):
    md_table_header = '| {} | {} |'.format("Meal Type", "Total Count")
    md_table_body_data = []

    meal_days = data.loc[(data["Student"] == student) & (data["Payment Method"] != 'Online Payment'), ['Date', 'Student', 'Item', 'Amount']]
    meal_days["Date"] = meal_days["Date"].dt.date

    grouped_df = meal_days.groupby('Item')["Date"].nunique().reset_index()

    for i in list(grouped_df["Item"].unique()):
        meal_type = i
        meal_count = grouped_df.loc[grouped_df["Item"] == i, 'Date'].item()

        md_table_body_data.append('| {} | {} |'.format(
            meal_type,
            meal_count)
        )

    md_table = '{}\n|:--------|:-------:|\n{}'.format(
        md_table_header,
        "\n".join(md_table_body_data)
    )

    return md_table


def main():
    parser = argparse.ArgumentParser(description='Builds dashboard based on MySchoolBucks account transactions')
    parser.add_argument('--demo', help='Run dashboard on demo data', dest='demo', default=False, action='store_true', required=False)
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
