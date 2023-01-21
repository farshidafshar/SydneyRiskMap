# SydneyRiskMap
In this I have stored my codes in developing risk map for Sydney crash prediction model via ERT and OrderedForest models 
## What is in there!?
There are three jupyter notebooks and one .py file which is a Streamlit app to play around with inputs.

## Data
CrashData: Thanks to transport for NSW the crash data is available at here : https://opendata.transport.nsw.gov.au/dataset/nsw-crash-data
GeoJson: Through osmnx it is easy peasy : ox.graph_from_place('Sydney, NSW', network_type='drive')

## Models
ERT: a scikit learn ensemble model that according to documentation :" is a meta estimator that fits a number of randomized decision trees (a.k.a. extra-trees) on various sub-samples of the dataset and uses averaging to improve the predictive accuracy and control over-fitting."

OrderedForest: "flexibly estimates the conditional probabilities of models with ordered categorical outcomes (so-called ordered choice models)." https://arxiv.org/abs/1907.02436

## Map&App
Maps are generated using Folium and Geopandas (probably a heaven-made combination).
App is a simple Streamlit product with a few filters.
