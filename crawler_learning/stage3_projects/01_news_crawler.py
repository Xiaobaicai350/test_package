"""
第三阶段实战 - 新闻爬虫

项目：爬取新闻网站的文章列表和详情
技术：requests + BeautifulSoup + JSON存储
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
import os

# ==================== 配置类 ====================

class Config:
    """爬虫配置"""
    
    # 请求配置
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    
    TIMEOUT = 10  # 请求超时时间
    DELAY = 1  # 请求间隔（秒）
    MAX_RETRIES = 3  # 最大重试次数
    
    # 存储配置
    OUTPUT_DIR = "news_data"
    OUTPUT_FILE = "news_articles.json"


# ==================== 新闻爬虫类 ====================

class NewsCrawler:
    """
    新闻爬虫类
    
    功能：
    1. 爬取新闻列表
    2. 爬取新闻详情
    3. 数据清洗
    4. 保存数据
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(Config.HEADERS)
        self.articles = []
        
        # 创建输出目录
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        获取网页内容（带重试）
        
        Args:
            url: 目标URL
            
        Returns:
            网页HTML内容，失败返回None
        """
        for attempt in range(Config.MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=Config.TIMEOUT)
                response.raise_for_status()
                response.encoding = response.apparent_encoding  # 自动检测编码
                return response.text
            except Exception as e:
                print(f"❌ 请求失败（第{attempt + 1}次）: {e}")
                if attempt < Config.MAX_RETRIES - 1:
                    time.sleep(2)
                else:
                    return None
    
    def parse_list_page(self, html: str, base_url: str) -> List[Dict]:
        """
        解析列表页
        
        Args:
            html: 列表页HTML
            base_url: 基础URL（用于拼接相对路径）
            
        Returns:
            文章列表（包含标题、链接、摘要等）
        """
        soup = BeautifulSoup(html, 'html.parser')
        articles = []
        
        # 这里以示例网站为例（实际项目中根据目标网站调整选择器）
        # 假设新闻列表在 class='news-item' 的div中
        news_items = soup.find_all('div', class_='news-item')
        
        for item in news_items:
            try:
                # 提取标题和链接
                title_tag = item.find('a', class_='title')
                if not title_tag:
                    continue
                
                title = title_tag.get_text(strip=True)
                link = title_tag.get('href', '')
                
                # 处理相对路径
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = base_url + '/' + link
                
                # 提取其他信息
                author_tag = item.find('span', class_='author')
                author = author_tag.get_text(strip=True) if author_tag else "未知"
                
                date_tag = item.find('span', class_='date')
                pub_date = date_tag.get_text(strip=True) if date_tag else ""
                
                summary_tag = item.find('p', class_='summary')
                summary = summary_tag.get_text(strip=True) if summary_tag else ""
                
                article = {
                    'title': title,
                    'link': link,
                    'author': author,
                    'pub_date': pub_date,
                    'summary': summary,
                }
                
                articles.append(article)
                
            except Exception as e:
                print(f"⚠️ 解析文章失败: {e}")
                continue
        
        return articles
    
    def parse_detail_page(self, html: str) -> Dict:
        """
        解析详情页
        
        Args:
            html: 详情页HTML
            
        Returns:
            文章详细内容
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        try:
            # 提取正文（根据实际网站调整）
            content_tag = soup.find('div', class_='article-content')
            if content_tag:
                # 删除script和style标签
                for tag in content_tag.find_all(['script', 'style']):
                    tag.decompose()
                
                content = content_tag.get_text(separator='\n', strip=True)
            else:
                content = ""
            
            # 提取图片
            images = []
            img_tags = soup.find_all('img', class_='article-img')
            for img in img_tags:
                src = img.get('src', '')
                if src:
                    images.append(src)
            
            # 提取标签
            tags = []
            tag_elements = soup.find_all('a', class_='tag')
            for tag in tag_elements:
                tags.append(tag.get_text(strip=True))
            
            return {
                'content': content,
                'images': images,
                'tags': tags,
            }
            
        except Exception as e:
            print(f"⚠️ 解析详情失败: {e}")
            return {
                'content': '',
                'images': [],
                'tags': [],
            }
    
    def crawl_article_detail(self, article: Dict) -> Dict:
        """
        爬取文章详情
        
        Args:
            article: 文章基本信息
            
        Returns:
            完整的文章信息
        """
        print(f"📖 正在爬取: {article['title']}")
        
        html = self.fetch_page(article['link'])
        if not html:
            return article
        
        # 解析详情
        detail = self.parse_detail_page(html)
        article.update(detail)
        
        # 添加爬取时间
        article['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 延迟（避免请求过快）
        time.sleep(Config.DELAY)
        
        return article
    
    def crawl(self, list_url: str, max_pages: int = 1, max_articles: int = 10):
        """
        执行爬取任务
        
        Args:
            list_url: 列表页URL
            max_pages: 最大爬取页数
            max_articles: 每页最大爬取文章数
        """
        print("=" * 60)
        print("🚀 开始爬取新闻")
        print("=" * 60)
        
        base_url = '/'.join(list_url.split('/')[:3])
        
        for page in range(1, max_pages + 1):
            print(f"\n📄 正在爬取第 {page} 页...")
            
            # 构造分页URL（根据实际网站调整）
            if page == 1:
                url = list_url
            else:
                url = f"{list_url}?page={page}"
            
            # 获取列表页
            html = self.fetch_page(url)
            if not html:
                print(f"❌ 获取第 {page} 页失败")
                continue
            
            # 解析列表页
            articles = self.parse_list_page(html, base_url)
            print(f"✅ 找到 {len(articles)} 篇文章")
            
            # 爬取详情
            for i, article in enumerate(articles[:max_articles], 1):
                try:
                    full_article = self.crawl_article_detail(article)
                    self.articles.append(full_article)
                    print(f"✅ [{i}/{len(articles[:max_articles])}] 完成")
                except Exception as e:
                    print(f"❌ 爬取失败: {e}")
                    continue
            
            time.sleep(Config.DELAY)
        
        print(f"\n🎉 爬取完成！共获取 {len(self.articles)} 篇文章")
    
    def save_to_json(self, filename: Optional[str] = None):
        """
        保存数据到JSON文件
        
        Args:
            filename: 文件名（可选）
        """
        if not filename:
            filename = os.path.join(Config.OUTPUT_DIR, Config.OUTPUT_FILE)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.articles, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 数据已保存到: {filename}")
        except Exception as e:
            print(f"❌ 保存失败: {e}")
    
    def display_statistics(self):
        """显示统计信息"""
        if not self.articles:
            print("⚠️ 没有数据")
            return
        
        print("\n" + "=" * 60)
        print("📊 统计信息")
        print("=" * 60)
        print(f"文章总数: {len(self.articles)}")
        
        # 统计作者
        authors = {}
        for article in self.articles:
            author = article.get('author', '未知')
            authors[author] = authors.get(author, 0) + 1
        
        print(f"作者数量: {len(authors)}")
        print("热门作者:")
        for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  - {author}: {count}篇")
        
        # 统计标签
        all_tags = []
        for article in self.articles:
            all_tags.extend(article.get('tags', []))
        
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        if tag_counts:
            print("热门标签:")
            for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  - {tag}: {count}次")


# ==================== 示例：爬取模拟新闻网站 ====================

def example_simple_crawler():
    """
    简单示例：爬取示例网站
    """
    print("\n" + "=" * 60)
    print("示例1：简单新闻爬虫")
    print("=" * 60 + "\n")
    
    # 模拟新闻HTML（实际项目中是真实网站）
    sample_html = """
    <div class="news-list">
        <div class="news-item">
            <a href="/news/1" class="title">Python 3.12正式发布</a>
            <span class="author">技术编辑</span>
            <span class="date">2024-01-15</span>
            <p class="summary">Python 3.12带来了显著的性能提升...</p>
        </div>
        <div class="news-item">
            <a href="/news/2" class="title">AI技术突破性进展</a>
            <span class="author">科技记者</span>
            <span class="date">2024-01-16</span>
            <p class="summary">人工智能领域迎来重大突破...</p>
        </div>
    </div>
    """
    
    # 解析示例
    soup = BeautifulSoup(sample_html, 'html.parser')
    news_items = soup.find_all('div', class_='news-item')
    
    print(f"找到 {len(news_items)} 条新闻:\n")
    for i, item in enumerate(news_items, 1):
        title = item.find('a', class_='title').get_text()
        author = item.find('span', class_='author').get_text()
        date = item.find('span', class_='date').get_text()
        summary = item.find('p', class_='summary').get_text()
        
        print(f"新闻 {i}:")
        print(f"  标题: {title}")
        print(f"  作者: {author}")
        print(f"  日期: {date}")
        print(f"  摘要: {summary}")
        print()


# ==================== 实战：爬取真实网站 ====================

def example_real_crawler():
    """
    实战示例：爬取练习网站
    """
    print("\n" + "=" * 60)
    print("示例2：爬取真实网站（http://books.toscrape.com）")
    print("=" * 60 + "\n")
    
    try:
        url = "http://books.toscrape.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取书籍信息
        books = soup.select('.product_pod')
        
        book_list = []
        for book in books[:5]:  # 只显示前5本
            title = book.select_one('h3 a')['title']
            price = book.select_one('.price_color').get_text()
            rating = book.select_one('.star-rating')['class'][1]
            link = book.select_one('h3 a')['href']
            
            book_data = {
                'title': title,
                'price': price,
                'rating': rating,
                'link': url + 'catalogue/' + link
            }
            book_list.append(book_data)
        
        # 显示结果
        print(f"✅ 成功爬取 {len(book_list)} 本书:\n")
        for i, book in enumerate(book_list, 1):
            print(f"书籍 {i}:")
            print(f"  标题: {book['title']}")
            print(f"  价格: {book['price']}")
            print(f"  评分: {book['rating']}")
            print(f"  链接: {book['link']}")
            print()
        
        # 保存到JSON
        output_file = os.path.join(Config.OUTPUT_DIR, "books_sample.json")
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(book_list, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 数据已保存到: {output_file}")
        
    except Exception as e:
        print(f"❌ 爬取失败: {e}")


# ==================== 练习题 ====================

def exercises():
    """
    课后练习
    """
    print("\n" + "=" * 60)
    print("📝 课后练习")
    print("=" * 60 + "\n")
    
    print("""
【练习1】完善新闻爬虫
基于NewsCrawler类：
1. 添加分类爬取功能（科技、财经、体育等）
2. 添加关键词搜索功能
3. 添加去重功能（避免重复爬取）
4. 添加日志记录

【练习2】爬取不同网站
选择以下网站之一进行爬取：
1. http://quotes.toscrape.com/ - 名言网站
2. http://books.toscrape.com/ - 图书网站
要求：
- 爬取至少3页数据
- 保存为JSON格式
- 添加错误处理
- 显示爬取进度

【练习3】数据分析
基于爬取的数据：
1. 统计最常见的标签/分类
2. 找出最热门的作者
3. 分析发布时间分布
4. 生成数据报告

【练习4】优化爬虫
优化方面：
1. 添加断点续爬功能
2. 实现增量爬取（只爬新内容）
3. 添加代理IP支持
4. 实现并发爬取（多线程）

提示：
- 先分析网站结构（F12开发者工具）
- 确定数据在哪个标签里
- 从小规模测试开始
- 遵守网站的robots.txt协议
    """)


# ==================== 主函数 ====================

def main():
    """
    主函数
    """
    print("\n" + "=" * 60)
    print("第三阶段实战 - 新闻爬虫")
    print("=" * 60)
    
    # 运行示例
    example_simple_crawler()
    example_real_crawler()
    
    # 显示练习题
    exercises()
    
    print("\n" + "=" * 60)
    print("✅ 新闻爬虫学习完成！")
    print("💡 核心流程：")
    print("   1. 爬取列表页获取文章链接")
    print("   2. 进入详情页获取完整内容")
    print("   3. 数据清洗和结构化")
    print("   4. 保存为JSON文件")
    print("⏭️  下一步：学习 02_ecommerce_crawler.py")
    print("=" * 60)


if __name__ == "__main__":
    main()

