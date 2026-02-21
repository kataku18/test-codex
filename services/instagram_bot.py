from __future__ import annotations

from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


class InstagramAutoPoster:
    def __init__(self, headless: bool = True):
        self.headless = headless

    def login_and_post(self, username: str, password: str, caption: str, image_path: Path) -> dict:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=self.headless)
            context = browser.new_context()
            page = context.new_page()

            try:
                page.goto('https://www.instagram.com/accounts/login/', wait_until='domcontentloaded')
                page.get_by_label('Phone number, username, or email').fill(username)
                page.get_by_label('Password').fill(password)
                page.get_by_role('button', name='Log in').click()

                page.wait_for_timeout(5000)
                page.goto('https://www.instagram.com/', wait_until='domcontentloaded')
                page.get_by_label('New post').click(timeout=15000)

                page.set_input_files("input[type='file']", str(image_path))
                page.get_by_role('button', name='Next').click()
                page.get_by_role('button', name='Next').click()
                page.get_by_label('Write a caption...').fill(caption)
                page.get_by_role('button', name='Share').click()
                page.wait_for_timeout(5000)
            except PlaywrightTimeoutError as exc:
                return {'posted': False, 'message': f'Instagram UI timeout: {exc}'}
            except Exception as exc:
                return {'posted': False, 'message': f'Automation failed: {exc}'}
            finally:
                context.close()
                browser.close()

        return {'posted': True, 'message': 'Posted successfully.'}
