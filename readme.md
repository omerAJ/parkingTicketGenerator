# People Counting

## Project Aim
The aim of this project is to develop a robust system for counting vehicles passing a road using advanced computer vision techniques. The code works on saved vids and RTSP stream. This involves using the YOLOv8 model to detect and track vehicles in video feeds. The project focuses on accurately counting the number of vehicles crossing a predefined line, making it applicable for scenarios such as traffic monitoring.


## Project Overview
The primary goal of this repository is to implement a vehicle counting system using the YOLOv8 object detection model from Ultralytics. The model is trained on personal labeled data [can be locally found in D://omer//vehicle counting//data], the datasets are not extencive, hence the system is not robust. The conclusion we came to is that to deploy the model for any application we would first need to deploy the camera, collect some data, label it, finetune the model. 


## Table of Contents
- [Project Overview](#project-overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Detection](#detection)
  - [Training](#training)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

## Getting Started

### Prerequisites
- Python
- YOLOv8 (Ultralytics)

### Installation
1. Clone the repository:
git clone https://github.com/omerAJ/vehicleCounting.git
cd vehickeCounting

2. Install required Python libraries:
pip install -r requirements.txt


## Usage

### Detection

- **detect and count on stream**
  - Use the provided script in Scripts/count.py to run the YOLOv8 model on RTSP stream. This script loads the pre-trained YOLOv8 model and applies it to detect and count vehicles in the stream, it tracks the detected vehicles across frames and counts how many cross a predefined line in the video feed. Adjust the line coordinates in the script based on your specific requirements. The counts are only displayed on stream right now, but they can easily be stored in a db or csv for future reference.

- **Count and collect GT**
  - In addition to detect and count this code can be used to collect GT counts to evaluate performance of model. As you watch the video, the model counts are automatically incremented and you can use key presses to count the actual vehicle classes in/out, adjust the key:value mappings based on your classes.

### Training

#### Dataset

There are many publicly available datasets for vehicle classification, but each are very small and specialized. I have trained on multiple combinations of these and availed no luck for a robust and generalizable model. The best bet right now is to finetune on a small but good quality dataset from the site of deployment like we did with traffic cams.

#### Training

- use train.py to train the model, provide it path to the data.yaml file and select the model you want to train.

#### Pre-trained weights

- all pretrained models are saved in D://omer/YOLO_weights

## Acknowledgements
- This project was done at Centre for Urban Informatics, Technology, and Policy (CITY @ LUMS)

