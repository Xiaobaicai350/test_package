"""
第四阶段 - Ajax数据爬取

学习如何分析和爬取Ajax异步加载的数据
这是最高效的动态数据爬取方式
"""

import requests
import json
from typing import Dict, List, Optional

# ==================== 1. Ajax基础知识 ====================

def ajax_intro():
    """
    Ajax简介
    """
    print("=" * 60)
    print("1. Ajax基础知识")
    print("=" * 60 + "\n")
    
    print("""
Ajax (Asynchronous JavaScript and XML)

【什么是Ajax？】
- 异步加载数据的技术
- 不刷新整个页面，只更新部分内容
- 通过JavaScript发送HTTP请求
- 数据通常是JSON格式

【如何识别Ajax？】
1. 查看网页源代码，看不到数据
2. 页面滚动或点击时动态加载内容
3. URL不变但内容在变化

【为什么要爬Ajax？】
✅ 优点：
- 直接获取结构化数据（JSON）
- 不需要解析HTML
- 速度快，效率高
- 不需要Selenium

❌ 缺点：
- 需要分析请求
- 可能有参数加密
- 接口可能有反爬虫

【Ajax vs Selenium对比】

方式         速度    资源    难度    适用场景
─────────────────────────────────────────
Ajax分析     ★★★    低      中      数据规律，API可分析
Selenium     ★      高      低      复杂交互，难以分析
    """)


# ==================== 2. 如何找到Ajax请求 ====================

def find_ajax_request():
    """
    如何找到Ajax请求
    """
    print("\n" + "=" * 60)
    print("2. 如何找到Ajax请求")
    print("=" * 60 + "\n")
    
    print("""
【步骤详解】

第一步：打开浏览器开发者工具
- Chrome: F12 或 右键->检查
- 切换到 Network（网络）标签

第二步：过滤请求类型
- 点击 XHR 或 Fetch
- 这些是Ajax请求

第三步：触发请求
- 滚动页面
- 点击"加载更多"
- 切换分类/页码

第四步：分析请求
- 找到返回数据的请求
- 查看Request URL（请求地址）
- 查看Request Headers（请求头）
- 查看Form Data/Payload（请求参数）
- 查看Response（响应数据）

第五步：模拟请求
- 复制URL和参数
- 用Python的requests发送相同请求

【实例：某电商商品列表】

1. 打开商品列表页
2. F12 -> Network -> XHR
3. 滚动页面，看到请求：
   
   Request URL: https://api.example.com/products/list
   Method: GET
   Query String:
     page=1
     size=20
     category=electronics
   
4. 用Python模拟：
   
   import requests
   
   url = "https://api.example.com/products/list"
   params = {
       "page": 1,
       "size": 20,
       "category": "electronics"
   }
   response = requests.get(url, params=params)
   data = response.json()

【常见Ajax特征】

URL包含：
- /api/
- /ajax/
- /data/
- /json/

参数名称：
- page, pageNum, currentPage (页码)
- size, pageSize, limit (每页数量)
- keyword, query, q (搜索词)
- category, type (分类)

响应格式：
{
  "code": 200,
  "message": "success",
  "data": [...]
}
    """)


# ==================== 3. 实战：爬取Ajax数据 ====================

class AjaxCrawler:
    """
    Ajax爬虫类
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Referer": "https://example.com",  # 很多网站会检查Referer
        })
    
    def fetch_json(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        获取JSON数据
        """
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return None
    
    def parse_data(self, json_data: Dict) -> List[Dict]:
        """
        解析JSON数据
        
        根据实际API结构调整
        """
        # 常见结构1: {code: 200, data: [...]}
        if 'data' in json_data:
            return json_data['data']
        
        # 常见结构2: {result: [...]}
        if 'result' in json_data:
            return json_data['result']
        
        # 常见结构3: 直接就是数组
        if isinstance(json_data, list):
            return json_data
        
        return []


def ajax_example():
    """
    Ajax爬取示例
    """
    print("\n" + "=" * 60)
    print("3. Ajax爬取示例")
    print("=" * 60 + "\n")
    
    # 示例：爬取GitHub API
    print("示例：GitHub API爬取\n")
    
    try:
        url = "https://api.github.com/search/repositories"
        params = {
            "q": "python+crawler",
            "sort": "stars",
            "order": "desc",
            "per_page": 5
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"✅ 找到 {data['total_count']} 个仓库\n")
        
        for i, repo in enumerate(data['items'], 1):
            print(f"仓库 {i}:")
            print(f"  名称: {repo['name']}")
            print(f"  作者: {repo['owner']['login']}")
            print(f"  星标: {repo['stargazers_count']}")
            print(f"  描述: {repo['description'][:50] if repo['description'] else '无'}...")
            print(f"  链接: {repo['html_url']}")
            print()
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")


# ==================== 4. POST请求和参数 ====================

def post_request_example():
    """
    POST请求示例
    """
    print("\n" + "=" * 60)
    print("4. POST请求和参数")
    print("=" * 60 + "\n")
    
    print("""
很多Ajax接口使用POST请求

【POST请求示例】

import requests
import json

url = "https://api.example.com/search"

# 方式1：Form Data (Content-Type: application/x-www-form-urlencoded)
data = {
    "keyword": "Python",
    "page": 1
}
response = requests.post(url, data=data)

# 方式2：JSON Data (Content-Type: application/json)
json_data = {
    "keyword": "Python",
    "page": 1
}
response = requests.post(url, json=json_data)

# 方式3：Raw Data
response = requests.post(url, data=json.dumps(json_data))

【如何判断用哪种方式？】
在Chrome DevTools中查看：
- Request Headers -> Content-Type
  - application/x-www-form-urlencoded -> 用data参数
  - application/json -> 用json参数

【带Cookie的POST请求】
session = requests.Session()

# 先访问首页获取Cookie
session.get("https://example.com")

# 再发送POST请求（自动带上Cookie）
response = session.post(url, json=data)

【示例：搜索接口】
def search_products(keyword, page=1):
    url = "https://api.shop.com/search"
    
    payload = {
        "keyword": keyword,
        "page": page,
        "pageSize": 20
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 ...",
        "Content-Type": "application/json",
        "Referer": "https://www.shop.com"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

results = search_products("手机", page=1)
    """)


# ==================== 5. 参数加密破解 ====================

def parameter_encryption():
    """
    参数加密破解
    """
    print("\n" + "=" * 60)
    print("5. 参数加密破解")
    print("=" * 60 + "\n")
    
    print("""
有些网站会对参数进行加密

【常见加密方式】

1. 时间戳 + 签名
   timestamp = int(time.time())
   sign = md5(f"key={value}&timestamp={timestamp}&secret=xxx")

2. Base64编码
   import base64
   encoded = base64.b64encode(data.encode()).decode()

3. MD5/SHA哈希
   import hashlib
   md5 = hashlib.md5(data.encode()).hexdigest()

4. AES/DES加密
   需要密钥，通常在JavaScript中

【破解步骤】

第一步：找到加密位置
- Chrome DevTools -> Sources
- 搜索参数名
- 设置断点调试

第二步：分析加密逻辑
- 查看JavaScript代码
- 找到加密函数
- 理解加密流程

第三步：Python实现
- 翻译成Python代码
- 或使用execjs执行JavaScript

【示例1：简单签名】
# JavaScript代码
function generateSign(params) {
    var str = "";
    for (var key in params) {
        str += key + "=" + params[key] + "&";
    }
    str += "secret=abc123";
    return md5(str);
}

# Python实现
import hashlib

def generate_sign(params):
    str_list = []
    for key, value in params.items():
        str_list.append(f"{key}={value}")
    str_list.append("secret=abc123")
    str_data = "&".join(str_list)
    return hashlib.md5(str_data.encode()).hexdigest()

【示例2：执行JavaScript】
import execjs

# 读取JavaScript文件
with open('encrypt.js', 'r') as f:
    js_code = f.read()

# 编译JavaScript
ctx = execjs.compile(js_code)

# 调用JavaScript函数
result = ctx.call('generateSign', params)

【工具】
- PyExecJS: 在Python中执行JavaScript
- 在线工具: https://tool.lu/js/ （调试JS代码）
- Chrome DevTools: 断点调试

【注意】
- 不要过度破解，容易被封
- 有些加密很复杂，不值得花时间
- 可以考虑使用Selenium
    """)


# ==================== 6. 翻页处理 ====================

def pagination_handling():
    """
    翻页处理
    """
    print("\n" + "=" * 60)
    print("6. 翻页处理")
    print("=" * 60 + "\n")
    
    example_code = """
【翻页爬取示例】

def crawl_all_pages(max_pages=10):
    '''爬取多页数据'''
    
    all_data = []
    
    for page in range(1, max_pages + 1):
        print(f"正在爬取第 {page} 页...")
        
        url = "https://api.example.com/list"
        params = {
            "page": page,
            "size": 20
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            items = data.get('items', [])
            
            # 检查是否还有数据
            if not items:
                print("已经没有更多数据")
                break
            
            all_data.extend(items)
            print(f"✅ 获取 {len(items)} 条数据")
            
            # 延迟（避免请求过快）
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ 第 {page} 页失败: {e}")
            continue
    
    return all_data

# 使用
data = crawl_all_pages(max_pages=5)
print(f"共爬取 {len(data)} 条数据")

【不同翻页方式】

1. 页码翻页
   page=1, page=2, page=3...

2. 偏移量翻页
   offset=0, offset=20, offset=40...
   
3. 游标翻页
   cursor=xxx (第一页返回)
   cursor=yyy (用上一页的cursor)

4. 时间戳翻页
   before_time=1234567890
   每次取更早的数据
    """
    
    print(example_code)


# ==================== 练习题 ====================

def exercises():
    """
    课后练习
    """
    print("\n" + "=" * 60)
    print("📝 课后练习")
    print("=" * 60 + "\n")
    
    print("""
【练习1】找到Ajax接口
选择一个动态网站：
1. 打开Chrome DevTools
2. 找到数据接口
3. 分析请求参数
4. 用Python模拟请求

推荐网站：
- 豆瓣电影
- 知乎
- GitHub

【练习2】爬取API数据
使用公开API：
1. GitHub API
2. 天气API
3. 新闻API

要求：
- 处理翻页
- 保存数据
- 错误处理

【练习3】POST请求
找一个使用POST的接口：
1. 搜索功能
2. 表单提交
3. 数据筛选

提取并保存结果

【练习4】参数加密
找一个带签名的接口：
1. 分析签名算法
2. Python实现签名
3. 成功请求数据

【练习5】综合项目
完整Ajax爬虫：
1. 分析目标网站
2. 找到所有API
3. 爬取多页数据
4. 数据清洗存储

提示：
- 先用Postman测试API
- 对比浏览器请求头
- 注意Referer和Cookie
- 添加延迟避免封禁
    """)


# ==================== 主函数 ====================

def main():
    """
    主函数
    """
    print("\n" + "=" * 60)
    print("第四阶段 - Ajax数据爬取")
    print("=" * 60)
    
    ajax_intro()
    find_ajax_request()
    ajax_example()
    post_request_example()
    parameter_encryption()
    pagination_handling()
    exercises()
    
    print("\n" + "=" * 60)
    print("✅ Ajax爬取学习完成！")
    print("💡 核心要点：")
    print("   1. Chrome DevTools查找Ajax请求")
    print("   2. 直接请求API获取JSON数据")
    print("   3. 注意Referer、Cookie、Content-Type")
    print("   4. 处理加密参数")
    print("   5. Ajax爬取比Selenium快很多")
    print("⏭️  下一步：学习 03_anti_spider.py")
    print("=" * 60)


if __name__ == "__main__":
    main()

