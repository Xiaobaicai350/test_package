"""
第二阶段 - XPath网页解析

XPath是一种在XML/HTML文档中查找信息的语言，功能强大
"""

from lxml import etree
import requests

# ==================== 1. XPath基础语法 ====================

def xpath_basics():
    """
    XPath基础语法讲解
    """
    print("=" * 60)
    print("1. XPath基础语法")
    print("=" * 60)
    
    print("""
XPath（XML Path Language）是查找XML/HTML节点的语言

【基本语法】
/     从根节点选择
//    选择所有匹配的节点（不考虑位置）
.     当前节点
..    父节点
@     选择属性

【常用表达式】
/html/body/div          从根开始的绝对路径
//div                   所有div元素
//div[@class='news']    class为news的div
//div[@id]              有id属性的div
//a/@href               所有a标签的href属性
//div[1]                第一个div（索引从1开始！）
//div[last()]           最后一个div
//div[position()<3]     前两个div

【谓词（条件）】
//div[@class='news']    属性等于
//div[contains(@class,'news')]  属性包含
//div[starts-with(@class,'news')]  属性开头
//p[text()='Python']    文本内容等于
//div[count(p)>2]       包含超过2个p标签

【运算符】
|     或（选择多个路径）
and   与
or    或

【示例】
//div[@class='news']//a/@href     选择class为news的div下所有a标签的href
//div[@class='news' or @class='hot']  选择class为news或hot的div
//p[@class='content' and @id='main']  同时满足两个条件
    """)


# ==================== 2. XPath基本使用 ====================

def xpath_basic_usage():
    """
    XPath基本使用示例
    """
    print("=" * 60)
    print("2. XPath基本使用")
    print("=" * 60)
    
    html = """
    <html>
        <body>
            <div class="container">
                <h1 id="title">新闻列表</h1>
                <div class="news">
                    <a href="/news/1">新闻标题1</a>
                    <span class="date">2024-01-01</span>
                </div>
                <div class="news">
                    <a href="/news/2">新闻标题2</a>
                    <span class="date">2024-01-02</span>
                </div>
                <div class="hot">
                    <a href="/news/3">热门新闻</a>
                </div>
            </div>
        </body>
    </html>
    """
    
    # 创建HTML树
    tree = etree.HTML(html)
    
    # 1. 选择所有div标签
    divs = tree.xpath('//div')
    print(f"✅ 所有div: {len(divs)}个")
    
    # 2. 选择class为news的div
    news_divs = tree.xpath('//div[@class="news"]')
    print(f"✅ class为news的div: {len(news_divs)}个")
    
    # 3. 获取h1标签的文本
    title = tree.xpath('//h1[@id="title"]/text()')
    print(f"✅ 标题: {title[0] if title else None}")
    
    # 4. 获取所有a标签的href属性
    hrefs = tree.xpath('//a/@href')
    print(f"✅ 所有链接: {hrefs}")
    
    # 5. 获取所有a标签的文本
    link_texts = tree.xpath('//a/text()')
    print(f"✅ 所有链接文本: {link_texts}")
    
    # 6. 选择第一个news div
    first_news = tree.xpath('//div[@class="news"][1]')
    print(f"✅ 第一个news div存在: {len(first_news) > 0}")
    
    # 7. 获取第一个news div下的a标签文本
    first_news_title = tree.xpath('//div[@class="news"][1]//a/text()')
    print(f"✅ 第一条新闻: {first_news_title[0] if first_news_title else None}")
    
    print()


# ==================== 3. XPath高级用法 ====================

def xpath_advanced():
    """
    XPath高级用法
    """
    print("=" * 60)
    print("3. XPath高级用法")
    print("=" * 60)
    
    html = """
    <div class="product-list">
        <div class="product hot-sale">
            <h3 class="product-title">iPhone 15 Pro</h3>
            <span class="price" data-value="7999">¥7999</span>
            <span class="rating">4.8</span>
        </div>
        <div class="product">
            <h3 class="product-title">MacBook Pro</h3>
            <span class="price" data-value="12999">¥12999</span>
            <span class="rating">4.9</span>
        </div>
        <div class="product new-arrival">
            <h3 class="product-title">iPad Air</h3>
            <span class="price" data-value="4999">¥4999</span>
            <span class="rating">4.7</span>
        </div>
    </div>
    """
    
    tree = etree.HTML(html)
    
    # 1. contains() - 属性包含某个值
    hot_products = tree.xpath('//div[contains(@class, "hot")]')
    print(f"✅ 热销商品(contains): {len(hot_products)}个")
    
    # 2. starts-with() - 属性以某个值开头
    product_titles = tree.xpath('//h3[starts-with(@class, "product")]')
    print(f"✅ 商品标题(starts-with): {len(product_titles)}个")
    
    # 3. text() - 选择文本节点
    all_text = tree.xpath('//h3/text()')
    print(f"✅ 所有标题: {all_text}")
    
    # 4. 获取data-*属性
    prices = tree.xpath('//span[@class="price"]/@data-value')
    print(f"✅ 所有价格: {prices}")
    
    # 5. 条件筛选 - 价格大于5000
    # XPath不支持直接的数值比较，需要先获取所有元素再在Python中处理
    expensive_products = tree.xpath('//span[@data-value]')
    print(f"✅ 有价格的商品: {len(expensive_products)}个")
    
    # 6. 多个条件（and）
    hot_new = tree.xpath('//div[contains(@class, "hot") or contains(@class, "new")]')
    print(f"✅ 热销或新品: {len(hot_new)}个")
    
    # 7. 父节点选择（..）
    # 找到评分4.9的商品的标题
    title = tree.xpath('//span[@class="rating" and text()="4.9"]/../h3/text()')
    print(f"✅ 评分4.9的商品: {title}")
    
    # 8. 兄弟节点选择（following-sibling::）
    # 找到标题后面的价格
    price_after_title = tree.xpath('//h3[@class="product-title"][1]/following-sibling::span[@class="price"]/text()')
    print(f"✅ 第一个商品价格: {price_after_title}")
    
    # 9. 轴（axis）- 更复杂的关系
    # ancestor:: 祖先节点
    # descendant:: 后代节点
    # following:: 当前节点之后的所有节点
    # preceding:: 当前节点之前的所有节点
    
    print()


# ==================== 4. XPath vs CSS选择器对比 ====================

def xpath_vs_css():
    """
    XPath和CSS选择器对比
    """
    print("=" * 60)
    print("4. XPath vs CSS选择器对比")
    print("=" * 60)
    
    print("""
【功能对比】

需求                    CSS选择器               XPath
-----------------------------------------------------------
选择所有div            div                     //div
选择class为news的div   .news                   //div[@class='news']
选择id为main的div      #main                   //div[@id='main']
选择第一个div          div:first-child         //div[1]
选择最后一个div        div:last-child          //div[last()]
选择第n个div           div:nth-child(n)        //div[n]
选择有href属性的a      a[href]                 //a[@href]
选择文本内容           (不支持)                //div[text()='xxx']
选择父节点             (不支持)                //div/..
获取属性值             (需要额外处理)          //a/@href
包含某个类             [class*='news']         //div[contains(@class,'news')]

【总结】
- CSS选择器：简洁，适合简单场景
- XPath：功能更强大，可以向上查找父节点，支持更复杂的逻辑

【建议】
- 简单查找：用CSS选择器（BeautifulSoup）
- 复杂逻辑：用XPath（lxml）
- 文本匹配：用XPath
- 需要父节点：用XPath
    """)


# ==================== 5. 实战：解析商品列表 ====================

def parse_products():
    """
    实战：使用XPath解析商品列表
    """
    print("=" * 60)
    print("5. 实战：解析商品列表")
    print("=" * 60)
    
    html = """
    <div class="shop-list">
        <div class="item" data-id="1">
            <img src="/img/product1.jpg" alt="商品1"/>
            <h3 class="title">Python编程入门</h3>
            <div class="info">
                <span class="price">¥89.00</span>
                <span class="sales">已售1000+</span>
            </div>
            <div class="rating">
                <span class="score">4.8</span>
                <span class="comments">200条评论</span>
            </div>
        </div>
        <div class="item" data-id="2">
            <img src="/img/product2.jpg" alt="商品2"/>
            <h3 class="title">Java核心技术</h3>
            <div class="info">
                <span class="price">¥128.00</span>
                <span class="sales">已售800+</span>
            </div>
            <div class="rating">
                <span class="score">4.9</span>
                <span class="comments">150条评论</span>
            </div>
        </div>
        <div class="item" data-id="3">
            <img src="/img/product3.jpg" alt="商品3"/>
            <h3 class="title">算法导论</h3>
            <div class="info">
                <span class="price">¥158.00</span>
                <span class="sales">已售500+</span>
            </div>
            <div class="rating">
                <span class="score">5.0</span>
                <span class="comments">80条评论</span>
            </div>
        </div>
    </div>
    """
    
    tree = etree.HTML(html)
    
    # 获取所有商品
    items = tree.xpath('//div[@class="item"]')
    print(f"✅ 共找到 {len(items)} 个商品\n")
    
    products = []
    for item in items:
        # 提取各字段（使用相对路径，从item开始）
        product_id = item.xpath('./@data-id')[0]
        title = item.xpath('.//h3[@class="title"]/text()')[0]
        price = item.xpath('.//span[@class="price"]/text()')[0]
        sales = item.xpath('.//span[@class="sales"]/text()')[0]
        score = item.xpath('.//span[@class="score"]/text()')[0]
        comments = item.xpath('.//span[@class="comments"]/text()')[0]
        img_url = item.xpath('.//img/@src')[0]
        
        product = {
            'id': product_id,
            'title': title.strip(),
            'price': price,
            'sales': sales,
            'score': float(score),
            'comments': comments,
            'image': img_url
        }
        
        products.append(product)
    
    # 打印结果
    for i, p in enumerate(products, 1):
        print(f"商品 {i}:")
        print(f"  ID: {p['id']}")
        print(f"  标题: {p['title']}")
        print(f"  价格: {p['price']}")
        print(f"  销量: {p['sales']}")
        print(f"  评分: {p['score']}")
        print(f"  评论: {p['comments']}")
        print(f"  图片: {p['image']}")
        print()


# ==================== 6. 实战：爬取真实网站 ====================

def crawl_with_xpath():
    """
    使用XPath爬取真实网站
    """
    print("=" * 60)
    print("6. 使用XPath爬取真实网站")
    print("=" * 60)
    
    try:
        url = "http://books.toscrape.com/"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 使用lxml解析
        tree = etree.HTML(response.text)
        
        # 提取书籍信息
        books = tree.xpath('//article[@class="product_pod"]')
        print(f"✅ 找到 {len(books)} 本书\n")
        
        for i, book in enumerate(books[:5], 1):
            # 标题（注意：title属性在a标签上）
            title = book.xpath('.//h3/a/@title')[0]
            
            # 价格
            price = book.xpath('.//p[@class="price_color"]/text()')[0]
            
            # 评分（在class属性中）
            rating_class = book.xpath('.//p[contains(@class, "star-rating")]/@class')[0]
            rating = rating_class.split()[-1]  # 提取评分等级
            
            # 链接
            link = book.xpath('.//h3/a/@href')[0]
            
            # 库存状态
            availability = book.xpath('.//p[@class="instock availability"]/text()')[1].strip()
            
            print(f"书籍 {i}:")
            print(f"  标题: {title}")
            print(f"  价格: {price}")
            print(f"  评分: {rating}")
            print(f"  链接: {link}")
            print(f"  库存: {availability}")
            print()
        
        print("✅ 爬取成功！")
        
    except Exception as e:
        print(f"❌ 爬取失败: {e}")


# ==================== 7. XPath调试技巧 ====================

def xpath_debugging():
    """
    XPath调试技巧
    """
    print("=" * 60)
    print("7. XPath调试技巧")
    print("=" * 60)
    
    print("""
【调试技巧】

1. 浏览器控制台测试
   - 打开Chrome开发者工具（F12）
   - 切换到Console标签
   - 使用 $x() 函数测试XPath
   
   例如：
   $x('//div[@class="news"]')           // 选择元素
   $x('//div[@class="news"]/text()')    // 选择文本
   $x('//a/@href')                      // 选择属性

2. 常见问题排查

问题1：返回空列表
- 检查HTML是否加载完整（可能是JavaScript渲染）
- 检查XPath表达式是否正确
- 检查大小写（HTML标签不区分，属性值区分）

问题2：获取不到文本
- 使用 /text() 获取直接文本
- 使用 //text() 获取所有后代文本
- 使用 string() 函数获取所有文本（XPath 1.0）

问题3：索引错误
- XPath索引从1开始（不是0！）
- [1] 表示第一个，不是 [0]

3. 实用工具
   - Chrome XPath Helper 插件
   - 在线XPath测试工具
   - lxml的tostring()查看解析后的HTML

4. 优化建议
   - 尽量使用相对路径（.//)而不是绝对路径
   - 避免使用太长的XPath
   - 使用contains()提高容错性
   - 先获取父元素，再在其内部查找子元素
    """)
    
    # 实际调试示例
    html = """
    <div class="container">
        <p>段落1</p>
        <div class="inner">
            <p>段落2</p>
        </div>
    </div>
    """
    
    tree = etree.HTML(html)
    
    print("\n【示例】")
    
    # 获取直接文本 vs 所有文本
    direct_text = tree.xpath('//div[@class="container"]/text()')
    all_text = tree.xpath('//div[@class="container"]//text()')
    
    print(f"直接文本 /text(): {[t.strip() for t in direct_text if t.strip()]}")
    print(f"所有文本 //text(): {[t.strip() for t in all_text if t.strip()]}")
    
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

【练习1】基础XPath
给定HTML，使用XPath提取：
- 所有h2标签的文本
- 所有class包含'highlight'的元素
- 第2个和第3个li元素
- 所有img标签的src属性

【练习2】复杂筛选
使用XPath选择：
- 价格大于100的商品（需要结合Python处理）
- 评分等于5星的商品
- 标题包含"Python"的文章
- 同时有class和id属性的div

【练习3】关系导航
使用XPath：
- 找到某个元素的父节点
- 找到某个元素的下一个兄弟节点
- 找到某个元素的所有祖先节点
- 找到评分最高的商品的标题

【练习4】实战项目
爬取 http://books.toscrape.com/
- 爬取所有分类链接
- 进入每个分类爬取书籍
- 提取：标题、价格、评分、库存
- 保存为JSON文件

提示：
- 先在浏览器Console用$x()测试表达式
- 使用Chrome开发者工具查看元素结构
- 注意索引从1开始！
    """)


# ==================== 主函数 ====================

def main():
    """
    主函数
    """
    print("\n" + "=" * 60)
    print("XPath网页解析教程")
    print("=" * 60 + "\n")
    
    xpath_basics()
    xpath_basic_usage()
    xpath_advanced()
    xpath_vs_css()
    parse_products()
    crawl_with_xpath()
    xpath_debugging()
    exercises()
    
    print("=" * 60)
    print("✅ XPath学习完成！")
    print("💡 核心要点：")
    print("   1. // 选择所有匹配节点")
    print("   2. [@attr='value'] 属性筛选")
    print("   3. /text() 获取文本，/@attr 获取属性")
    print("   4. contains() 模糊匹配")
    print("   5. XPath索引从1开始！")
    print("⏭️  下一步：学习 03_regex.py")
    print("=" * 60)


if __name__ == "__main__":
    main()

