"""
第二阶段 - 正则表达式

正则表达式是处理文本的强大工具，在爬虫中常用于提取特定格式的数据
"""

import re
from typing import List, Optional

# ==================== 1. 正则表达式基础 ====================

def regex_basics():
    """
    正则表达式基础语法
    """
    print("=" * 60)
    print("1. 正则表达式基础语法")
    print("=" * 60)
    
    print("""
正则表达式（Regular Expression）是匹配文本模式的工具

【基础字符】
.       匹配任意单个字符（除换行符）
\d      匹配数字 [0-9]
\D      匹配非数字
\w      匹配字母数字下划线 [a-zA-Z0-9_]
\W      匹配非字母数字下划线
\s      匹配空白字符（空格、制表符、换行符）
\S      匹配非空白字符

【量词】
*       0次或多次
+       1次或多次
?       0次或1次
{n}     恰好n次
{n,}    至少n次
{n,m}   n到m次

【位置】
^       字符串开头
$       字符串结尾
\b      单词边界

【字符类】
[abc]   匹配a或b或c
[a-z]   匹配a到z
[^abc]  不匹配a、b、c

【分组和引用】
(...)   捕获分组
(?:...) 非捕获分组
|       或

【贪婪与非贪婪】
*       贪婪（尽可能多匹配）
*?      非贪婪（尽可能少匹配）
+?      非贪婪
??      非贪婪

【示例】
\d{11}          11位数字（手机号）
\w+@\w+\.\w+    邮箱地址
\d{4}-\d{2}-\d{2}  日期格式 2024-01-01
https?://.*     HTTP或HTTPS开头的URL
    """)


# ==================== 2. re模块基本使用 ====================

def re_module_basics():
    """
    Python re模块基本使用
    """
    print("=" * 60)
    print("2. re模块基本使用")
    print("=" * 60)
    
    text = "我的手机号是13812345678，邮箱是test@example.com"
    
    # 1. re.search() - 查找第一个匹配
    phone_match = re.search(r'\d{11}', text)
    if phone_match:
        print(f"✅ search找到手机号: {phone_match.group()}")
    
    # 2. re.findall() - 查找所有匹配
    numbers = re.findall(r'\d+', text)
    print(f"✅ findall找到所有数字: {numbers}")
    
    # 3. re.match() - 从字符串开头匹配
    text2 = "138"
    match = re.match(r'\d{3}', text2)
    if match:
        print(f"✅ match从开头匹配: {match.group()}")
    
    # 4. re.sub() - 替换
    censored = re.sub(r'\d{11}', '***隐藏***', text)
    print(f"✅ sub替换: {censored}")
    
    # 5. re.split() - 分割
    text3 = "苹果,香蕉;橙子|葡萄"
    fruits = re.split(r'[,;|]', text3)
    print(f"✅ split分割: {fruits}")
    
    # 6. re.compile() - 编译正则（提高效率）
    pattern = re.compile(r'\d{11}')
    result = pattern.findall(text)
    print(f"✅ compile编译后使用: {result}")
    
    print()


# ==================== 3. 分组和捕获 ====================

def regex_groups():
    """
    正则表达式分组
    """
    print("=" * 60)
    print("3. 分组和捕获")
    print("=" * 60)
    
    # 示例1：提取日期的年月日
    text = "今天是2024-01-15，明天是2024-01-16"
    
    # 使用分组
    pattern = r'(\d{4})-(\d{2})-(\d{2})'
    matches = re.findall(pattern, text)
    
    print("✅ 提取日期:")
    for match in matches:
        year, month, day = match
        print(f"   年:{year}, 月:{month}, 日:{day}")
    
    # 示例2：提取邮箱的用户名和域名
    email = "admin@example.com"
    match = re.search(r'(\w+)@(\w+\.\w+)', email)
    if match:
        username = match.group(1)  # 第1个分组
        domain = match.group(2)    # 第2个分组
        print(f"✅ 邮箱: 用户名={username}, 域名={domain}")
    
    # 示例3：命名分组（更清晰）
    pattern = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
    match = re.search(pattern, text)
    if match:
        print(f"✅ 命名分组: {match.group('year')}年{match.group('month')}月{match.group('day')}日")
    
    # 示例4：非捕获分组 (?:...)
    # 当你需要分组但不需要捕获时使用
    text2 = "http://example.com 和 https://test.com"
    urls = re.findall(r'(?:http|https)://(\w+\.com)', text2)
    print(f"✅ 非捕获分组，只获取域名: {urls}")
    
    print()


# ==================== 4. 贪婪与非贪婪 ====================

def greedy_vs_lazy():
    """
    贪婪匹配 vs 非贪婪匹配
    """
    print("=" * 60)
    print("4. 贪婪 vs 非贪婪")
    print("=" * 60)
    
    html = "<div>内容1</div><div>内容2</div>"
    
    # 贪婪模式（默认）- 尽可能多匹配
    greedy = re.findall(r'<div>.*</div>', html)
    print(f"✅ 贪婪模式 .*: {greedy}")
    print(f"   （匹配了整个字符串）")
    
    # 非贪婪模式 - 尽可能少匹配
    lazy = re.findall(r'<div>.*?</div>', html)
    print(f"✅ 非贪婪模式 .*?: {lazy}")
    print(f"   （分别匹配每个div）")
    
    # 实际应用：提取所有div标签的内容
    contents = re.findall(r'<div>(.*?)</div>', html)
    print(f"✅ 提取内容: {contents}")
    
    print()


# ==================== 5. 爬虫常用正则 ====================

def common_patterns():
    """
    爬虫中常用的正则表达式
    """
    print("=" * 60)
    print("5. 爬虫常用正则表达式")
    print("=" * 60)
    
    # 测试文本
    text = """
    联系方式：
    手机：13812345678, 13987654321
    邮箱：admin@example.com, test@gmail.com
    网址：https://www.python.org, http://github.com
    价格：¥199.00, $99.99, 500元
    日期：2024-01-15, 2024/01/16
    身份证：110101199001011234
    IP地址：192.168.1.1, 8.8.8.8
    """
    
    # 1. 手机号（中国）
    phones = re.findall(r'1[3-9]\d{9}', text)
    print(f"✅ 手机号: {phones}")
    
    # 2. 邮箱
    emails = re.findall(r'\w+@\w+\.\w+', text)
    print(f"✅ 邮箱: {emails}")
    
    # 3. URL
    urls = re.findall(r'https?://[\w./]+', text)
    print(f"✅ URL: {urls}")
    
    # 4. 价格（多种格式）
    prices = re.findall(r'[¥$]?\d+\.?\d*', text)
    print(f"✅ 价格: {prices}")
    
    # 5. 日期
    dates = re.findall(r'\d{4}[-/]\d{2}[-/]\d{2}', text)
    print(f"✅ 日期: {dates}")
    
    # 6. 身份证号（18位）
    id_cards = re.findall(r'\d{17}[\dXx]', text)
    print(f"✅ 身份证: {id_cards}")
    
    # 7. IP地址
    ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text)
    print(f"✅ IP地址: {ips}")
    
    # 8. 中文字符
    chinese = re.findall(r'[\u4e00-\u9fa5]+', "Hello世界Python")
    print(f"✅ 中文: {chinese}")
    
    print()


# ==================== 6. 实战：提取HTML中的数据 ====================

def extract_from_html():
    """
    实战：使用正则从HTML中提取数据
    """
    print("=" * 60)
    print("6. 实战：从HTML提取数据")
    print("=" * 60)
    
    html = """
    <div class="product">
        <h3>iPhone 15 Pro</h3>
        <span class="price">¥7999</span>
        <a href="/product/123">查看详情</a>
    </div>
    <div class="product">
        <h3>MacBook Pro</h3>
        <span class="price">¥12999</span>
        <a href="/product/456">查看详情</a>
    </div>
    """
    
    # 1. 提取所有商品名称
    titles = re.findall(r'<h3>(.*?)</h3>', html)
    print(f"✅ 商品名称: {titles}")
    
    # 2. 提取价格
    prices = re.findall(r'<span class="price">¥(\d+)</span>', html)
    print(f"✅ 价格: {prices}")
    
    # 3. 提取链接
    links = re.findall(r'<a href="(.*?)">', html)
    print(f"✅ 链接: {links}")
    
    # 4. 提取完整的产品信息
    pattern = r'<div class="product">.*?<h3>(.*?)</h3>.*?<span class="price">¥(\d+)</span>.*?<a href="(.*?)">.*?</div>'
    products = re.findall(pattern, html, re.DOTALL)  # re.DOTALL让.匹配换行符
    
    print("\n✅ 完整产品信息:")
    for title, price, link in products:
        print(f"   - {title}: ¥{price}, {link}")
    
    print("""
⚠️ 注意：
1. 正则提取HTML有局限性（HTML嵌套复杂时容易出错）
2. 推荐使用BeautifulSoup或XPath解析HTML
3. 正则适合提取简单、规则固定的文本
    """)
    
    print()


# ==================== 7. 实战：清洗文本数据 ====================

def clean_text():
    """
    实战：使用正则清洗文本数据
    """
    print("=" * 60)
    print("7. 实战：清洗文本数据")
    print("=" * 60)
    
    # 示例：爬取的新闻文本（包含HTML标签、空格、特殊字符）
    raw_text = """
    <p>   Python是一门   <strong>强大</strong>的编程语言。   </p>
    <p>它被广泛应用于Web开发、数据分析、人工智能等领域。&nbsp;&nbsp;</p>
    <script>alert('广告')</script>
    联系方式：13812345678
    """
    
    print(f"原始文本:\n{raw_text}\n")
    
    # 1. 删除HTML标签
    step1 = re.sub(r'<[^>]+>', '', raw_text)
    print(f"✅ 删除HTML标签:\n{step1}\n")
    
    # 2. 删除特殊HTML实体
    step2 = re.sub(r'&[a-z]+;', '', step1)
    print(f"✅ 删除HTML实体:\n{step2}\n")
    
    # 3. 删除多余空格
    step3 = re.sub(r'\s+', ' ', step2)
    print(f"✅ 删除多余空格:\n{step3}\n")
    
    # 4. 隐藏手机号
    step4 = re.sub(r'1[3-9]\d{9}', '***隐藏***', step3)
    print(f"✅ 隐藏手机号:\n{step4}\n")
    
    # 5. 去除首尾空格
    final = step4.strip()
    print(f"✅ 最终清洗结果:\n{final}\n")


# ==================== 8. 正则表达式工具类 ====================

class RegexHelper:
    """
    正则表达式工具类
    """
    
    # 常用正则模式
    PATTERNS = {
        'phone': r'1[3-9]\d{9}',
        'email': r'\w+@\w+\.\w+',
        'url': r'https?://[\w./-]+',
        'price': r'\d+\.?\d*',
        'date': r'\d{4}[-/]\d{2}[-/]\d{2}',
        'ip': r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
        'id_card': r'\d{17}[\dXx]',
        'chinese': r'[\u4e00-\u9fa5]+',
    }
    
    @classmethod
    def extract_phones(cls, text: str) -> List[str]:
        """提取手机号"""
        return re.findall(cls.PATTERNS['phone'], text)
    
    @classmethod
    def extract_emails(cls, text: str) -> List[str]:
        """提取邮箱"""
        return re.findall(cls.PATTERNS['email'], text)
    
    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        """提取URL"""
        return re.findall(cls.PATTERNS['url'], text)
    
    @classmethod
    def extract_prices(cls, text: str) -> List[float]:
        """提取价格并转换为浮点数"""
        price_strs = re.findall(cls.PATTERNS['price'], text)
        return [float(p) for p in price_strs]
    
    @classmethod
    def clean_html(cls, html: str) -> str:
        """清洗HTML标签"""
        # 删除script和style标签及其内容
        text = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL)
        # 删除其他HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        # 删除HTML实体
        text = re.sub(r'&[a-z]+;', ' ', text)
        # 删除多余空格
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    @classmethod
    def mask_sensitive(cls, text: str) -> str:
        """隐藏敏感信息"""
        # 隐藏手机号中间4位
        text = re.sub(r'(1[3-9]\d)\d{4}(\d{4})', r'\1****\2', text)
        # 隐藏邮箱部分字符
        text = re.sub(r'(\w{3})\w+(@\w+\.\w+)', r'\1***\2', text)
        return text


def regex_helper_demo():
    """
    工具类使用示例
    """
    print("=" * 60)
    print("8. 正则工具类使用")
    print("=" * 60)
    
    text = """
    联系我们：
    电话：13812345678，13987654321
    邮箱：admin@example.com
    官网：https://www.python.org
    价格：99.99元，199.00元
    """
    
    print("✅ 提取手机号:", RegexHelper.extract_phones(text))
    print("✅ 提取邮箱:", RegexHelper.extract_emails(text))
    print("✅ 提取URL:", RegexHelper.extract_urls(text))
    print("✅ 提取价格:", RegexHelper.extract_prices(text))
    
    # 清洗HTML
    html = "<p>这是<strong>重要</strong>内容</p><script>alert('test')</script>"
    print(f"✅ 清洗HTML: {RegexHelper.clean_html(html)}")
    
    # 隐藏敏感信息
    sensitive = "我的手机是13812345678，邮箱是admin123@example.com"
    print(f"✅ 隐藏敏感信息: {RegexHelper.mask_sensitive(sensitive)}")
    
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

【练习1】基础匹配
编写正则表达式匹配：
- QQ号（5-11位数字）
- 车牌号（如：京A12345）
- 邮政编码（6位数字）
- 用户名（字母开头，4-16位字母数字下划线）

【练习2】分组提取
从以下文本提取信息：
"张三(男,25岁,北京)，李四(女,23岁,上海)"
提取：姓名、性别、年龄、城市

【练习3】数据清洗
清洗以下文本：
- 删除所有HTML标签
- 统一日期格式（yyyy-mm-dd）
- 提取所有数字
- 替换敏感词（如：电话号码打码）

【练习4】实战应用
从真实网页HTML中：
- 提取所有图片链接
- 提取所有外部链接
- 提取商品价格并求平均值
- 提取文章发布时间

【练习5】优化工具类
扩展RegexHelper类：
- 添加提取身份证号方法
- 添加验证邮箱格式方法
- 添加提取数字方法
- 添加统一日期格式方法

提示：
- 使用re.DOTALL处理多行
- 使用re.IGNORECASE忽略大小写
- 先在 https://regex101.com/ 测试正则表达式
- 复杂HTML用BeautifulSoup，简单文本用正则
    """)


# ==================== 主函数 ====================

def main():
    """
    主函数
    """
    print("\n" + "=" * 60)
    print("正则表达式教程")
    print("=" * 60 + "\n")
    
    regex_basics()
    re_module_basics()
    regex_groups()
    greedy_vs_lazy()
    common_patterns()
    extract_from_html()
    clean_text()
    regex_helper_demo()
    exercises()
    
    print("=" * 60)
    print("✅ 正则表达式学习完成！")
    print("💡 核心要点：")
    print("   1. \\d数字 \\w字母数字 \\s空白")
    print("   2. + 一次或多次，* 零次或多次，? 零次或一次")
    print("   3. (.*?) 非贪婪捕获")
    print("   4. re.findall() 查找所有，re.sub() 替换")
    print("   5. 复杂HTML用BS4/XPath，简单文本用正则")
    print("⏭️  下一步：进入第三阶段实战项目")
    print("=" * 60)


if __name__ == "__main__":
    main()

