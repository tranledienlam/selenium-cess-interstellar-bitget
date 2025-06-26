
import argparse
import tempfile
from pathlib import Path
from selenium.webdriver.common.by import By

from browser_automation import BrowserManager, Node
from utils import Utility
from w_bitget import Setup as BitgetSetup, Auto as BitgetAuto
from googl import Setup as GoogleSetup, Auto as GoogleAuto

PROJECT_URL = "https://cess.network"
GG_URL = "https://mail.google.com"

class Setup:
    def __init__(self, node: Node, profile) -> None:
        self.node = node
        self.profile = profile
        self.bitget_setup = BitgetSetup(node, profile)
        self.google_setup = GoogleSetup(node, profile)
        
    def _run(self):
        self.google_setup._run()
        self.bitget_setup._run()
        self.node.new_tab(f'{PROJECT_URL}/interstellarairdrop/?code=3043048', method="get")
        Utility.wait_time(10)

class Auto:
    def __init__(self, node: Node, profile: dict) -> None:
        self.driver = node._driver
        self.node = node
        self.profile_name = profile.get('profile_name')
        self.pwd_wallet = profile.get('pwd_wallet')
        self.email = profile.get('email')
        self.pwd_email = profile.get('pwd_email')
        self.seeds = profile.get('seeds')

        self.bitget_auto = BitgetAuto(node, profile)
        self.google_auto = GoogleAuto(node, profile)
        self.address = None

    def connect(self):
        button = self.node.find(By.CSS_SELECTOR, 'button[class*="rounded-full"]')
        if button and button.text:
            if button.text.lower() in ['Disconnect'.lower(), 'Log Out'.lower()]:
                self.node.log(f'Đã connect ví')
                return True

            elif button.text.lower() in ['Connect Wallet'.lower(), 'Log In'.lower()]:
                self.node.log(f'Cần connect ví')
                self.node.click(button)
                self.node.find_and_click(By.XPATH, '//button[p[contains(text(), "Bitget")]]')
                self.node.find_and_click(By.XPATH, '//button[contains(text(),"Accept")]')
                self.bitget_auto.confirm('connect')
                self.bitget_auto.confirm('agree')

                button = self.node.find(By.CSS_SELECTOR, 'button[class*="rounded-full"]')
                if button and button.text:
                    if button.text.lower() in ['Disconnect'.lower(), 'Log Out'.lower()]:
                        self.node.log(f'Đã connect ví')
                        return True
                else:
                    self.node.log('Button có thể đã bị thay đổi text "Connect Wallet", "Disconnect"')
                    return False
            else:
                self.node.log('Không tìm thấy button connect')
                return False
        else:
            self.node.log('Không tìm thấy button connect')
            return False

    def click_alert(self):
        Utility.wait_time(3)
        p_els = self.node.find_all(By.TAG_NAME, 'p')
        for el in p_els:
            if 'Success'.lower() == el.text.lower():
                self.node.click(el)
                return True
            elif 'Retweet error'.lower() == el.text.lower():
                self.node.click(el)
                return False
            elif 'Request limit exceeded'.lower() in el.text.lower():
                self.node.click(el)
                return False
            
    def task_visit(self, button):
        self.click_alert()
        
        if button.text.lower() != "Get Points".lower():
            current_url = self.node.get_url()
            self.node.scroll_to(button)
            self.node.click(button)
            self.node.switch_tab(current_url)

        buttons = self.node.find_all(By.TAG_NAME, 'button')
        for button in buttons:
            if button.text.lower() == "Get Points".lower():
                self.node.click(button)
                if self.click_alert():
                    return True

        return False
    
    def task_retweet(self, button):
        self.click_alert()

        current_url = self.node.get_url()
        self.node.scroll_to(button)
        self.node.click(button)
        self.node.switch_tab(current_url)

        buttons = self.node.find_all(By.TAG_NAME, 'button')
        for button in buttons:
            if button.text.lower() == "Later".lower():
                if self.node.click(button):
                    return False
                buttons = self.node.find_all(By.TAG_NAME, 'button')
        
        for button in buttons:
            if button.text.lower() == "Forwarded & Get Points".lower():
                self.node.click(button)
                if self.click_alert():
                    return True
        
    def capture_and_upload_screenshot(self):
        file_path = self.node._save_screenshot()
        if file_path is None:
            self.node.log("❌ Không thể chụp màn hình")
            return False

        try:
            file_input = self.node.find(By.ID, 'dropzone-file')
            if file_input:
                file_input.send_keys(file_path)
            self.node.log("✅ Đã gửi ảnh chụp màn hình vào input file thành công")
            Utility.wait_time(1)
            return True

        except Exception as e:
            self.node.log(f"❌ Lỗi khi gửi file vào input: {e}")
            return False

        finally:
            # Bước 4: Xóa file tạm
            if Path(file_path).exists():
                Path(file_path).unlink()
                self.node.log(f"🧹 Đã xóa ảnh tạm sau khi upload: {file_path}")

    def check_upload(self):
        p_els = self.node.find_all(By.TAG_NAME, 'p')
        for el in p_els:
            if el.text and '(error)' in el.text.lower():
                self.node.log(f'Giới hạn upload file')
                self.node.click(el)
                break

            elif 'File upload'.lower() in el.text.lower():
                self.node.click(el)
                return True
            
        return False

    def task_upload(self, button):
        success_times = 0
        self.node.scroll_to(button)
        if not self.node.click(button):
            p_els = self.node.find_all(By.TAG_NAME, 'p')
            for el in p_els:
                if 'Unlock this task after completing all social media tasks.'.lower() in el.text.lower():
                    self.node.snapshot(f'Cần hoàn thành task social để thực hiện task upload', False)
            return success_times
        
        while True:
            self.capture_and_upload_screenshot()
            if self.check_upload():
                success_times +=1
                Utility.wait_time(10)
            else:
                p_els = self.node.find_all(By.TAG_NAME, 'p')
                for el in p_els:
                    if el.text and 'back' in el.text.lower():
                        self.node.click(el)
                        break
                break

        return success_times

    def task_get_cess(self, button):
        self.node.scroll_to(button)
        self.node.new_tab(f'{PROJECT_URL}/faucet.html', method="get")
        btn_send = self.node.find(By.XPATH, '//div[contains(@class, "btn") and contains(text(), "Send Me TCESS")]',timeout=60)
        if not btn_send:
            self.node.log('Không tìm thấy button Send Me TCESS. Có thể trang chưa lload xong')
            return False

        if not self.address or not self.email:
            self.node.log('Không tìm thấy address hoặc email')
            return False
        
        self.node.find_and_input(By.CSS_SELECTOR, '[placeholder="Please enter your address"]', self.address, delay=0.1)
        self.node.find_and_input(By.CSS_SELECTOR, '[placeholder="Please enter your Email address"]', self.email, delay=0.1)
        
        self.node.find_and_click(By.XPATH, '//span[contains(text(),"Send")]')
        self.node.scroll_to(btn_send)
        code = self.google_auto.read_code('CESS Team', '(//p[contains(text(), "Your verification code")]/ancestor::div[1]/p[@style])[last()]')
        if code:
            self.node.find_and_input(By.CSS_SELECTOR, '[placeholder="Enter the authentication code"]', code, delay=0.1)
            self.node.click(btn_send)
            self.node.switch_tab(f'{PROJECT_URL}/interstellarairdrop')
            return True

        return False

    def click_check(self, button):
        self.node.scroll_to(button)
        self.node.click(button)
        return self.click_alert()

    def task_signature(self, button):
        self.node.scroll_to(button)
        self.node.click(button)
        self.bitget_auto.confirm('approve')
        if self.bitget_auto.confirm('confirm'):
            Utility.wait_time(20)
            self.click_alert()
            return True
        return False

    def _run(self):
        
        self.bitget_auto._run()
        self.bitget_auto.change_network_other('CESS Testnet')
        self.address = self.bitget_auto.address

        self.node.new_tab()
        task_google = self.google_auto._run()
        if task_google:
            self.node.go_to(f'{GG_URL}')

        self.node.new_tab(f'{PROJECT_URL}/interstellarairdrop/?code=3043048', method="get")
        
        if not self.connect():
            self.node.snapshot(f'Connect ví thất bại')

        actives = ['get points',"Forwarded & Get Points".lower(),'visit', 'retweet', 'upload']
        buttons = self.node.find_all(By.TAG_NAME, 'button')

        task_buttons = []
        for button in buttons:
            if button.text.lower() in actives:
                task_buttons.append(button)
                
        tasks_completed = []
        for task_button in task_buttons:
            if task_button.text.lower() in ['get points','visit']:
                if self.task_visit(task_button):
                    tasks_completed.append('visit')
            elif task_button.text.lower() == 'retweet':
                if self.task_retweet(task_button):
                    tasks_completed.append('retweet')
            elif task_button.text.lower() == 'upload':
                times = self.task_upload(task_button)
                tasks_completed.append(f'upload - {times}')
            
        if task_google:
            is_get = False
            actives = ['get $cess', 'Check'.lower(), 'Signature'.lower()]
            buttons = self.node.find_all(By.TAG_NAME, 'button')

            task_buttons = []
            for button in buttons:
                if button.text.lower() in actives:
                    task_buttons.append(button)
            
            for task_button in task_buttons:
                if task_button.text.lower() == 'get $cess':
                    if self.task_get_cess(task_button):
                        is_get = True

                elif is_get and task_button.text.lower() == 'check':
                    if self.click_check(task_button):
                        tasks_completed.append('get $cess')
                
                elif is_get and task_button.text.lower() == 'signature':
                    if self.task_signature(task_button):
                        tasks_completed.append('signature')
        
        self.node.snapshot(f'Hoàn thành: {tasks_completed}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auto', action='store_true', help="Chạy ở chế độ tự động")
    parser.add_argument('--headless', action='store_true', help="Chạy trình duyệt ẩn")
    parser.add_argument('--disable-gpu', action='store_true', help="Tắt GPU")
    args = parser.parse_args()

    profiles = Utility.read_data('profile_name', 'pwd_wallet', 'email', 'pwd_email','seeds')
    if not profiles:
        print("Không có dữ liệu để chạy")
        exit()

    browser_manager = BrowserManager(AutoHandlerClass=Auto, SetupHandlerClass=Setup)
    browser_manager.config_extension('Bitget-Wallet-*.crx')

    browser_manager.run_terminal(
        profiles=profiles,
        max_concurrent_profiles=4,
        block_media=False,
        auto=args.auto,
        headless=args.headless,
        disable_gpu=args.disable_gpu,
    )