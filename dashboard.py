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

import lunch_money

logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()


def run(args):
    df = pd.read_csv('meal_history.csv')
    df['Date'] = pd.to_datetime(df['Date'])

    students = students_list(df)

    db_title = 'MySchoolBucks Personal Dashboard'

    st.markdown(
        "<h1 style='text-align: center;'>{}</h1>".format(db_title),
        unsafe_allow_html=True
    )

    update_button = st.button('Update Report Data')

    if update_button:
        update_report_data()

    balance_col, buffer, payments_col = st.columns([50, 3, 50])
    with balance_col:
        st.markdown("<h3 style='text-align: left'>Current Balances</h3>", unsafe_allow_html=True)
        st.markdown(current_balances(df, students), unsafe_allow_html=True)

    with payments_col:
        st.markdown("<h3 style='text-align: left'>Account Total Deposits</h3>", unsafe_allow_html=True)
        st.altair_chart(payments(df), use_container_width=True)

    st.markdown("---", unsafe_allow_html=True)

    st.markdown("<br><h3 style='text-align: left'>Daily Purchase Totals</h3>", unsafe_allow_html=True)
    buffer, student_dropdown, buffer = st.columns([1, 200, 1])
    with student_dropdown:
        dropdown_key = st.selectbox("Students", [''] + students)

    buffer, report, buffer = st.columns([1, 200, 1])
    with report:
        if dropdown_key != '':
            st.altair_chart(purchases(df, dropdown_key), use_container_width=True)
        else:
            st.write('Please select a student to view purchases report')


def students_list(data):
    student_list = data["Student"].unique().tolist()

    return student_list


def current_balances(data, students):
    md_table_header = '| {} | {} | {} | {} |'.format("Student", "Date", "Time", "Balance")
    md_table_body_data = []

    for s in students:
        first_name = s.split(' ')[1]

        filtered_df = data[data["Student"] == s]
        s_current_df = filtered_df.iloc[filtered_df["Date"].argmax()]
        date_value = s_current_df["Date"].strftime('%m/%d')
        time_value = s_current_df["Date"].strftime('%H:%M %p')
        s_balance = '${:,.2f}'.format(s_current_df["Balance"])

        if s_current_df["Balance"] <= 3:
            balance = '{} :rotating_light:'.format(s_balance)
        elif 3 < s_current_df["Balance"] <= 6:
            balance = '{} :warning:'.format(s_balance)
        else:
            balance = s_balance

        md_table_body_data.append('| {} | {} | {} | {} |'.format(
            first_name,
            date_value,
            time_value,
            balance)
        )

    md_table = '{}\n|:--------|:--------|:--------|:-------:|\n{}'.format(
        md_table_header,
        "\n".join(md_table_body_data)
    )

    return md_table


def purchases(data, student):
    filtered_df = data[(data["Student"] == student) & (data["Payment Method"] != 'Online Payment')]
    purchases = filtered_df.loc[:, ('Date', 'Item', 'Amount')]

    purchases["Date"] = purchases["Date"].dt.date
    purchases["Amount"] = purchases["Amount"].apply(lambda x: x * -1)

    purchases.sort_values(by=['Date', 'Item'], ascending=[False, True]).reset_index()

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


def payments(data):
    filtered_df = data[data["Payment Method"] != 'Online Payment']
    payments = filtered_df.loc[:, ('Student', 'Amount')]

    payments["Amount"] = payments["Amount"].apply(lambda x: x * -1)
    payments["Student"] = payments["Student"].apply(lambda x: x.split(' ')[1])

    grouped_df = payments.groupby(["Student"]).sum().reset_index()

    bar_chart = alt.Chart(grouped_df).mark_bar().encode(
        x=alt.X('Student', axis=alt.Axis(format="", title='')),
        y=alt.Y('Amount', axis=alt.Axis(format="$.3", title='Amount')),
        color='Student'
    )

    return bar_chart


def update_report_data():
    print('Updating Report')
    lunch_money()


def main():
    parser = argparse.ArgumentParser(description='Builds dashboard based on MySchoolBucks account transactions')
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
