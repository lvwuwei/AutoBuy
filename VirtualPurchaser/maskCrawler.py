__author__ = 'Ldaze'

from pyppeteer.launcher import launch
import asyncio
import pyautogui
import random
import json
import time
import logging
from lxml import etree


def move_slider(x_distance, y_distance, src):
    slider = pyautogui.locateOnScreen(src)
    x, y = pyautogui.center(slider)
    pyautogui.moveTo(x, y)
    pyautogui.dragRel(x_distance, y_distance, 0.5)
    time.sleep(random.uniform(2, 4))


def click_button(src):
    coords = pyautogui.locateOnScreen(src)
    x, y = pyautogui.center(coords)
    pyautogui.leftClick(x, y)
    time.sleep(random.randint(1, 3))


class AutoOperation(object):

    def __init__(self, user_name, password, exec_path, proxy=""):
        self.user_name = user_name
        self.password = password
        self.start_parm = {
            "executablePath": exec_path,
            "headless": False,
            "args": [
                # f'--window-size={self.width},{self.height}'
                '--disable-infobars',
                '--log-level=30',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
                '--no-sandbox',
                '--start-maximized',
                '--proxy-server=%s' % proxy
            ],
        }
        self.browser = None
        self.page = None

    async def get_cookie(self):
        cookies_list = await self.page.cookies()
        cookies = ''
        for cookie in cookies_list:
            str_cookie = '{0}={1};'
            str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
            cookies += str_cookie
        print(cookies)
        return cookies

    @staticmethod
    async def save_cookie(self, cookie):
        with open("../cookies/cookie.json", 'w+', encoding="utf-8") as file:
            json.dump(cookie, file, ensure_ascii=False)

    @staticmethod
    async def load_cookie(self):
        with open("../cookies/cookie.json", 'r', encoding="utf-8") as file:
            cookie = json.load(file)
        return cookie

    async def start(self, url):
        pyppeteer_level = logging.WARNING
        logging.getLogger('pyppeteer').setLevel(pyppeteer_level)
        logging.getLogger('websockets.protocol').setLevel(pyppeteer_level)
        pyppeteer_logger = logging.getLogger('pyppeteer')
        pyppeteer_logger.setLevel(logging.WARNING)
        self.browser = await launch(userDataDir='../log', **self.start_parm)
        self.page = await self.browser.newPage()
        await self.page.setViewport(viewport={'width': 1536, 'height': 1010})

        # js_text = """
        #     () =>{
        #         window.navigator.chrome = { runtime: {},  };
        #         Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        #         Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5, 6], });
        #      }
        # """
        # await page.evaluateOnNewDocument(js_text)
        await self.page.goto(url)


class TaoBaoAutoOperation(AutoOperation):

    def __init__(self, user_name, password, exec_path, proxy=""):
        super(TaoBaoAutoOperation, self).__init__(user_name, password, exec_path, proxy)

    async def run(self, url, data_id, *size):
        await self.start(url)
        await self.tao_bao(data_id, *size)

    async def tao_bao(self, data_id, *size):

        await self.page.click("a.password-login-tab-item")
        time.sleep(random.uniform(1, 3))
        if await self.page.evaluate("document.querySelector('#input#fm-login-id.fm-text')") == "":
            await self.page.type("input#fm-login-id.fm-text", self.user_name, {'delay': random.randint(100, 151) - 50})
            await self.page.type("input#fm-login-password.fm-text", self.password, {'delay': random.randint(100, 151)})
        time.sleep(random.uniform(1, 3))
        await self.page.click("button.fm-button.fm-submit.password-login")

        await self.page.waitForSelector("dd#favorite")
        time.sleep(random.uniform(2, 6))
        await self.page.click("dd#favorite")

        await self.page.waitForSelector("li.J_FavListItem.g-i-item.fav-item.istmall")
        time.sleep(random.uniform(2, 8))
        good = await self.page.xpath("//li[@data-id=%s]" % data_id)
        await good[0].click()

        start_position = (1909, 160)
        end_position = (1909, 174)
        await self.page.waitForSelector("li")
        time.sleep(random.uniform(2, 5))
        move_slider(0, end_position[1] - start_position[1], '../picture/slider.png')
        for i in size:
            click_button(i)

        while 1:
            try:
                click_button('../picture/add_cart.png')
                break
            except TypeError:
                try:
                    click_button('../picture/add_in_supermarket_cart.png')
                    break
                except TypeError:
                    await self.page.reload()
                    await self.page.waitForSelector("li")
                    time.sleep(2)  # random.randint(30, 60)
                    continue
        time.sleep(random.uniform(2, 4))
        move_slider(0, start_position[1]-end_position[1]-100, '../picture/slider.png')
        pyautogui.leftClick(1177, 145)
        time.sleep(random.randint(3, 9))
        pyautogui.leftClick(234, 366)
        time.sleep(1)
        click_button('../picture/settlement.png')
        move_slider(0, 180, '../picture/slider.png')
        input('测试完成以后回到这里按下回车...')
        await self.browser.close()


if __name__ == "__main__":
    target = 'https://login.taobao.com'
    exe_path = 'C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe'
    username = 'denchris'
    pwd = 'dcq1998314'
    gid = 601760264973  # 20739895092
    buy_time = ""
    autoOperation = TaoBaoAutoOperation(username, pwd, exe_path)
    asyncio.get_event_loop().run_until_complete(
        autoOperation.run(
            target,
            gid,
            "../picture/44.png",
            "../picture/vans-gray.png"
        )
    )
