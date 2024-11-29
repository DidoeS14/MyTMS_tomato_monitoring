
![MyTM (1)](https://github.com/user-attachments/assets/ff4bedad-c931-448e-9edd-254b712df7d8)


# Tomato Monitoring System 👀 ➡️ 🍅🌿

#### Project Overview 🔎
This project utilizes YOLOv11 to detect tomatoes in video files or video streams.
It combines state-of-the-art object detection for 2024 with intelligent processing
to identify diseased tomatoes, determine tomato maturity, and provide actionable insights
for farmers and agricultural specialists. The system is flexible, highly configurable,
and designed for deployment on devices such as the
[Jetson Nano](https://developer.nvidia.com/embedded/jetson-nano),
where the model weights were trained using [Ultralytics](https://github.com/ultralytics/ultralytics)
and [YOLOv11](https://docs.ultralytics.com/models/yolo11/).

---
### Showcase  📺
![Showcase](https://github.com/user-attachments/assets/f7e9491c-3204-48ab-a5ed-f023bff192ce)



## 🧰 Features 

1. Disease Detection:

- Detects tomato diseases using two dedicated detectors.
- If a disease is detected with confidence above given value, it:
    - Writes the finding to a database.
    - Sends an alert to user via email.
 
2. Tomato State Analysis:

- Identifies the growth state of tomatoes (e.g., ripe, unripe).
- Stores state information in the database.
- Sends an email alert if there are more than n grown (ripe) tomatoes ready for harvest, based on confidence threshold x.

3. Harvest Estimation:
- Provides a basic estimation of when the next batch of grown tomatoes is expected.
4. Data Visualization:

- Generates and displays charts based on the analysis results.
5. Flexible Input Options:

- Works with video files, video streams, and static images (with minor configuration changes).
6. Configurable Settings:

- Adjustable parameters in the `config.ini` file for thresholds, email notifications, and other options.

7. Pre-trained Weights:

- Model weights are available in the [Releases](https://github.com/DidoeS14/tomato_monitoring/releases) section.
- Trained on a dedicated Jetson Nano using YOLOv11 and Ultralytics frameworks.
- Datasets used for training are in the  References section at the end of this file.


---
## 🔧 Installation and Setup 

1. Clone the Repository

```bash
  git clone https://github.com/DidoeS14/tomato_monitoring.git
  cd tomato_monitoring

```

 2. Install Dependencies: Ensure Python 3.x and pip are installed. Then, install the required libraries:
 ```bash
 pip install -r requirements.txt
 ```
 3. Download Model Weights:
  - Access the pre-trained weights from the [Releases](https://github.com/DidoeS14/tomato_monitoring/releases) section.
  - Place the downloaded weights in a `weights/` directory.

  4. Configure Settings
  - Create the `config.ini` following the example from `config.ini.example` or check the example [here](https://github.com/DidoeS14/tomato_monitoring/blob/main/config.ini.example).
  - You can find a table with description for each parameter in the config file [here](https://github.com/DidoeS14/tomato_monitoring/blob/main/CONFIG.md)
  - Edit the `config.ini` file to adjust parameters such as confidence thresholds, alert settings, path to weights and other operational configurations.
  5. Run the system:
  ```bash
  py main.py
  ```

---
## 🗃️ Database 

You can find a .sql file inside `/database` folder, which will execute the DDL statement
(query) that will build all MySQL tables with their respective columns and types for you.
<br>
## 👾 Models 
- Classes in **tomato stage** model:
  - `b_green`
  - `b_half_ripened`
  - `b_fully_ripened`
  - `l_green`
  - `l_half_ripened`
  - `l_fully_ripened`
<br>
<br>

#### Tomato stage metrics:


mAP: 68.1% ‎ ‎ ‎ ‎ ‎ ‎ ‎ 🟪🟪🟪🟪🟪🟪🟪🟪⬜⬜<br>
Precision: 71.2% 🟦🟦🟦🟦🟦🟦🟦🟦🟦⬜<br>
Recall: 63.2% ‎ ‎ ‎ ‎ ‎ 🟧🟧🟧🟧🟧🟧🟧⬜⬜⬜<br>
<br>
**Note:** "b" and "l" in the class names stands for the rough physical size of the tomato, `b` standing for _big_
and `l` standing for _little_.
<br>
<br>
- Classes in **tomato disease** model:
  - `Healthy`
  - `Bacterial Spot`
  - `Early Blight`
  - `Iron Deficiency`
  - `Late Blight`
  - `Lead Mold`
  - `Leaf_Miner`
  - `Mosaic Virus`
  - `Septoria`
  - `Spider Mites`
  - `Yellow Leaf Curl Virus`

<br>

#### Tomato disease metrics:<br>


mAP: 50% ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ 🟪🟪🟪🟪🟪⬜⬜⬜⬜⬜<br>
Precision: 45.6% 🟦🟦🟦🟦🟦⬜⬜⬜⬜⬜<br>
Recall: 43.4% ‎ ‎ ‎ ‎ ‎ 🟧🟧🟧🟧⬜⬜⬜⬜⬜⬜<br>

## 💡 Quick Testing 

In case you want to test the system quick without connecting to database or setting an ftp server, you can simply 
 turn them off from the `config.ini` file. Instructions for how to use the parameters in the config file you can 
find [here](https://github.com/DidoeS14/tomato_monitoring/blob/main/CONFIG.md).

---
## 📔 Usage 

1. Disease Detection:
- The system prioritizes detecting diseases first.
- A confidence threshold x determines if the disease alert process is triggered. Usually confidence should be 80% (0.8f). State analysis is not performed if disease is detected.

2. Tomato State Analysis:
- If no diseases are found, the system evaluates tomato maturity.
- Alerts are sent if the number of ripe tomatoes exceeds the given count of x.

3. Harvest Prediction:
- Post-analysis, the system estimates when the next batch of tomatoes will mature.It's important to be noted that it's really rouigh estimation, requires future improvement!

4. Visualization:
- Video stream can be watched in real time
- Images with detections can be saved and later viewed
- Charts from the data can be saved and later viewed

---
  # 🔗 References 
  - [Ultralytics](https://github.com/ultralytics/ultralytics)
  - [Tomato Stages Dataset](https://datasetninja.com/laboro-tomato)
  - [Tomato Disease Dataset](https://universe.roboflow.com/universitas-atma-jaya/tomato-leaf-disease-rxcft)

