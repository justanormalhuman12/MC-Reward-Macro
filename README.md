Microsoft Rewards Farmer
A Python script that automates tasks for the Microsoft Rewards system, including logging in, completing daily sets, punch cards, and more promotions. It also tracks and notifies about the points earned.

Features
Automates Daily Tasks: Completes daily sets, punch cards, and more promotions.
Points Tracking: Keeps track of points earned and total points.
Notifications: Sends notifications via Telegram or Discord about points earned.
Configurable: Supports proxy settings, geolocation, and language options.
Requirements
Python 3.8 or higher
Browser automation tools (e.g., Selenium)
Required Python libraries (see requirements.txt)
Installation
Clone the Repository

git clone https://github.com/your-username/microsoft-rewards-farmer.git
cd microsoft-rewards-farmer

Install Dependencies

Create a virtual environment and install the required packages:

python -m venv venv
source venv/bin/activate (On Windows use venv\Scripts\activate)
pip install -r requirements.txt

Set Up Configuration

Create a accounts.json file in the root directory with the following structure:

json
Copy code
[
    {
        "username": "Your Email",
        "password": "Your Password"
    }
]
Replace "Your Email" and "Your Password" with your Microsoft Rewards account credentials.

Set Up Logging and Notifications

Modify the src/notifier.py file to implement the notification methods for Telegram and Discord if not already set up.

Usage
Run the script with the desired arguments:

python rewards_farmer.py [options]

Options
-v, --visible: Optional. Run with a visible browser window.
-l, --lang: Optional. Specify language (e.g., en for English).
-g, --geo: Optional. Specify geolocation (e.g., US).
-p, --proxy: Optional. Specify a global proxy (e.g., http://user:pass@host:port).
-t, --telegram: Optional. Provide Telegram Bot Token and Chat ID for notifications.
-d, --discord: Optional. Provide Discord Webhook URL for notifications.
Example
To run the script with Telegram notifications:

python rewards_farmer.py -t YOUR_TELEGRAM_TOKEN YOUR_CHAT_ID

Contributing
Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Make your changes.
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature/your-feature).
Create a new Pull Request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
Browser automation tools and libraries.
Microsoft Rewards system documentation (if available).
