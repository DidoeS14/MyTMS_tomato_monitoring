# Configuration File Explanation

This document describes the purpose and usage of each section and setting in the provided configuration file. The file is used to manage the behavior of the tomato monitoring system.

## **[model]** 👾
| Setting               | Description                                                                                   |
|-----------------------|-----------------------------------------------------------------------------------------------|
| `size_model`          | Path to the model weights used for detecting the size or ripeness of tomatoes.                |
| `disease_model`       | Path to the model weights used for detecting tomato diseases.                                 |
| `size_confidence`     | Confidence threshold for the size/ripeness detection model. Default: `0.6`.                   |
| `disease_confidence`  | Confidence threshold for the disease detection model. Default: `0.8`.                         |
| `size_ripened_count`  | Minimum number of ripened tomatoes required to trigger an alert for gathering. Default: `10`. |
| `input`               | Path to the input video or stream file for processing. Default: `test_tomato.mp4`.            |
| `output`              | Directory to save the processed results. Default: `test_results`.                             |
| `detection_cooldown`  | Time interval between consecutive detections (in seconds). Default: `25`.                     |
| `use_minutes`         | Boolean to treat `detection_cooldown` as minutes when `True`. Default: `False`.               |
| `show_stream`         | Boolean indicating whether to display the video stream. Default: `True`.                      |
| `save_images`         | Boolean to save detection images to the output folder. Default: `False`.                      |

---

## **[chart]** 📊
| Setting     | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| `output`    | Directory to save results used for generating charts. Default: `test_results`. |
| `subdir`    | Subdirectory within the output folder to save charts. Default: `charts`.    |
| `save`      | Boolean to enable or disable saving charts. Default: `False`.               |

---

## **[email]** 📧
| Setting      | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| `smtp_server`| The SMTP server for sending emails. Default: `smtp.gmail.com`.              |
| `port`       | Port number for the SMTP server. Recommended: `587` for secure connections. |
| `sender`     | Email address sending the alerts.                                           |
| `password`   | Password for the sender's email account. **Remove before sharing code.**    |
| `receiver`   | Recipient email address for receiving alerts.                               |

---

##  **[database]** 📚
| Setting      | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| `host`       | Database server address. Default: `localhost`.                              |
| `port`       | Port number for connecting to the database. Default: `3307`.                |
| `name`       | Name of the database to use. Default: `tomato`.                             |
| `username`   | Username for accessing the database. Default: `root`.                       |
| `password`   | Password for the database user. Default: `123456`.                          |
| `use_database`| Boolean to enable or disable using the database. Default: `False`.         |

---

## **[ftp]** 📤
| Setting     | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| `server`    | Address of the FTP server. Default: `0.0.0.0`.                              |
| `user`      | Username for the FTP server. Default: `user`.                               |
| `port`      | Port number for the FTP connection. Default: `2121`.                        |
| `password`  | Password for the FTP user. Default: `123456`.                               |
| `use_ftp`   | Boolean to enable or disable using the FTP server. Default: `False`.        |
