# Python Projects Repository

This repository contains a collection of Python projects developed for coursework and practice.
The projects cover **AI (Search & ML)**, **Communication / Signal Processing**, **Cryptography**, and **Python automation in Linux-style workflows**.

---

## 📌 Projects Overview

- **AI Project 1:** Delivery routing optimization using **Genetic Algorithm** and **Simulated Annealing**.
- **AI Project 2:** Natural scene **image classification** (Forest / Mountain / Sea) using **Naive Bayes**, **Decision Tree**, and **Neural Network (MLP)** with **PCA**.
- **Communication Project:** Audio **demodulation** and **modulation** (inverse process) to demonstrate communication system concepts.
- **Cryptography Task 1:** Cryptanalysis of **A5 stream cipher** using **known-plaintext attack** and brute-force state recovery.
- **Cryptography Task 2:** **AES modes analysis** (ECB vs CBC): pattern exposure (images), CBC error propagation, and avalanche effect.
- **Python & Linux Automation:** Processing daily invoices from a text file (file parsing + automation workflow).

---

## 1) AI Project 1 — Delivery Optimization (Search & Optimization)

### Description
This project solves a **delivery routing / optimization** problem using AI search techniques.
The goal is to find an **optimal or near-optimal** delivery route that minimizes a cost (e.g., distance/time/total cost).

### Techniques
- **Genetic Algorithm (GA)**
- **Simulated Annealing (SA)**

### What it does
- Loads delivery data
- Generates candidate solutions (routes)
- Evaluates solutions using a cost function
- Improves solutions iteratively using GA and SA
- Compares the quality of results between both approaches

### Key Concepts
- Heuristic optimization
- Cost function evaluation
- Solution generation and improvement
- Comparative analysis of metaheuristics

### Files (example structure)
- `AI_Project/main.py`
- `AI_Project/delivery_data.py`
- `AI_Project/solution_generator.py`
- `AI_Project/Genetic.py`
- `AI_Project/simulated.py`
- `AI_Project/utils.py`
- `AI_Project/input.txt`
- `AI_Project/AiReport_1221003_1222600.pdf`

---

## 2) AI Project 2 — Image Classification (Machine Learning)

### Description
This project performs **supervised image classification** for natural scenes into:
- **Forest**
- **Mountain**
- **Sea**

### Models Used
- **Naive Bayes**
- **Decision Tree**
- **Feedforward Neural Network (MLP)**

### Methodology
- Preprocessing of image data
- Dimensionality reduction using **PCA**
- Training with a consistent dataset split
- Evaluation using standard classification metrics

### Evaluation Metrics
- Accuracy
- Precision
- Recall
- F1-score

### Key Concepts
- Supervised learning
- Feature reduction (PCA)
- Model comparison and analysis

### Files (example structure)
- `AI_Project_2/main.py`
- `AI_Project_2/Ai_ProjectTwoReport_1221003_1222600.pdf`

---

## 3) Communication Project — Audio Modulation & Demodulation

### Description
A communication/signal-processing project using an **audio signal**.
It demonstrates:
- **Demodulation**: recovering the original/baseband information signal
- **Modulation**: applying the inverse process (reconstructing/modulating the signal)

### What it does
- Reads/handles an audio signal
- Applies demodulation to extract the information signal
- Applies modulation as the inverse process to demonstrate the concept

### Key Concepts
- Modulation / demodulation fundamentals
- Time-domain signal processing
- Practical communication system workflow

### Files (example structure)
- `communication/project.py`
- `communication/untitled.py`

---

## 4) Cryptography Task 1 — A5 Stream Cipher Attack (Known-Plaintext)

### Description
Cryptanalysis of the **A5 stream cipher** using a **known-plaintext attack**.
The task recovers an internal cipher state (e.g., register state) and decrypts the ciphertext.

### What it does
- Uses a known plaintext segment to brute-force the internal state
- Recovers the correct cipher state
- Decrypts the full ciphertext using the recovered state

### Key Concepts
- Stream ciphers
- Known-plaintext attacks
- Brute-force state recovery
- Practical decryption workflow

### Files (example structure)
- `cryptography/A5_brute_force_y.py`
- `cryptography/A5_decrypt_full.py`
- `cryptography/ciphertext.bin`
- `cryptography/known_plaintext.txt`
- `cryptography/initial_states.txt`
- `cryptography/recovered_y_state.txt`
- `cryptography/recovered_plaintext.txt`

---

## 5) Cryptography Task 2 — AES Modes Analysis (ECB vs CBC)

### Description
An experimental analysis of **AES modes of operation** focusing on:
- **Pattern exposure** (especially on images)
- **CBC error propagation**
- **Avalanche effect**

### Experiments

#### A) Pattern Exposure (ECB vs CBC)
- Encrypting structured data/images with **ECB** reveals visible patterns
- **CBC** hides structural information and is safer for structured data

#### B) CBC Error Propagation
- Introduces bit errors into ciphertext
- Studies how decryption output is affected across blocks

#### C) Avalanche Effect
- Changes a single bit and measures output bit changes
- Demonstrates diffusion properties of AES

### Key Concepts
- AES block cipher modes
- Security weaknesses of ECB for images
- Error propagation behavior in CBC
- Avalanche effect (diffusion)

### Files (example structure)
- `cryptography/task2_aes.py`
- `cryptography/task2_pattern_exposure.py`
- `cryptography/task2_cbc_image_exposure.py`
- `cryptography/task2_cbc_error_analyses.py`
- `cryptography/task2_aes_avalanche_analysis.py`
- `cryptography/make_bw_image.py`
- `cryptography/cipher_ecb.png`
- `cryptography/pattern_output.txt`
- `cryptography/cbc_errors_output.txt`

---

## 6) Python & Linux Automation — Daily Invoices Processing

### Description
A Python scripting project that automates a Linux-style workflow by reading and processing invoice records from a text file.

### What it does
- Reads daily invoices from an input file
- Parses and processes the records
- Produces summarized/organized output based on the invoice data

### Key Concepts
- File handling and parsing
- Automation using Python scripts
- Structured processing of textual data

### Files (example structure)
- `python_linux/project.py`
- `python_linux/daily_invoices.txt`

---

## 🛠️ Technologies Used
- Python
- File handling / parsing
- Algorithms & optimization
- Machine Learning concepts (PCA, classifiers)
- Cryptography (A5, AES, modes of operation)

---

## ✅ Notes
- Folder names may differ slightly depending on your repository structure.
- If needed, update the file paths above to match your actual folder names.
