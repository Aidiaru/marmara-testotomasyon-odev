import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


class LoginTest(unittest.TestCase):
    def setUp(self):
        """Test başlamadan önce tarayıcıyı ayarla"""
        # Chrome options ayarla (isteğe bağlı)
        options = Options()
        # Headless mod için aşağıdaki satırın yorum işaretini kaldırabilirsiniz
        # options.add_argument('--headless')

        # ChromeDriver yolunu belirt (proje dizinindeyse)
        service = Service("./chromedriver.exe")  # Windows için

        # Chrome driver'ı başlat
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()

        # WebDriverWait için maksimum bekleme süresi
        self.wait = WebDriverWait(self.driver, 10)

    def test_invalid_login(self):
        """Invalid credentials ile login testi"""
        print("Test başlıyor...")

        # 1. Login sayfasına git
        self.driver.get("https://the-internet.herokuapp.com/login")
        print("Login sayfasına gidildi")

        # 2. Username ve password alanlarını bul
        username_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_field = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        # 3. Yanlış kullanıcı adı ve şifre gir
        username_field.clear()
        username_field.send_keys("wronguser")
        print("Yanlış kullanıcı adı girildi: wronguser")

        password_field.clear()
        password_field.send_keys("wrongpassword")
        print("Yanlış şifre girildi: wrongpassword")

        # 4. Login butonuna tıkla
        login_button.click()
        print("Login butonuna tıklandı")

        # 5. Hata mesajının görünmesini bekle ve kontrol et
        error_message = self.wait.until(
            EC.presence_of_element_located((By.ID, "flash"))
        )

        # 6. Hata mesajının içeriğini kontrol et
        error_text = error_message.text
        print(f"Hata mesajı: {error_text}")

        # 7. Beklenen hata mesajının olup olmadığını doğrula
        self.assertIn("Your username is invalid!", error_text)
        print("✅ Test başarılı: Invalid credentials hatası görüntülendi")

        # Test sonucunu görebilmek için kısa bir bekleme
        time.sleep(2)

    def tearDown(self):
        """Test bittikten sonra tarayıcıyı kapat"""
        self.driver.quit()
        print("Tarayıcı kapatıldı")


if __name__ == "__main__":
    # Test'i çalıştır
    unittest.main()