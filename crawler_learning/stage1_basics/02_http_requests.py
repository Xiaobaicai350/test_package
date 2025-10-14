"""
第一阶段 - HTTP请求与Requests库

本文件教你如何使用Python发送HTTP请求，这是爬虫的基础
"""

import requests
import json
import time
from typing import Dict, Optional

# ==================== 1. HTTP基础知识 ====================

def http_basics():
    """
    HTTP协议基础知识讲解
    """
    print("=" * 60)
    print("1. HTTP协议基础")
    print("=" * 60)
    
    print("""
HTTP（超文本传输协议）是Web的基础协议

【请求方法】
- GET:    获取资源（最常用，爬虫主要用这个）
- POST:   提交数据（表单提交、API调用）
- PUT:    更新资源
- DELETE: 删除资源

【状态码】
- 200: 成功
- 301/302: 重定向
- 400: 客户端错误（请求有误）
- 403: 禁止访问（可能被反爬虫）
- 404: 资源不存在
- 500: 服务器错误

【重要请求头】
- User-Agent: 标识浏览器类型（反爬虫重点检查）
- Cookie: 保持会话状态
- Referer: 来源页面
- Content-Type: 请求体类型

【响应内容】
- HTML: 网页内容
- JSON: API数据
- XML: 结构化数据
""")


# ==================== 2. 基础GET请求 ====================

def basic_get_request():
    """
    最简单的GET请求示例
    """
    print("=" * 60)
    print("2. 基础GET请求")
    print("=" * 60)
    
    # 发送GET请求
    url = "http://httpbin.org/get"  # 测试API
    
    try:
        # requests.get() 相当于在浏览器输入网址
        response = requests.get(url)
        
        # 响应信息
        print(f"✅ 请求URL: {response.url}")
        print(f"✅ 状态码: {response.status_code}")
        print(f"✅ 响应头: {dict(list(response.headers.items())[:3])}")  # 只显示前3个
        print(f"✅ 响应内容(前100字符): {response.text[:100]}")
        
        # 检查请求是否成功
        if response.status_code == 200:
            print("🎉 请求成功！")
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    print()


# ==================== 3. 带参数的GET请求 ====================

def get_with_params():
    """
    带查询参数的GET请求
    类似：https://www.example.com/search?keyword=Python&page=1
    """
    print("=" * 60)
    print("3. 带参数的GET请求")
    print("=" * 60)
    
    url = "http://httpbin.org/get"
    
    # 方式1: 直接拼接URL
    full_url = f"{url}?keyword=Python爬虫&page=1"
    response1 = requests.get(full_url)
    print(f"方式1 URL: {response1.url}")
    
    # 方式2: 使用params参数（推荐）
    params = {
        "keyword": "Python爬虫",
        "page": 1,
        "size": 10
    }
    response2 = requests.get(url, params=params)
    print(f"方式2 URL: {response2.url}")
    print(f"返回数据: {response2.json()}")
    
    print()


# ==================== 4. POST请求 ====================

def post_request():
    """
    POST请求示例（提交表单数据）
    """
    print("=" * 60)
    print("4. POST请求")
    print("=" * 60)
    
    url = "http://httpbin.org/post"
    
    # 表单数据（application/x-www-form-urlencoded）
    data = {
        "username": "testuser",
        "password": "123456",
        "remember": "true"
    }
    
    response = requests.post(url, data=data)
    print(f"✅ 状态码: {response.status_code}")
    print(f"✅ 提交的数据: {response.json()['form']}")
    
    # JSON数据（application/json）
    json_data = {
        "name": "张三",
        "age": 25,
        "skills": ["Python", "爬虫"]
    }
    
    response = requests.post(url, json=json_data)
    print(f"✅ JSON数据: {response.json()['json']}")
    
    print()


# ==================== 5. 设置请求头（重要！）====================

def headers_demo():
    """
    设置请求头 - 反爬虫的关键
    """
    print("=" * 60)
    print("5. 设置请求头（反爬虫关键）")
    print("=" * 60)
    
    url = "http://httpbin.org/headers"
    
    # 不设置User-Agent（会被识别为爬虫）
    response1 = requests.get(url)
    print(f"❌ 默认User-Agent: {response1.json()['headers']['User-Agent']}")
    
    # 伪装成浏览器（推荐做法）
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.google.com/",
    }
    
    response2 = requests.get(url, headers=headers)
    print(f"✅ 自定义User-Agent: {response2.json()['headers']['User-Agent']}")
    print(f"✅ Accept: {response2.json()['headers']['Accept']}")
    
    print("""
💡 重要提示：
1. 大部分网站会检查User-Agent，不设置容易被封
2. 可以从浏览器开发者工具（F12）复制真实的请求头
3. 定期更换User-Agent可以降低被封风险
    """)
    
    print()


# ==================== 6. Cookie和Session ====================

def cookie_session_demo():
    """
    Cookie和Session处理（登录状态保持）
    """
    print("=" * 60)
    print("6. Cookie和Session")
    print("=" * 60)
    
    # 方式1: 直接传递Cookie字符串
    url = "http://httpbin.org/cookies"
    headers = {
        "Cookie": "session_id=abc123; user_id=12345"
    }
    response = requests.get(url, headers=headers)
    print(f"✅ Cookie传递: {response.json()}")
    
    # 方式2: 使用cookies参数
    cookies = {
        "session_id": "abc123",
        "user_id": "12345"
    }
    response = requests.get(url, cookies=cookies)
    print(f"✅ Cookies字典: {response.json()}")
    
    # 方式3: 使用Session保持会话（推荐）
    session = requests.Session()
    
    # 第一次请求，服务器设置Cookie
    response1 = session.get("http://httpbin.org/cookies/set?session=xyz789")
    
    # 第二次请求，自动携带Cookie
    response2 = session.get("http://httpbin.org/cookies")
    print(f"✅ Session自动保持: {response2.json()}")
    
    print("""
💡 使用场景：
- Session适合需要登录的网站爬取
- 自动管理Cookie，不需要手动设置
- 模拟用户登录后的操作
    """)
    
    print()


# ==================== 7. 超时和重试 ====================

def timeout_retry_demo():
    """
    设置超时和重试机制（提高爬虫稳定性）
    """
    print("=" * 60)
    print("7. 超时和重试")
    print("=" * 60)
    
    # 设置超时
    url = "http://httpbin.org/delay/2"  # 延迟2秒响应
    
    try:
        # timeout=5 表示5秒内必须响应
        response = requests.get(url, timeout=5)
        print(f"✅ 请求成功，耗时: {response.elapsed.total_seconds()}秒")
    except requests.Timeout:
        print("❌ 请求超时！")
    
    # 重试机制（简单版）
    def fetch_with_retry(url, max_retries=3):
        """
        带重试的请求函数
        """
        for i in range(max_retries):
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()  # 检查HTTP错误
                return response
            except Exception as e:
                print(f"❌ 第{i+1}次尝试失败: {e}")
                if i < max_retries - 1:
                    time.sleep(2)  # 等待2秒后重试
                else:
                    print("❌ 达到最大重试次数，放弃")
                    return None
    
    print("\n测试重试机制:")
    result = fetch_with_retry("http://httpbin.org/status/500")  # 模拟服务器错误
    
    print()


# ==================== 8. 下载文件 ====================

def download_file():
    """
    下载图片、文档等文件
    """
    print("=" * 60)
    print("8. 下载文件")
    print("=" * 60)
    
    # 下载图片
    image_url = "http://httpbin.org/image/png"
    
    try:
        response = requests.get(image_url)
        
        # 保存二进制内容
        with open("downloaded_image.png", "wb") as f:
            f.write(response.content)
        
        print(f"✅ 文件下载成功")
        print(f"✅ 文件大小: {len(response.content)} bytes")
        
        # 大文件下载（流式下载，节省内存）
        print("\n流式下载大文件:")
        with requests.get(image_url, stream=True) as r:
            r.raise_for_status()
            with open("streamed_image.png", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("✅ 流式下载完成")
        
    except Exception as e:
        print(f"❌ 下载失败: {e}")
    
    print()


# ==================== 9. 综合实战案例 ====================

class SimpleCrawler:
    """
    简单的爬虫类
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
    
    def fetch(self, url: str, params: Optional[Dict] = None) -> Optional[str]:
        """
        获取网页内容
        """
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return None
    
    def fetch_json(self, url: str) -> Optional[Dict]:
        """
        获取JSON数据
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ 获取JSON失败: {e}")
            return None


def practical_example():
    """
    综合实战示例
    """
    print("=" * 60)
    print("9. 综合实战案例")
    print("=" * 60)
    
    crawler = SimpleCrawler()
    
    # 示例1: 获取GitHub API数据
    print("示例1: 获取GitHub仓库信息")
    repo_data = crawler.fetch_json("https://api.github.com/repos/python/cpython")
    if repo_data:
        print(f"✅ 仓库名: {repo_data.get('name')}")
        print(f"✅ 星标数: {repo_data.get('stargazers_count')}")
        print(f"✅ 描述: {repo_data.get('description')}")
    
    # 示例2: 搜索功能
    print("\n示例2: 搜索测试")
    search_data = crawler.fetch_json("https://api.github.com/search/repositories?q=python+crawler&sort=stars&per_page=3")
    if search_data:
        print(f"✅ 搜索结果数: {search_data.get('total_count')}")
        for repo in search_data.get('items', [])[:3]:
            print(f"  - {repo['name']}: {repo['stargazers_count']} stars")
    
    print()


# ==================== 练习题 ====================

def exercises():
    """
    课后练习题
    """
    print("=" * 60)
    print("📝 课后练习")
    print("=" * 60)
    
    print("""
请完成以下练习：

【练习1】基础请求
编写函数 fetch_weather(city)，获取指定城市的天气信息
- 使用公开的天气API
- 添加User-Agent
- 处理异常情况

【练习2】数据下载
编写函数 download_images(url_list)，批量下载图片
- 接收图片URL列表
- 保存到本地并命名（image_1.jpg, image_2.jpg...）
- 添加进度提示

【练习3】登录模拟
使用Session模拟登录流程
- 第一步：GET请求获取登录页面
- 第二步：POST提交用户名密码
- 第三步：访问需要登录才能看的页面

【练习4】重试机制
改进 fetch_with_retry 函数
- 添加指数退避（第1次等1秒，第2次等2秒，第3次等4秒）
- 记录每次失败的原因
- 返回详细的错误信息

提示：可以使用 http://httpbin.org 进行测试
    """)


# ==================== 主函数 ====================

def main():
    """
    主函数
    """
    print("\n" + "=" * 60)
    print("HTTP请求与Requests库 - 爬虫基础")
    print("=" * 60 + "\n")
    
    http_basics()
    basic_get_request()
    get_with_params()
    post_request()
    headers_demo()
    cookie_session_demo()
    timeout_retry_demo()
    download_file()
    practical_example()
    exercises()
    
    print("=" * 60)
    print("✅ 第一阶段学习完成！")
    print("💡 核心要点：")
    print("   1. 掌握GET/POST请求")
    print("   2. 设置User-Agent伪装")
    print("   3. 使用Session保持会话")
    print("   4. 添加超时和重试")
    print("⏭️  下一步：进入第二阶段学习网页解析")
    print("=" * 60)


if __name__ == "__main__":
    main()

