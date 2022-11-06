#!/usr/bin/env python3
###########################################################
# Processes the CSV export of lunch-money.py and builds an
# interactive dashboard to view the results.
###########################################################
import argparse
import logging
import pandas as pd
import streamlit as st


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

    buffer, col2, buffer = st.columns([1, 10, 1])

    with col2:
        for i in students:
            st.write('{}\n\tBalance: {}'.format(i, current_balance(df, i)))

        key = st.selectbox("Student", [''] + students)

    buffer, col2 = st.columns([1, 2000])

    with col2:
        if key != '':
            filtered_df = df[df['Student'] == key]

            st.dataframe(filtered_df)
        else:
            st.write('Please select a student to view transactions')


def students_list(data):
    student_list = data["Student"].unique().tolist()

    return student_list


def current_balance(data, student):
    filtered_df = data[data['Student'] == student]
    balance = filtered_df.iloc[filtered_df["Date"].argmax()]

    return balance["Balance"]


def main():
    parser = argparse.ArgumentParser(description='Builds dashboard based on MySchoolBucks account transactions')
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
