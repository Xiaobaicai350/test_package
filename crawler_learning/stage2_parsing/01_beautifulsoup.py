"""
第二阶段 - BeautifulSoup网页解析

BeautifulSoup是Python最流行的HTML解析库，简单易用
"""

from bs4 import BeautifulSoup
import requests

# ==================== 1. HTML基础知识 ====================

def html_basics():
    """
    HTML基础知识速成
    """
    print("=" * 60)
    print("1. HTML基础知识")
    print("=" * 60)
    
    print("""
HTML（超文本标记语言）是网页的结构

【基本结构】
<html>
  <head>
    <title>网页标题</title>
  </head>
  <body>
    <div class="container">
      <h1 id="title">这是标题</h1>
      <p class="content">这是段落</p>
      <a href="https://example.com">链接</a>
    </div>
  </body>
</html>

【常用标签】
- <div>: 块级容器
- <span>: 行内容器
- <a>: 链接 (属性: href)
- <img>: 图片 (属性: src, alt)
- <p>: 段落
- <h1>-<h6>: 标题
- <ul>, <li>: 列表
- <table>, <tr>, <td>: 表格

【重要属性】
- class: CSS类名（一个元素可以有多个class）
- id: 唯一标识符
- href: 链接地址
- src: 资源地址（图片、脚本）

【爬虫关注点】
1. 找到数据在哪个标签里
2. 通过class或id定位元素
3. 提取标签内的文本或属性
    """)


# ==================== 2. BeautifulSoup基础 ====================

def bs4_basics():
    """
    BeautifulSoup基础用法
    """
    print("=" * 60)
    print("2. BeautifulSoup基础")
    print("=" * 60)
    
    # 示例HTML
    html = """
    <html>
        <head>
            <title>爬虫学习网站</title>
        </head>
        <body>
            <div class="header">
                <h1 id="main-title">欢迎学习爬虫</h1>
            </div>
            <div class="content">
                <p class="intro">Python是最好的爬虫语言</p>
                <p class="intro">BeautifulSoup非常好用</p>
                <a href="https://www.python.org">Python官网</a>
                <a href="https://www.github.com">GitHub</a>
            </div>
            <div class="footer">
                <span>联系我们: admin@example.com</span>
            </div>
        </body>
    </html>
    """
    
    # 创建BeautifulSoup对象
    # 第一个参数：HTML字符串
    # 第二个参数：解析器（html.parser是Python内置的）
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. 获取标题
    title = soup.title
    print(f"✅ 标题标签: {title}")
    print(f"✅ 标题文本: {title.string}")
    
    # 2. 查找第一个匹配的标签
    h1 = soup.find('h1')
    print(f"✅ 第一个h1: {h1.string}")
    
    # 3. 通过id查找
    main_title = soup.find(id='main-title')
    print(f"✅ ID查找: {main_title.string}")
    
    # 4. 通过class查找（注意：class是Python关键字，需要用class_）
    intro = soup.find(class_='intro')
    print(f"✅ Class查找: {intro.string}")
    
    # 5. 查找所有匹配的标签
    all_p = soup.find_all('p')
    print(f"✅ 所有p标签数量: {len(all_p)}")
    for i, p in enumerate(all_p, 1):
        print(f"   {i}. {p.string}")
    
    # 6. 提取链接
    all_links = soup.find_all('a')
    print(f"✅ 所有链接:")
    for link in all_links:
        text = link.string
        url = link.get('href')  # 或 link['href']
        print(f"   - {text}: {url}")
    
    print()


# ==================== 3. 查找方法详解 ====================

def find_methods():
    """
    find() 和 find_all() 详解
    """
    print("=" * 60)
    print("3. 查找方法详解")
    print("=" * 60)
    
    html = """
    <div class="container">
        <div class="article" id="article-1">
            <h2>文章标题1</h2>
            <p class="author">作者: 张三</p>
            <p class="content">这是第一篇文章的内容</p>
            <span class="date">2024-01-01</span>
        </div>
        <div class="article" id="article-2">
            <h2>文章标题2</h2>
            <p class="author">作者: 李四</p>
            <p class="content">这是第二篇文章的内容</p>
            <span class="date">2024-01-02</span>
        </div>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # find() - 返回第一个匹配的元素
    first_article = soup.find('div', class_='article')
    print(f"✅ find()返回第一个: {first_article.get('id')}")
    
    # find_all() - 返回所有匹配的元素列表
    all_articles = soup.find_all('div', class_='article')
    print(f"✅ find_all()返回所有: {len(all_articles)}个")
    
    # 限制返回数量
    limited = soup.find_all('p', limit=2)
    print(f"✅ 限制数量(limit=2): {len(limited)}个")
    
    # 多个条件
    author_p = soup.find('p', class_='author')
    print(f"✅ 多条件查找: {author_p.string}")
    
    # 使用attrs参数（当属性是Python关键字时）
    article1 = soup.find('div', attrs={'id': 'article-1'})
    print(f"✅ attrs参数: {article1.h2.string}")
    
    # 正则表达式匹配
    import re
    date_spans = soup.find_all('span', class_=re.compile('date'))
    print(f"✅ 正则匹配: {len(date_spans)}个日期")
    
    # 函数匹配（高级）
    def has_author_class(tag):
        return tag.has_attr('class') and 'author' in tag['class']
    
    authors = soup.find_all(has_author_class)
    print(f"✅ 函数匹配: {len(authors)}个作者")
    
    print()


# ==================== 4. CSS选择器 ====================

def css_selector():
    """
    CSS选择器（推荐使用，更简洁）
    """
    print("=" * 60)
    print("4. CSS选择器")
    print("=" * 60)
    
    html = """
    <div class="container">
        <ul class="news-list">
            <li class="news-item active">
                <a href="/news/1">新闻标题1</a>
                <span class="category">科技</span>
            </li>
            <li class="news-item">
                <a href="/news/2">新闻标题2</a>
                <span class="category">财经</span>
            </li>
            <li class="news-item">
                <a href="/news/3">新闻标题3</a>
                <span class="category">体育</span>
            </li>
        </ul>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. 标签选择器
    items = soup.select('li')
    print(f"✅ 标签选择器 'li': {len(items)}个")
    
    # 2. class选择器（.类名）
    news_items = soup.select('.news-item')
    print(f"✅ Class选择器 '.news-item': {len(news_items)}个")
    
    # 3. id选择器（#id名）
    # container = soup.select('#container')
    
    # 4. 后代选择器（空格）
    links = soup.select('.news-list a')
    print(f"✅ 后代选择器 '.news-list a': {len(links)}个")
    for link in links:
        print(f"   - {link.string}: {link.get('href')}")
    
    # 5. 子选择器（>）
    direct_children = soup.select('.container > ul')
    print(f"✅ 子选择器 '.container > ul': {len(direct_children)}个")
    
    # 6. 多个类（.class1.class2）
    active_item = soup.select('.news-item.active')
    print(f"✅ 多类选择器 '.news-item.active': {len(active_item)}个")
    
    # 7. 属性选择器
    tech_category = soup.select('span.category')
    print(f"✅ 属性选择器: {len(tech_category)}个分类")
    
    # 8. 第n个元素
    first_item = soup.select('.news-item:nth-of-type(1)')
    print(f"✅ 第1个元素: {first_item[0].a.string}")
    
    print("""
💡 CSS选择器语法总结：
- 标签: 'div'
- Class: '.classname'
- ID: '#idname'
- 后代: '.parent .child'
- 子元素: '.parent > .child'
- 属性: '[href]', '[href="/news"]'
- 第n个: ':nth-of-type(n)'
    """)
    
    print()


# ==================== 5. 遍历DOM树 ====================

def navigate_tree():
    """
    遍历DOM树（父节点、子节点、兄弟节点）
    """
    print("=" * 60)
    print("5. 遍历DOM树")
    print("=" * 60)
    
    html = """
    <div class="article">
        <h2>标题</h2>
        <p class="author">作者</p>
        <p class="content">内容</p>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 获取p标签
    p_tag = soup.find('p', class_='author')
    
    # 1. 父节点
    parent = p_tag.parent
    print(f"✅ 父节点: {parent.name}")
    
    # 2. 所有父节点
    parents = [p.name for p in p_tag.parents]
    print(f"✅ 所有父节点: {parents}")
    
    # 3. 子节点
    div_tag = soup.find('div')
    children = list(div_tag.children)
    print(f"✅ 子节点数: {len(children)}")
    for child in div_tag.children:
        if child.name:  # 跳过空白文本
            print(f"   - {child.name}: {child.string}")
    
    # 4. 下一个兄弟节点
    next_sibling = p_tag.find_next_sibling()
    print(f"✅ 下一个兄弟: {next_sibling.get('class')}")
    
    # 5. 上一个兄弟节点
    prev_sibling = p_tag.find_previous_sibling()
    print(f"✅ 上一个兄弟: {prev_sibling.name}")
    
    print()


# ==================== 6. 提取数据技巧 ====================

def extract_data():
    """
    提取数据的各种技巧
    """
    print("=" * 60)
    print("6. 提取数据技巧")
    print("=" * 60)
    
    html = """
    <div class="product">
        <h3 class="title">iPhone 15 Pro</h3>
        <span class="price" data-value="7999">¥7999</span>
        <img src="/images/iphone.jpg" alt="iPhone图片">
        <p class="desc">
            这是一款<strong>高端</strong>手机
            支持5G网络
        </p>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. 获取文本内容
    title = soup.find('h3', class_='title')
    print(f"✅ .string: {title.string}")  # 获取直接文本
    print(f"✅ .get_text(): {title.get_text()}")  # 获取所有文本
    
    # 2. 获取属性值
    price = soup.find('span', class_='price')
    print(f"✅ data-value属性: {price.get('data-value')}")
    print(f"✅ 或使用['data-value']: {price['data-value']}")
    
    # 3. 获取图片链接
    img = soup.find('img')
    print(f"✅ src: {img.get('src')}")
    print(f"✅ alt: {img.get('alt')}")
    
    # 4. 获取包含子标签的文本
    desc = soup.find('p', class_='desc')
    print(f"✅ 完整文本: {desc.get_text(strip=True)}")  # strip=True去除空白
    
    # 5. 分隔符处理
    print(f"✅ 分隔符处理: {desc.get_text(separator=' ', strip=True)}")
    
    # 6. 检查标签是否存在
    rating = soup.find('span', class_='rating')
    if rating:
        print(f"✅ 评分: {rating.string}")
    else:
        print("⚠️ 未找到评分信息")
    
    # 7. 使用get()安全获取属性（不存在时返回None）
    link = soup.find('a')
    href = link.get('href') if link else None
    print(f"✅ 安全获取: {href}")
    
    print()


# ==================== 7. 实战案例：解析新闻列表 ====================

def parse_news_example():
    """
    实战：解析新闻列表页面
    """
    print("=" * 60)
    print("7. 实战案例：解析新闻列表")
    print("=" * 60)
    
    # 模拟新闻列表HTML
    html = """
    <div class="news-container">
        <div class="news-item">
            <a href="/news/1" class="title">Python 3.12正式发布</a>
            <span class="author">作者: 张三</span>
            <span class="date">2024-01-15</span>
            <p class="summary">Python 3.12带来了性能提升...</p>
            <span class="views">浏览: 1000</span>
        </div>
        <div class="news-item">
            <a href="/news/2" class="title">AI技术的最新进展</a>
            <span class="author">作者: 李四</span>
            <span class="date">2024-01-16</span>
            <p class="summary">人工智能领域迎来重大突破...</p>
            <span class="views">浏览: 2000</span>
        </div>
        <div class="news-item">
            <a href="/news/3" class="title">Web开发趋势2024</a>
            <span class="author">作者: 王五</span>
            <span class="date">2024-01-17</span>
            <p class="summary">2024年Web开发的新趋势...</p>
            <span class="views">浏览: 1500</span>
        </div>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 解析所有新闻
    news_list = []
    news_items = soup.find_all('div', class_='news-item')
    
    for item in news_items:
        # 提取各个字段
        title_tag = item.find('a', class_='title')
        title = title_tag.string
        url = title_tag.get('href')
        
        author = item.find('span', class_='author').string.replace('作者: ', '')
        date = item.find('span', class_='date').string
        summary = item.find('p', class_='summary').string
        views = item.find('span', class_='views').string.replace('浏览: ', '')
        
        # 构造字典
        news = {
            'title': title,
            'url': url,
            'author': author,
            'date': date,
            'summary': summary,
            'views': int(views)
        }
        
        news_list.append(news)
    
    # 打印结果
    print(f"✅ 共解析 {len(news_list)} 条新闻\n")
    for i, news in enumerate(news_list, 1):
        print(f"新闻 {i}:")
        print(f"  标题: {news['title']}")
        print(f"  链接: {news['url']}")
        print(f"  作者: {news['author']}")
        print(f"  日期: {news['date']}")
        print(f"  浏览: {news['views']}")
        print()


# ==================== 8. 实战：爬取真实网页 ====================

def crawl_real_website():
    """
    爬取真实网站示例（使用公开API）
    """
    print("=" * 60)
    print("8. 爬取真实网页示例")
    print("=" * 60)
    
    try:
        # 爬取示例网站（http://books.toscrape.com 是一个专门用于爬虫练习的网站）
        url = "http://books.toscrape.com/"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 解析书籍列表
        books = soup.select('.product_pod')
        print(f"✅ 找到 {len(books)} 本书\n")
        
        for i, book in enumerate(books[:5], 1):  # 只显示前5本
            # 标题
            title = book.select_one('h3 a').get('title')
            
            # 价格
            price = book.select_one('.price_color').string
            
            # 评分
            rating_class = book.select_one('.star-rating').get('class')[1]
            
            # 库存
            availability = book.select_one('.availability').string.strip()
            
            print(f"书籍 {i}:")
            print(f"  标题: {title}")
            print(f"  价格: {price}")
            print(f"  评分: {rating_class}")
            print(f"  库存: {availability}")
            print()
        
        print("✅ 爬取成功！")
        
    except Exception as e:
        print(f"❌ 爬取失败: {e}")


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

【练习1】解析电商商品
给定一个商品列表HTML，提取：
- 商品名称
- 价格
- 评分
- 评论数
- 商品图片链接

【练习2】表格数据提取
解析一个HTML表格，将数据转换为列表格式：
[
    ['姓名', '年龄', '城市'],
    ['张三', 25, '北京'],
    ['李四', 30, '上海']
]

【练习3】链接爬虫
爬取一个网页的所有链接，分类为：
- 站内链接（相对路径）
- 站外链接（绝对路径）
- 图片链接
- 文档链接（pdf, doc等）

【练习4】综合应用
爬取 http://books.toscrape.com/ 的多个分类
- 遍历所有分类
- 每个分类爬取前10本书
- 保存为JSON文件

提示：使用CSS选择器会更简洁！
    """)


# ==================== 主函数 ====================

def main():
    """
    主函数
    """
    print("\n" + "=" * 60)
    print("BeautifulSoup网页解析教程")
    print("=" * 60 + "\n")
    
    html_basics()
    bs4_basics()
    find_methods()
    css_selector()
    navigate_tree()
    extract_data()
    parse_news_example()
    crawl_real_website()
    exercises()
    
    print("=" * 60)
    print("✅ BeautifulSoup学习完成！")
    print("💡 核心要点：")
    print("   1. 使用find()和find_all()查找元素")
    print("   2. CSS选择器更简洁（推荐）")
    print("   3. 提取文本用.string或.get_text()")
    print("   4. 提取属性用.get()或['attr']")
    print("⏭️  下一步：学习 02_xpath.py")
    print("=" * 60)


if __name__ == "__main__":
    main()

