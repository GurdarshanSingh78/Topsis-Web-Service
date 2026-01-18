# TOPSIS Web Service

This is a web-based application that calculates the **TOPSIS score** (Technique for Order of Preference by Similarity to Ideal Solution) for a given dataset. Users can upload a CSV/Excel file, specify weights and impacts, and receive the results via email.

**Live Demo:** [Click Here to View App](https://your-app-name.vercel.app)

## Features
* **Upload Support:** Accepts `.csv` and `.xlsx` files.
* **Dynamic Calculation:** Computes TOPSIS scores and ranks based on user-defined weights and impacts.
* **Email Integration:** Sends the processed result file directly to the user's email.
* **Sample Data:** Provides a downloadable sample file for testing.
* **Interactive UI:** Displays the result table directly on the webpage.

## How to Use
1.  **Access the Web App:** Open the live link above.
2.  **Download Sample:** Click "Download Sample CSV File" to see the required format.
3.  **Upload File:** Select your input file (must contain numeric columns for decision making).
4.  **Enter Parameters:**
    * **Weights:** Comma-separated numbers (e.g., `1,1,1,1`).
    * **Impacts:** Comma-separated signs (e.g., `+,+,-,+`).
    * **Email:** The address where you want the result file sent.
5.  **Submit:** The application processes the data, displays the result, and emails the file.

## Local Installation

If you want to run this project on your own computer:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Topsis-Web-Service.git](https://github.com/YOUR_USERNAME/Topsis-Web-Service.git)
    cd Topsis-Web-Service
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Email:**
    Open `app.py` and update the `SENDER_EMAIL` and `SENDER_PASSWORD` with your own credentials (use an App Password for Gmail).

4.  **Run the application:**
    ```bash
    python app.py
    ```

5.  **Open in Browser:**
    Go to `http://127.0.0.1:5000`

## Technologies Used
* **Python** (Backend Logic)
* **Flask** (Web Framework)
* **Pandas & NumPy** (Data Processing)
* **SMTP** (Email Service)
* **Vercel** (Deployment)

## License
[MIT](https://choosealicense.com/licenses/mit/)