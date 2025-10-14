"""
第四阶段 - Selenium基础

Selenium是一个Web自动化测试工具，也是爬取动态网页的利器
"""

import time
from typing import List

# ==================== 1. Selenium简介 ====================

def selenium_intro():
    """
    Selenium简介
    """
    print("=" * 60)
    print("1. Selenium简介")
    print("=" * 60)
    
    print("""
Selenium 是什么？
- Web自动化测试工具
- 可以控制真实浏览器
- 支持多种编程语言
- 适合爬取动态网页

【核心概念】
1. WebDriver: 浏览器驱动（控制浏览器）
2. 元素定位: 找到网页上的元素
3. 操作元素: 点击、输入、滚动等
4. 等待策略: 等待页面加载完成

【支持的浏览器】
- Chrome (推荐)
- Firefox
- Safari
- Edge

【安装步骤】
1. 安装Selenium
   pip install selenium

2. 下载浏览器驱动
   Chrome: chromedriver
   下载地址: https://chromedriver.chromium.org/

3. 配置驱动路径
   方式1: 放到PATH环境变量
   方式2: 代码中指定路径

【优缺点】
✅ 优点:
- 可以处理JavaScript渲染
- 可以模拟用户行为
- 支持复杂交互

❌ 缺点:
- 速度慢（需要启动浏览器）
- 资源占用大
- 不稳定（网络、页面变化）
    """)


# ==================== 2. Selenium基本使用 ====================

def selenium_basic():
    """
    Selenium基本使用示例
    
    注意：需要先安装selenium和下载chromedriver
    """
    print("\n" + "=" * 60)
    print("2. Selenium基本使用")
    print("=" * 60 + "\n")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        print("✅ Selenium已安装\n")
        
        # 代码示例（不实际运行，仅展示）
        example_code = '''
# 创建浏览器实例
driver = webdriver.Chrome()  # 或指定路径：webdriver.Chrome('/path/to/chromedriver')

# 访问网页
driver.get("https://www.python.org")

# 获取页面标题
print(f"页面标题: {driver.title}")

# 查找元素
search_box = driver.find_element(By.NAME, "q")

# 输入文本
search_box.send_keys("Python爬虫")

# 点击按钮
search_button = driver.find_element(By.ID, "submit")
search_button.click()

# 等待页面加载
time.sleep(2)

# 获取页面内容
page_source = driver.page_source

# 关闭浏览器
driver.quit()
        '''
        
        print("📝 基本使用示例:")
        print(example_code)
        
    except ImportError:
        print("⚠️ Selenium未安装")
        print("📦 安装命令: pip install selenium")


# ==================== 3. 元素定位方法 ====================

def element_locators():
    """
    元素定位方法大全
    """
    print("\n" + "=" * 60)
    print("3. 元素定位方法")
    print("=" * 60 + "\n")
    
    print("""
Selenium提供多种定位元素的方法

【8种定位方式】

1. By.ID - 通过id属性
   element = driver.find_element(By.ID, "username")
   
   HTML: <input id="username" />
   优点: 最快速，id唯一
   缺点: 不是所有元素都有id

2. By.NAME - 通过name属性
   element = driver.find_element(By.NAME, "email")
   
   HTML: <input name="email" />
   适合: 表单元素

3. By.CLASS_NAME - 通过class
   element = driver.find_element(By.CLASS_NAME, "btn-primary")
   
   HTML: <button class="btn btn-primary">提交</button>
   注意: 只能指定一个class

4. By.TAG_NAME - 通过标签名
   elements = driver.find_elements(By.TAG_NAME, "a")
   
   适合: 获取所有某类标签

5. By.LINK_TEXT - 通过链接文本（完全匹配）
   element = driver.find_element(By.LINK_TEXT, "登录")
   
   HTML: <a href="/login">登录</a>

6. By.PARTIAL_LINK_TEXT - 通过链接文本（部分匹配）
   element = driver.find_element(By.PARTIAL_LINK_TEXT, "更多")

7. By.CSS_SELECTOR - 通过CSS选择器（推荐）
   element = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary")
   element = driver.find_element(By.CSS_SELECTOR, "#username")
   
   功能强大，语法简洁

8. By.XPATH - 通过XPath（功能最强）
   element = driver.find_element(By.XPATH, "//input[@id='username']")
   
   可以向上查找父元素

【查找单个 vs 多个】
- find_element(): 返回第一个匹配的元素
- find_elements(): 返回所有匹配的元素列表

【示例】
# 单个元素
username = driver.find_element(By.ID, "username")

# 多个元素
all_links = driver.find_elements(By.TAG_NAME, "a")
for link in all_links:
    print(link.text)
    """)


# ==================== 4. 元素操作 ====================

def element_operations():
    """
    元素操作方法
    """
    print("\n" + "=" * 60)
    print("4. 元素操作")
    print("=" * 60 + "\n")
    
    print("""
找到元素后，可以进行各种操作

【常用操作】

1. 点击
   element.click()

2. 输入文本
   element.send_keys("Python")
   
   # 清空后输入
   element.clear()
   element.send_keys("Java")

3. 获取文本
   text = element.text

4. 获取属性
   value = element.get_attribute("value")
   href = element.get_attribute("href")

5. 判断元素状态
   is_displayed = element.is_displayed()  # 是否可见
   is_enabled = element.is_enabled()      # 是否可用
   is_selected = element.is_selected()    # 是否选中（checkbox）

6. 提交表单
   form.submit()

7. 截图
   element.screenshot("element.png")

【键盘操作】
from selenium.webdriver.common.keys import Keys

# 回车
element.send_keys(Keys.ENTER)

# 组合键
element.send_keys(Keys.CONTROL, "a")  # Ctrl+A

# 特殊键
element.send_keys(Keys.BACKSPACE)    # 退格
element.send_keys(Keys.TAB)          # Tab

【鼠标操作】
from selenium.webdriver.common.action_chains import ActionChains

# 悬停
actions = ActionChains(driver)
actions.move_to_element(element).perform()

# 右键点击
actions.context_click(element).perform()

# 双击
actions.double_click(element).perform()

# 拖拽
actions.drag_and_drop(source, target).perform()

【示例：登录操作】
# 找到用户名输入框
username_input = driver.find_element(By.ID, "username")
username_input.send_keys("admin")

# 找到密码输入框
password_input = driver.find_element(By.ID, "password")
password_input.send_keys("123456")

# 点击登录按钮
login_button = driver.find_element(By.ID, "login-btn")
login_button.click()
    """)


# ==================== 5. 等待策略 ====================

def wait_strategies():
    """
    等待策略（重要！）
    """
    print("\n" + "=" * 60)
    print("5. 等待策略")
    print("=" * 60 + "\n")
    
    print("""
等待策略是Selenium的关键，解决页面加载时机问题

【三种等待方式】

1. 强制等待（不推荐）
   import time
   time.sleep(3)  # 等待3秒
   
   ❌ 缺点：
   - 浪费时间
   - 不够智能
   - 可能还不够

2. 隐式等待（全局设置）
   driver.implicitly_wait(10)  # 最多等待10秒
   
   特点：
   - 全局生效
   - 自动等待元素出现
   - 找到后立即返回
   
   ⚠️ 注意：只在查找元素时等待

3. 显式等待（推荐）
   from selenium.webdriver.support.ui import WebDriverWait
   from selenium.webdriver.support import expected_conditions as EC
   from selenium.webdriver.common.by import By
   
   # 等待元素可见
   element = WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.ID, "myElement"))
   )
   
   优点：
   - 灵活精确
   - 可以等待各种条件
   - 针对具体场景

【常用等待条件】

EC.presence_of_element_located        # 元素存在于DOM中
EC.visibility_of_element_located      # 元素可见
EC.element_to_be_clickable            # 元素可点击
EC.title_contains                     # 标题包含某文本
EC.url_contains                       # URL包含某文本
EC.text_to_be_present_in_element     # 元素文本包含某内容

【综合示例】
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://example.com")

# 设置隐式等待（全局）
driver.implicitly_wait(10)

# 显式等待特定元素
wait = WebDriverWait(driver, 10)

# 等待按钮可点击
button = wait.until(
    EC.element_to_be_clickable((By.ID, "submit-btn"))
)
button.click()

# 等待加载完成
wait.until(EC.title_contains("结果"))

【最佳实践】
1. 隐式等待设置一次（全局）
2. 关键操作使用显式等待
3. 避免使用time.sleep()
4. 等待时间不要太长（10-15秒足够）
    """)


# ==================== 6. 实战示例 ====================

def practical_examples():
    """
    实战示例（代码演示，不实际运行）
    """
    print("\n" + "=" * 60)
    print("6. 实战示例")
    print("=" * 60 + "\n")
    
    example_1 = """
【示例1：爬取动态加载的新闻】

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 创建浏览器
driver = webdriver.Chrome()

try:
    # 访问页面
    driver.get("https://example-news.com")
    
    # 等待新闻列表加载
    wait = WebDriverWait(driver, 10)
    news_list = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "news-list"))
    )
    
    # 滚动加载更多（模拟无限滚动）
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 等待加载
    
    # 提取所有新闻
    news_items = driver.find_elements(By.CLASS_NAME, "news-item")
    
    for item in news_items:
        title = item.find_element(By.CLASS_NAME, "title").text
        link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
        print(f"标题: {title}")
        print(f"链接: {link}")
        print()
    
finally:
    driver.quit()
    """
    
    example_2 = """
【示例2：处理下拉菜单】

from selenium.webdriver.support.select import Select

# 找到下拉菜单
select_element = driver.find_element(By.ID, "category")
select = Select(select_element)

# 三种选择方式
select.select_by_value("tech")           # 通过value
select.select_by_visible_text("科技")    # 通过可见文本
select.select_by_index(1)                # 通过索引

# 获取所有选项
options = select.options
for option in options:
    print(option.text)
    """
    
    example_3 = """
【示例3：处理弹窗】

# 切换到弹窗（Alert）
alert = driver.switch_to.alert

# 获取弹窗文本
alert_text = alert.text
print(alert_text)

# 确认弹窗
alert.accept()

# 取消弹窗
alert.dismiss()

# 输入内容（prompt弹窗）
alert.send_keys("输入内容")
alert.accept()
    """
    
    example_4 = """
【示例4：切换窗口/标签页】

# 获取当前窗口句柄
main_window = driver.current_window_handle

# 获取所有窗口句柄
all_windows = driver.window_handles

# 切换到新窗口
for window in all_windows:
    if window != main_window:
        driver.switch_to.window(window)
        break

# 切换回主窗口
driver.switch_to.window(main_window)
    """
    
    example_5 = """
【示例5：处理iframe】

# 切换到iframe
iframe = driver.find_element(By.ID, "myframe")
driver.switch_to.frame(iframe)

# 在iframe中操作
element = driver.find_element(By.ID, "content")

# 切换回主页面
driver.switch_to.default_content()
    """
    
    print(example_1)
    print(example_2)
    print(example_3)
    print(example_4)
    print(example_5)


# ==================== 7. 无头模式 ====================

def headless_mode():
    """
    无头模式（不显示浏览器窗口）
    """
    print("\n" + "=" * 60)
    print("7. 无头模式（Headless）")
    print("=" * 60 + "\n")
    
    print("""
无头模式：浏览器在后台运行，不显示窗口

【优点】
- 速度更快
- 节省资源
- 适合服务器运行

【配置方法】
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 创建配置
options = Options()
options.add_argument('--headless')              # 无头模式
options.add_argument('--disable-gpu')           # 禁用GPU
options.add_argument('--no-sandbox')            # 沙盒模式
options.add_argument('--disable-dev-shm-usage') # 解决资源限制

# 创建浏览器
driver = webdriver.Chrome(options=options)

【其他有用的配置】
# 禁用图片加载（提速）
prefs = {
    'profile.managed_default_content_settings.images': 2
}
options.add_experimental_option('prefs', prefs)

# 设置窗口大小
options.add_argument('--window-size=1920,1080')

# 禁用自动化控制提示
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

# 设置User-Agent
options.add_argument('user-agent=Mozilla/5.0 ...')
    """)


# ==================== 练习题 ====================

def exercises():
    """
    课后练习
    """
    print("\n" + "=" * 60)
    print("📝 课后练习")
    print("=" * 60 + "\n")
    
    print("""
【练习1】基础操作
使用Selenium完成：
1. 打开百度首页
2. 搜索"Python爬虫"
3. 点击搜索按钮
4. 等待结果加载
5. 提取前10条标题和链接

【练习2】模拟登录
选择一个网站（如GitHub）：
1. 打开登录页面
2. 输入用户名密码
3. 点击登录
4. 等待登录成功
5. 获取用户信息

【练习3】无限滚动
爬取无限滚动页面：
1. 检测页面滚动到底部
2. 自动滚动加载更多
3. 提取所有内容
4. 判断何时停止

【练习4】处理动态表格
爬取动态生成的表格：
1. 等待表格加载
2. 提取表头
3. 提取所有行数据
4. 保存为CSV

【练习5】综合项目
完整爬虫项目：
1. 处理登录
2. 切换分类
3. 翻页爬取
4. 数据存储

提示：
- 先安装 selenium: pip install selenium
- 下载对应浏览器的驱动
- 使用显式等待提高稳定性
- 添加异常处理
- 记得关闭浏览器 driver.quit()
    """)


# ==================== 主函数 ====================

def main():
    """
    主函数
    """
    print("\n" + "=" * 60)
    print("第四阶段 - Selenium基础教程")
    print("=" * 60)
    
    selenium_intro()
    selenium_basic()
    element_locators()
    element_operations()
    wait_strategies()
    practical_examples()
    headless_mode()
    exercises()
    
    print("\n" + "=" * 60)
    print("✅ Selenium基础学习完成！")
    print("💡 核心要点：")
    print("   1. 使用WebDriver控制浏览器")
    print("   2. 8种元素定位方法")
    print("   3. 等待策略很重要（显式等待）")
    print("   4. 无头模式提高效率")
    print("⏭️  下一步：学习 02_ajax_crawler.py")
    print("=" * 60)


if __name__ == "__main__":
    main()

