import streamlit as st
import pandas as pd
import numpy as np

from main import run_apriori, data_from_file, results_to_sring

st.markdown("# Apriori Algorithm")
st.markdown('Apriori adalah sebuah algoritma yang digunakan untuk menemukan pola dalam data. Algoritma ini digunakan untuk menemukan pola dalam data transaksi.')

used_csv = 'dataset.csv'

st.markdown('Contoh sample dataset: ')
csv_file = pd.read_csv(used_csv, nrows=2, header=None)
st.write(csv_file.head())

st.markdown('---')
st.markdown('## Inputs')
st.markdown('''
    **Minimum Support** adalah nilai minimum yang digunakan untuk menentukan item yang sering muncul dalam data transaksi.

    **Minimum Confidence** adalah nilai minimum yang harus dipenuhi untuk menentukan asosiasi antara dua item.
''')

support_helper = ''' > Support(A) = (Number of transactions in which A appears)/(Total Number of Transactions') '''
confidence_helper = ''' > Confidence(A->B) = Support(AUB)/Support(A)') '''
st.markdown('---')

support = st.slider("Masukkan nilai support minimum", min_value=0.00001,
                    max_value=0.9, value=0.01,
                    help=support_helper)

confidence = st.slider("Masukkan nilai confidence minimum", min_value=0.00001,
                       max_value=0.9, value=0.5, help=confidence_helper)

inFile = data_from_file(used_csv)

items, rules = run_apriori(inFile, support, confidence)

i, r = results_to_sring(items, rules)

st.markdown("## Results")

st.markdown("### Frequent Itemsets")
st.write(i)

st.markdown("### Frequent Rules")
st.write(r)