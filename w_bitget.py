# version 20250402
import argparse
from selenium.webdriver.common.by import By

from browser_automation import BrowserManager, Node
from utils import Utility

EXTENSION_URL = 'chrome-extension://jiidiaalihmmhddjgbnbgdfflelocpak'


class Auto:
    def __init__(self, node: Node, profile: dict) -> None:
        self.driver = node._driver
        self.node = node
        self.profile_name = profile.get('profile_name')
        self.password = profile.get('password')
        self.seeds = profile.get('seeds')
    def confirm(self, text: str = 'Cancel'):
        done = False
        current_window = self.driver.current_window_handle
        if not self.node.switch_tab(f'{EXTENSION_URL}'):
            self.node.new_tab(f'{EXTENSION_URL}/popup.html')
        
        footerBox = self.node.find(By.CSS_SELECTOR, '[class="footer"], [class="footerBox"]')
        if not footerBox:
            self.node.log('Không tìm thấy footer chứa button')
        
        buttons = self.node.find_all(By.TAG_NAME, 'button', footerBox, wait=0, timeout=0)
        button_click = None
        for button in buttons:
            if button.text.lower() == text.lower():
                button_click = button
        
        if button_click:
            try:
                button_click.click()
                done = True
            except Exception as e:
                self.node.log(f'Không thể click vào {text}. Gặp lỗi {e}')
        else:
            self.node.log(f'Không tìm thấy button {text}')
        self.driver.switch_to.window(current_window)
        return done

    def import_wallet(self) -> bool:
        """Import ví mới từ seed phrase"""
        if not self.seeds:
            self.node.snapshot('Không tìm thấy seed trong data.txt')
            return False
            
        self.seeds = self.seeds.split(' ')
        if len(self.seeds) != 12:
            self.node.snapshot('Seeds không đủ 12 từ')
            return False
        
        if not self.node.find_and_click(By.XPATH, '//button[contains(text(),"Import a wallet")]'):
            self.node.snapshot('Không tìm thấy button Import')
            return False
        
        inputs_pass = self.node.find_all(By.XPATH, '//div[input[@id="component-password"]]')

        for input in inputs_pass[:2]:
            self.node.find_and_input(By.CSS_SELECTOR, '[id="component-password"]', self.password, input, delay=0, wait=0, timeout=10)
        
        self.node.find_and_click(By.XPATH, '//button[span[contains(text(),"Next")]]')

        # Đợi form và import 12 seed
        inputs_seed = self.node.find_all(By.XPATH, '//div[input[@class="wordInput-contaniner-input"]]')
        if len(inputs_seed) != 12:
            self.node.snapshot(f'Không tìm thấy input 12 seed')
        for index, input in enumerate(inputs_seed):
            self.node.find_and_input(By.CSS_SELECTOR, '[class="wordInput-contaniner-input"]', self.seeds[index], parent_element=input, delay=0, wait=0.1)
        self.node.find_and_click(By.XPATH, '//button[span[contains(text(), "Confirm")]]')
        self.node.find_and_click(By.XPATH, '//button[contains(text(),"OK")]')
        
        if self.is_unlocked():
            return True
        else:
            return False

    def is_unlocked(self) -> bool:
        self.node.go_to(f'{EXTENSION_URL}/popup.html')
        if self.node.find(By.CSS_SELECTOR, '[class="homepage_assets"]', timeout=60):
            self.node.log(f'Unlock wallet thành công')
            return True
        else:
            self.node.log(f'Unlock wallet thất bại')
            return False
        
    def unlock_wallet(self) -> bool:
        """Unlock ví với mật khẩu"""
        self.node.switch_tab(f'{EXTENSION_URL}')
        if not self.node.find_and_input(By.CSS_SELECTOR, '[id="component-password"]', self.password, delay=0.1, timeout=20):
            return False
        self.node.press_key('Enter')

        return self.is_unlocked()

    def change_network(self, network_name: str, rpc_url: str, chain_id: str, symbol: str, block_explorer: str = None):
        """Thay đổi mạng lưới"""
        # Kiểm tra và chọn network
        current_network = self.node.get_text(By.CSS_SELECTOR, '[class*="networkName"]')
        
        if network_name in current_network:
            self.node.log(f"Đang ở network {network_name}, không cần chuyển")
            return True
        else:
            if not self.node.find_and_click(By.CSS_SELECTOR, '[class*="networkName"]'):
                self.node.snapshot(f'Không thể click vào name network')
            
            network_list = self.node.find_all(By.CSS_SELECTOR, '[class*="nameBox"]')
            name_list = [ network.text for network in network_list] 
            if network_name in name_list:
                self.node.find_and_click(By.XPATH, f'//div[contains(text(),"{network_name}")]')
            else:
                self.node.find_and_click(By.XPATH, '//span[contains(text(),"Add a network")]')
                self.node.find_and_click(By.XPATH, '//div[contains(text(),"Custom")]')
                self.node.find_and_click(By.XPATH, '//button[contains(text(),"View All Custom Mainnets")]')
                self.node.find_and_click(By.XPATH, '//span[contains(text(),"Add manually")]')

                inputs_network = self.node.find_all(By.CSS_SELECTOR, '[class="inputItemBox"]')
                if len(inputs_network) != 5:
                    self.node.snapshot(f'Không tìm thấy input add network')
                self.node.find_and_input(By.TAG_NAME, 'textarea', rpc_url, inputs_network[0], delay=0, wait=0.1, timeout=0)
                self.node.find_and_input(By.TAG_NAME, 'input', network_name, inputs_network[1], delay=0, wait=0.1, timeout=0)
                self.node.find_and_input(By.TAG_NAME, 'input', chain_id, inputs_network[2], delay=0, wait=0.1, timeout=0)
                self.node.find_and_input(By.TAG_NAME, 'input', symbol, inputs_network[3], delay=0, wait=0.1, timeout=0)
                self.node.find_and_input(By.TAG_NAME, 'input', block_explorer, inputs_network[4], delay=0, wait=0.1, timeout=0)
                self.node.find_and_click(By.CSS_SELECTOR, '[class="buttonBox"]')

        current_network = self.node.get_text(By.CSS_SELECTOR, '[class*="networkName"]')
        
        if network_name in current_network:
            self.node.log(f"Chuyển network {network_name} thành công")
            return True
        else:
            return False

    def change_network_other(self, network_name):
        """Thay đổi mạng lưới"""
        # Kiểm tra và chọn network
        current_network = self.node.get_text(By.CSS_SELECTOR, '[class*="networkName"]')
        
        if network_name in current_network:
            self.node.log(f"Đang ở network {network_name}, không cần chuyển")
            return True
        else:
            if not self.node.find_and_click(By.CSS_SELECTOR, '[class*="networkName"]'):
                self.node.snapshot(f'Không thể click vào name network')
            
            self.node.find_and_input(By.CSS_SELECTOR, '[placeholder="Search for mainnets"]', network_name, delay=0.1)
            self.node.find_and_click(By.XPATH, f'//div[contains(text(),"{network_name}")]')
    
            current_network = self.node.get_text(By.CSS_SELECTOR, '[class*="networkName"]')
            
            if network_name in current_network:
                self.node.log(f"Chuyển network {network_name} thành công")
                return True
            else:
                return False
        
    def _run(self):
        # Chuyển đến trang extension
        self.node.go_to(f'{EXTENSION_URL}/popup.html', 'get')
        if not self.unlock_wallet():
            # import wallet
            if not self.import_wallet():
                self.node.snapshot(f'Unlock ví thất bại')
                pass

        return True

class Setup:
    def __init__(self, node: Node, profile) -> None:
        self.node = node
        self.profile = profile
        
    def _run(self):
        # Chuyển đến trang extension
        self.node.go_to(f'{EXTENSION_URL}/popup.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auto', action='store_true', help="Chạy ở chế độ tự động")
    parser.add_argument('--headless', action='store_true', help="Chạy trình duyệt ẩn")
    parser.add_argument('--disable-gpu', action='store_true', help="Tắt GPU")
    args = parser.parse_args()

    profiles = Utility.read_data('profile_name', 'password', 'seeds')
    
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