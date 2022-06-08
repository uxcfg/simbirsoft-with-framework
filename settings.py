from dotenv import load_dotenv
from pydantic import BaseSettings, Field, typing

load_dotenv()


class Settings(BaseSettings):
    is_remote: bool = True

    wait_time: int = 5  # Глобальное ожидание загрузки веб страницы
    browser: str = "chrome"
    browser_version: str = "89.0"
    browser_width: int = 1920
    browser_height: int = 1080
    browser_blocked_urls: list = []

    selenoid_host: str = "http://127.0.0.1"
    selenoid_port: int = 80
    selenoid_enable_vnc: bool = False
    selenoid_session_name: str = Field("selenoid", env="JOB_NAME")
    selenoid_hosts_entries: list = None

    base_url: str
    in_container: bool = False

    @property
    def selenoid_url(self):
        return f"{self.selenoid_host}:{self.selenoid_port}/wd/hub"

    class Config:
        env_prefix = ""
        case_sensitive = False
        env_file_encoding = "utf-8"

    passwords: typing.Dict[str, str] = {}


settings = Settings()
