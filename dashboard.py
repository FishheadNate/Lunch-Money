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

    db_title = 'MySchoolBucks Personal Dashboard'

    st.markdown(
        "<h1 style='text-align: center;'>{}</h1>".format(db_title),
        unsafe_allow_html=True
    )

    buffer, col2, buffer = st.columns([1, 10, 1])

    with col2:
        key = st.selectbox("Student", students(df))

    buffer, col2 = st.columns([1, 2000])

    with col2:
        if key != '':
            filtered_df = df[df['Student'] == key]
            st.dataframe(filtered_df)
        else:
            st.write('Please select a student to view transactions')


def students(data):
    student_list = [''] + data["Student"].unique().tolist()

    return student_list


def main():
    parser = argparse.ArgumentParser(description='Builds dashboard based on MySchoolBucks account transactions')
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
