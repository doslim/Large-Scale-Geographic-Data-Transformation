# Large Scale Geographic Data Transformation

![](https://visitor-badge.glitch.me/badge?page_id=Doslim.Large-Scale-Geographic-Data-Transformation)

In this repository, we provide a solution to transform large scale geographic data based on the [Geoencoding API](https://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding) provided by Baidu Map. 

Our task is to query the  corresponding GPS corrdinates of addresses from different provinces in China. The original data are around 50M and stored in 31 files with different length. Since each individual account can only call the API no more than 300K times, we design a plan to finish this task within a reasonable time. More details can be found in our brief report.

## Data
The data used in this project is extracted from a database about Chinese enterprises. We do not provide the raw data due to the privacy concerns. But our plan can be adapted to other scenarios that require a lot of transformations.

## Project Structure and Environments

All codes are written in Python 3.8 . No special packages are needed.

The structure of our project is as follows.
- main.py: the entrance of our codes.
- utils.py: define several tools to load the data and the core function to call the API.
- data\_split\_merge.ipynb: group, segment the data and merge data after transformation.
- config.yaml: store the configurations.
- main.sh: the script to run the code.
- data: contain all the data (empty due to privacy concerns)
    - original\_data: path to load the original data.
    - transformed\_data: path to store the transformed data.
    - logs: path to save logs.
    - error\_info: path to save error information.
- output\_log: path to save the output to the screen when running our codes.

We provide some logs generated by our codes.

## Usage

To use our code, you first need to collect AKs for the API. And then use the code in data\_split.ipynb to prepare the data but some slight modifications are needed. The tools defined in utils.py should be adjusted according to your task. Our report could provide some guidence.
