from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import webbrowser


def open_page(url):
	"""使用系统默认浏览器打开网页
	open_page('http://baidu.com')"""
	webbrowser.open(url, new = 0)
	
class browser_utility:
	"""浏览器工具函数抽象类
	由Chrome类实现"""
	def go(self, url):
		"""页面跳转
		chrome.to('http://baidu.com')"""
		self.instance.get(url)

	def set_cookies(cookies):
		"""设置session cookie, 登录验证
		chrome.to('http://www.bilibili.com')
		cookies = [
		    'SESSDATA=a959f392%2C1599117854%2C49e4c*31; Domain=.bilibili.com; Expires=Thu, 03-Sep-2020 07:07:34 GMT;',
		    'DedeUserID=31890217; Domain=.bilibili.com; Expires=Thu, 03-Sep-2020 07:07:34 GMT;', 
		    'DedeUserID__ckMd5=04e309be22e2c59e; Domain=.bilibili.com; Expires=Thu, 03-Sep-2020 07:07:34 GMT;',
		    'bili_jct=d227001282644a628f6b5cbc282085b2; Domain=.bilibili.com; Expires=Thu, 03-Sep-2020 07:07:34 GMT;'
		]"""
		for cookie in cookies:
		    chrome.eval('document.cookie="%s"'%cookie)
	
	@property
	def url(self):
		"""返回当前地址
		print(chrome.url)"""
		return self.instance.current_url
	
	def click(self,selector):
		"""点击页面元素
		chrome.to('http://baidu.com')
		chrome.click('.s-top-left .mnav:nth-of-type(1)')
		"""
		self.find(selector).click()
	
	def exit(self):
		"""关闭浏览器
		chrome.exit()"""
		self.instance.quit()
	
	def eval(self,js_code_str):
		"""执行js代码
		chrome.eval('console.log("hello")')
		"""
		self.instance.execute_script(js_code_str)
	
	@property
	def html(self):
		"""返回网页html
		print(chrome.html）
		"""
		return self.instance.page_source
	
	def find(self,selector,root=None):
		"""查找节点元素
		browser.find('div.coin.view-stat .icon-text',item).text
		"""
		root = root if root else self.instance
		return root.find_element_by_css_selector(selector)
	
	def find_all(self,selector,root=None):
		"""查找所有节点元素
		browser.find_all('div.article-card')
		"""
		root = root if root else self.instance
		return root.find_elements_by_css_selector(selector)
	
	def new_tab(self,url):
		"""新标签页打开
		chrome.new_tab('http://sohu.com')"""
		self.instance.execute_script("""window.open('"""+ url+ """','_blank');""")
	
	def screenshot(self):
		"""网页截图
		chrome.screenshot()"""
		self.instance.save_screenshot('%s.png' % t.timestamp())

HEADLESS_MODE = 0
LISTENING_MODE = 1
DEFAULT_MODE = 2

class Chrome(browser_utility):
	"""继承浏览器工具函数类"""
	def __init__(self,mode=DEFAULT_MODE,using_proxy=False): #三种启动方式，1.无壳，2.现有窗口监听，3.新窗口
		chrome_options = Options()
		chrome_options.add_argument("--no-sandbox") # DevTools相关,防闪退
		if(mode==DEFAULT_MODE):
			pass
		elif(mode == HEADLESS_MODE) : 
			chrome_options.add_argument('--headless')
			chrome_options.add_argument("--disable-gpu") # Windows GPU驱动相关,防闪退
			chrome_options.add_argument('--window-size=2560,1600')
		elif(mode == LISTENING_MODE):
   			chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") # 端口监听模式
		if(using_proxy):
			PROXY = "socks5://127.0.0.1:1080"
			chrome_options.add_argument('--proxy-server=%s' % PROXY)
		self.instance = webdriver.Chrome(options=chrome_options)


if __name__ == '__main__':
	chrome = Chrome(0, using_proxy = True)
	chrome.go('http://google.com')
	print(chrome.html)

	# chrome_options = webdriver.ChromeOptions()
	# PROXY = "socks5://127.0.0.1:1080"
	# chrome_options.add_argument('--proxy-server=%s' % PROXY)
	# c = webdriver.Chrome(options=chrome_options)
	# c.get('http://google.com')
	
