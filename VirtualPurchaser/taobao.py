from getProxy import get_random_proxy
from maskCrawler import TaoBaoAutoOperation
import asyncio


def main():
    proxy = get_random_proxy()
    target = 'https://login.taobao.com'
    exe_path = 'C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe'
    username = 'denchris'
    pwd = 'dcq1998314'
    gid = 20739895092
    autoOperation = TaoBaoAutoOperation(username, pwd, exe_path, proxy)
    asyncio.get_event_loop().run_until_complete(autoOperation.start(target, gid))


if __name__ == "__main__":
    main()
