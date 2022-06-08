import os
import pathlib
import shutil

import allure
from pytest import fixture

from utils.browser import setup_browser
from utils.patch import patch_selenium
from register import pages as all_pages


patch_selenium()

files_dir = pathlib.Path(__file__).parent.joinpath("files").absolute()


@fixture
def browser():
    browser = setup_browser()
    yield browser
    browser.quit()


@fixture
def pages(browser):
    all_pages.init(browser)
    return all_pages


@fixture
def pdf_file():
    return os.path.join(files_dir, "pdf_less_1mb.pdf")


@fixture
def docx_file():
    return os.path.join(files_dir, "file_doc.docx")


@fixture(autouse=True)
def setup(request):
    allure.dynamic.label("build_number", os.getenv("BUILD_NUMBER", "0"))
    allure.dynamic.label("job_url", os.getenv("JOB_URL", ""))
    allure.dynamic.label("as_id", request.node.name)
    allure.dynamic.feature("Функциональное тестирование")


@fixture
def clear_jenkins_workspace():
    if not os.getenv("WORKSPACE"):
        return
    workspace = pathlib.Path(os.getenv("WORKSPACE"))
    for filename in workspace.glob("**/*"):
        if "allure" in filename.as_posix():
            continue
        if filename.is_dir():
            shutil.rmtree(filename.as_posix())
        else:
            os.remove(filename.as_posix())
