# Parking Ticket Generator

## Project Aim
This project aims to automate the process of monitoring vehicles entering a parking space using YOLO-based detection models. The system identifies the vehicle class, reads the license plate, records the timestamp of entry, and generates a parking ticket for each vehicle. This system enhances parking management efficiency and accuracy.




## Project Overview
The system utilizes two YOLO models: the first detects the vehicle entering the parking space, and the second focuses on detecting the license plate and its characters. Upon successful detection and recognition, the vehicle's image, license plate details, and entry timestamp are used to generate a digital parking ticket, which can also be printed directly from the code.


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
- OpenCV

### Installation
1. Clone the repository:
git clone https://github.com/omerAJ/parkingTicketGenerator.git
cd vehicle-entry-system


2. Install required Python libraries:
pip install -r requirements.txt


## Usage

### Detection

- **models**
  - This requires 3 models, detecting vehicle class (S, M, L), finding number plate in frame, OCR of the number plate.


- **Generating and Printing Parking Tickets**
  - The code in main.ipynb can be used to generate and print the parking ticket. 

### Training

#### Dataset

The models are trained on self labelled private dataset. Can be found locally in D://omer/vehicleClassification

#### Pre-trained weights

- all pretrained models are saved in D://omer/YOLO_weights

## Acknowledgements
- This project was done at Centre for Urban Informatics, Technology, and Policy (CITY @ LUMS)

