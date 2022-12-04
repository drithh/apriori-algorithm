Simple Python Implementation of Apriori Algorithm

Live Demo in streamlit  
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]()

This is a simple implementation of Apriori algorithm in Python. The algorithm is implemented in a way that it can be used for any dataset. The dataset used in this implementation is the one provided in kaggle. The dataset can be found here. [https://www.kaggle.com/irfanasrullah/groceries](https://www.kaggle.com/irfanasrullah/groceries)

To run the program with dataset provided and default values for _minSupport_ = 0.001 and _minConfidence_ = 0.5

    python main.py -f dataset.csv

To run program with dataset

    python main.py -f dataset.csv -s 0.17 -c 0.69
