import argparse
import json
import logging
import logging.handlers as handlers
import random
import sys
from pathlib import Path
from typing import List, Dict

from src.Browser import Browser
from src.DailySet import DailySet
from src.Login import Login
from src.MorePromotions import MorePromotions
from src.PunchCards import PunchCards
from src.Searches import Searches
from src.constants import VERSION
from src.loggingColoredFormatter import ColoredFormatter
from src.notifier import Notifier

class MicrosoftRewardsFarmer:
    def __init__(self, args: argparse.Namespace, notifier: Notifier):
        self.args = args
        self.notifier = notifier
        self.accounts = self.load_accounts()
        self.setup_logging()

    def setup_logging(self):
        log_format = "%(asctime)s [%(levelname)s] %(message)s"
        log_dir = Path(__file__).resolve().parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        terminal_handler = logging.StreamHandler(sys.stdout)
        terminal_handler.setFormatter(ColoredFormatter(log_format))

        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                handlers.TimedRotatingFileHandler(
                    log_dir / "activity.log",
                    when="midnight",
                    interval=1,
                    backupCount=2,
                    encoding="utf-8",
                ),
                terminal_handler,
            ],
        )

    def load_accounts(self) -> List[Dict[str, str]]:
        account_path = Path(__file__).resolve().parent / "accounts.json"
        if not account_path.exists():
            account_path.write_text(
                json.dumps(
                    [{"username": "Your Email", "password": "Your Password"}], indent=4
                ),
                encoding="utf-8",
            )
            logging.warning(
                "[ACCOUNT] 'accounts.json' not found. A template has been created. "
                "Please fill it with your credentials."
            )
            sys.exit()

        with account_path.open(encoding="utf-8") as f:
            accounts = json.load(f)
        
        random.shuffle(accounts)
        return accounts

    def execute_bot(self):
        for account in self.accounts:
            self.process_account(account)

    def process_account(self, account: Dict[str, str]):
        logging.info(f"Processing account: {account.get('username', '')}")
        try:
            self.run_tasks(account)
        except Exception as e:
            logging.exception(f"Error with account {account.get('username', '')}: {e}")

    def run_tasks(self, account: Dict[str, str]):
        points_counter = 0
        with Browser(mobile=False, account=account, args=self.args) as browser:
            points_counter = self.perform_tasks(browser, points_counter)

        self.notify_points(account, points_counter)

    def perform_tasks(self, browser: Browser, starting_points: int) -> int:
        current_points = Login(browser).login()
        logging.info(f"Starting with {browser.utils.formatNumber(current_points)} points")

        DailySet(browser).completeDailySet()
        PunchCards(browser).completePunchCards()
        MorePromotions(browser).completeMorePromotions()

        remaining_searches, remaining_mobile_searches = browser.utils.getRemainingSearches()

        if remaining_searches:
            current_points = Searches(browser).bingSearches(remaining_searches)

        if remaining_mobile_searches:
            browser.closeBrowser()
            with Browser(mobile=True, account=browser.account, args=self.args) as mobile_browser:
                Login(mobile_browser).login()
                current_points = Searches(mobile_browser).bingSearches(remaining_mobile_searches)

        points_earned = current_points - starting_points
        logging.info(f"Points earned today: {browser.utils.formatNumber(points_earned)}")
        logging.info(f"Total points: {browser.utils.formatNumber(current_points)}")
        return current_points

    def notify_points(self, account: Dict[str, str], points: int):
        message = (
            f"Microsoft Rewards Farmer\n"
            f"Account: {account.get('username', '')}\n"
            f"Total points: {points}"
        )
        self.notifier.send(message)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Microsoft Rewards Farmer")
    parser.add_argument("-v", "--visible", action="store_true", help="Optional: Visible browser")
    parser.add_argument("-l", "--lang", type=str, default=None, help="Optional: Language (e.g., en)")
    parser.add_argument("-g", "--geo", type=str, default=None, help="Optional: Geolocation (e.g., US)")
    parser.add_argument("-p", "--proxy", type=str, default=None, help="Optional: Global Proxy")
    parser.add_argument("-t", "--telegram", metavar=("TOKEN", "CHAT_ID"), nargs=2, type=str, default=None, help="Optional: Telegram Bot Token and Chat ID")
    parser.add_argument("-d", "--discord", type=str, default=None, help="Optional: Discord Webhook URL")
    return parser.parse_args()

def main():
    args = parse_arguments()
    notifier = Notifier(args)
    farmer = MicrosoftRewardsFarmer(args, notifier)
    farmer.execute_bot()

if __name__ == "__main__":
    main()
