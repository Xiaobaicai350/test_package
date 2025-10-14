"""
第四阶段 - 反爬虫对抗

学习常见的反爬虫技术及应对策略
"""

import requests
import time
import random
from typing import List

# ==================== 1. 反爬虫技术概览 ====================

def anti_spider_intro():
    """
    反爬虫技术概览
    """
    print("=" * 60)
    print("1. 反爬虫技术概览")
    print("=" * 60 + "\n")
    
    print("""
【常见反爬虫技术】

1. User-Agent检测
   ❌ 不设置User-Agent -> 被识别为爬虫
   ✅ 伪装成浏览器

2. 请求频率限制
   ❌ 请求过快 -> IP被封
   ✅ 添加随机延迟

3. IP封禁
   ❌ 单IP大量请求 -> 封IP
   ✅ 使用代理IP池

4. Cookie/Session验证
   ❌ 不带Cookie -> 无法访问
   ✅ 使用Session保持Cookie

5. JavaScript渲染
   ❌ 静态请求获取不到数据
   ✅ 使用Selenium或分析Ajax

6. 验证码
   ❌ 自动访问触发验证码
   ✅ 验证码识别或人工处理

7. 请求头检查
   ❌ 请求头不完整 -> 被拒绝
   ✅ 复制真实浏览器请求头

8. Token/签名验证
   ❌ 缺少签名 -> 请求失败
   ✅ 分析签名算法

9. 蜜罐陷阱
   ❌ 爬取隐藏链接 -> 被标记
   ✅ 只爬取可见内容

10. 字体反爬
    ❌ 文字用自定义字体 -> 乱码
    ✅ 解析字体文件

【反爬虫对抗策略】
┌─────────────────┐
│  降低被检测概率  │
├─────────────────┤
│ 1. 伪装User-Agent │
│ 2. 控制请求频率   │
│ 3. 使用代理IP    │
│ 4. 携带完整请求头 │
│ 5. 模拟真实行为   │
└─────────────────┘

【注意事项】
⚠️ 遵守robots.txt
⚠️ 不要给服务器造成压力
⚠️ 仅用于学习研究
⚠️ 遵守法律法规
    """)


# ==================== 2. User-Agent伪装 ====================

def user_agent_handling():
    """
    User-Agent处理
    """
    print("\n" + "=" * 60)
    print("2. User-Agent伪装")
    print("=" * 60 + "\n")
    
    print("""
【User-Agent是什么？】
标识浏览器类型和版本的字符串

【常见User-Agent】

Chrome (Mac):
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 
(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36

Chrome (Windows):
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 
(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36

Firefox:
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) 
Gecko/20100101 Firefox/121.0

Safari (Mac):
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 
(KHTML, like Gecko) Version/17.1 Safari/605.1.15

手机 (iPhone):
Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 
(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1

【使用方法】
    """)
    
    # 代码示例
    example = """
# 方式1：固定User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}
response = requests.get(url, headers=headers)

# 方式2：随机User-Agent池
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) Firefox/121.0",
]

headers = {
    "User-Agent": random.choice(USER_AGENTS)
}

# 方式3：使用fake-useragent库
from fake_useragent import UserAgent

ua = UserAgent()
headers = {
    "User-Agent": ua.random  # 随机
    # "User-Agent": ua.chrome  # Chrome
    # "User-Agent": ua.firefox  # Firefox
}
    """
    
    print(example)


# ==================== 3. 请求频率控制 ====================

class RateLimiter:
    """
    请求频率限制器
    """
    
    def __init__(self, min_delay=1, max_delay=3):
        """
        初始化
        
        Args:
            min_delay: 最小延迟（秒）
            max_delay: 最大延迟（秒）
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request_time = 0
    
    def wait(self):
        """等待一段时间"""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        # 计算需要等待的时间
        delay = random.uniform(self.min_delay, self.max_delay)
        
        if elapsed < delay:
            wait_time = delay - elapsed
            print(f"⏰ 等待 {wait_time:.2f} 秒...")
            time.sleep(wait_time)
        
        self.last_request_time = time.time()


def rate_limiting_example():
    """
    请求频率控制示例
    """
    print("\n" + "=" * 60)
    print("3. 请求频率控制")
    print("=" * 60 + "\n")
    
    print("""
【为什么要控制频率？】
- 避免给服务器造成压力
- 避免被识别为爬虫
- 避免IP被封

【控制策略】

1. 固定延迟
   time.sleep(2)  # 每次请求等待2秒

2. 随机延迟（推荐）
   delay = random.uniform(1, 3)  # 1-3秒随机
   time.sleep(delay)

3. 指数退避
   遇到错误时逐渐增加延迟
   第1次：1秒
   第2次：2秒
   第3次：4秒
   ...

【实现示例】
    """)
    
    example = """
# 使用频率限制器
limiter = RateLimiter(min_delay=1, max_delay=3)

for url in urls:
    limiter.wait()  # 等待
    response = requests.get(url)
    # 处理数据...

# 手动实现
import time
import random

for url in urls:
    # 随机延迟1-3秒
    time.sleep(random.uniform(1, 3))
    
    response = requests.get(url)
    # 处理数据...
    """
    
    print(example)


# ==================== 4. 代理IP ====================

def proxy_handling():
    """
    代理IP使用
    """
    print("\n" + "=" * 60)
    print("4. 代理IP使用")
    print("=" * 60 + "\n")
    
    print("""
【为什么需要代理IP？】
- 单IP请求过多会被封
- 突破IP限制
- 提高并发能力

【代理IP类型】

1. 透明代理
   - 服务器知道你用了代理
   - 不推荐

2. 匿名代理
   - 服务器知道你用了代理，但不知道真实IP
   - 一般

3. 高匿代理（推荐）
   - 服务器不知道你用了代理
   - 效果最好

【获取代理IP】

1. 免费代理（不稳定）
   - https://www.kuaidaili.com/free/
   - https://www.89ip.cn/

2. 付费代理（推荐）
   - 阿布云
   - 快代理
   - 讯代理

【使用方法】
    """)
    
    example = """
# 方式1：单个代理
proxies = {
    "http": "http://user:pass@proxy.com:port",
    "https": "http://user:pass@proxy.com:port",
}
response = requests.get(url, proxies=proxies)

# 方式2：代理池
class ProxyPool:
    def __init__(self):
        self.proxies = [
            "http://proxy1.com:8000",
            "http://proxy2.com:8000",
            "http://proxy3.com:8000",
        ]
        self.current = 0
    
    def get_proxy(self):
        proxy = self.proxies[self.current]
        self.current = (self.current + 1) % len(self.proxies)
        return {"http": proxy, "https": proxy}

pool = ProxyPool()

for url in urls:
    proxies = pool.get_proxy()
    try:
        response = requests.get(url, proxies=proxies, timeout=5)
    except:
        # 代理失败，换下一个
        continue

# 方式3：测试代理是否可用
def test_proxy(proxy):
    try:
        response = requests.get(
            "http://httpbin.org/ip",
            proxies=proxy,
            timeout=5
        )
        return response.status_code == 200
    except:
        return False

# 过滤可用代理
valid_proxies = []
for proxy in all_proxies:
    if test_proxy(proxy):
        valid_proxies.append(proxy)
    """
    
    print(example)


# ==================== 5. 完整请求头 ====================

def complete_headers():
    """
    完整请求头
    """
    print("\n" + "=" * 60)
    print("5. 完整请求头")
    print("=" * 60 + "\n")
    
    print("""
【为什么需要完整请求头？】
很多网站会检查请求头的完整性

【如何获取真实请求头？】
1. Chrome DevTools -> Network
2. 点击某个请求
3. 复制 Request Headers

【完整请求头示例】
    """)
    
    headers_example = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.example.com",
        "Referer": "https://www.example.com/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    }
    
    print("headers = {")
    for key, value in headers_example.items():
        print(f'    "{key}": "{value}",')
    print("}")
    
    print("""
【重要请求头说明】

User-Agent: 浏览器标识（必须）
Referer: 来源页面（很多网站检查）
Cookie: 会话信息（登录状态）
Accept: 接受的内容类型
Accept-Language: 语言偏好
Host: 目标主机（自动设置）
Connection: 连接方式
    """)


# ==================== 6. 验证码处理 ====================

def captcha_handling():
    """
    验证码处理
    """
    print("\n" + "=" * 60)
    print("6. 验证码处理")
    print("=" * 60 + "\n")
    
    print("""
【验证码类型】

1. 图片验证码
   - 数字字母组合
   - 算术题
   - 扭曲文字

2. 滑块验证码
   - 拖动滑块到指定位置

3. 点选验证码
   - 点击图片中的文字

4. 行为验证
   - 分析鼠标轨迹

【处理方法】

1. OCR识别（简单验证码）
   - pytesseract
   - ddddocr

2. 打码平台（推荐）
   - 超级鹰
   - 云打码
   - 价格：0.01-0.1元/次

3. 机器学习
   - 训练CNN模型
   - 需要大量数据

4. 人工处理
   - 弹窗提示人工输入

【示例：使用ddddocr】
    """)
    
    example = """
# 安装：pip install ddddocr

import ddddocr

# 创建识别器
ocr = ddddocr.DdddOcr()

# 识别图片
with open("captcha.png", "rb") as f:
    image_bytes = f.read()

result = ocr.classification(image_bytes)
print(f"识别结果: {result}")

# 在爬虫中使用
def solve_captcha(image_url):
    # 下载验证码图片
    response = requests.get(image_url)
    
    # 识别
    ocr = ddddocr.DdddOcr()
    result = ocr.classification(response.content)
    
    return result

# 使用
captcha_text = solve_captcha("https://example.com/captcha.png")
    """
    
    print(example)


# ==================== 练习题 ====================

def exercises():
    """
    课后练习
    """
    print("\n" + "=" * 60)
    print("📝 课后练习")
    print("=" * 60 + "\n")
    
    print("""
【练习1】User-Agent池
实现一个User-Agent管理类：
1. 维护多个User-Agent
2. 随机选择
3. 定期更新
4. 支持按浏览器类型选择

【练习2】频率限制器
增强RateLimiter类：
1. 支持令牌桶算法
2. 支持滑动窗口
3. 统计请求速度
4. 自动调整延迟

【练习3】代理池
实现完整的代理池：
1. 从免费网站爬取代理
2. 测试代理可用性
3. 维护可用代理列表
4. 自动剔除失效代理
5. 支持代理轮换

【练习4】验证码识别
实践验证码处理：
1. 收集验证码样本
2. 使用OCR识别
3. 计算识别准确率
4. 优化识别算法

【练习5】综合对抗
完整的反反爬虫爬虫：
1. User-Agent伪装
2. 随机延迟
3. 代理IP轮换
4. 完整请求头
5. Cookie管理
6. 异常重试
7. 日志记录

提示：
- 从简单网站开始练习
- 遵守网站规则
- 不要过度请求
- 仅用于学习研究
    """)


# ==================== 主函数 ====================

def main():
    """
    主函数
    """
    print("\n" + "=" * 60)
    print("第四阶段 - 反爬虫对抗")
    print("=" * 60)
    
    anti_spider_intro()
    user_agent_handling()
    rate_limiting_example()
    proxy_handling()
    complete_headers()
    captcha_handling()
    exercises()
    
    print("\n" + "=" * 60)
    print("✅ 反爬虫对抗学习完成！")
    print("💡 核心要点：")
    print("   1. 伪装User-Agent（必须）")
    print("   2. 控制请求频率（重要）")
    print("   3. 使用代理IP（高级）")
    print("   4. 完整请求头（细节）")
    print("   5. 验证码识别（难点）")
    print("⚠️  记住：遵守规则，合理使用")
    print("⏭️  下一步：进入第五阶段学习Scrapy框架")
    print("=" * 60)


if __name__ == "__main__":
    main()

