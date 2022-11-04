#!/usr/bin/env python3
###########################################################
#
###########################################################
import argparse
import logging
import streamlit as st


logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()


def run(args):
    db_title = 'MySchoolBucks Personal Dashboard'

    st.markdown(
        "<h1 style='text-align: center;'>{}</h1>".format(db_title),
        unsafe_allow_html=True
    )


def main():
    parser = argparse.ArgumentParser(description='Builds dashboard based on MySchoolBucks account transactions')
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
