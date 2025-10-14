"""
第三阶段实战 - 电商爬虫

项目：爬取电商网站的商品信息
技术：requests + XPath + 数据分析
"""

import requests
from lxml import etree
import json
import csv
import time
from typing import List, Dict
import os
from urllib.parse import urljoin

# ==================== 电商爬虫类 ====================

class EcommerceCrawler:
    """
    电商爬虫类
    
    功能：
    1. 爬取商品列表
    2. 提取商品详细信息
    3. 下载商品图片
    4. 数据分析统计
    """
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        self.products = []
        
        # 创建输出目录
        self.output_dir = "ecommerce_data"
        self.images_dir = os.path.join(self.output_dir, "images")
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
    
    def fetch(self, url: str, max_retries: int = 3) -> str:
        """获取网页内容"""
        for i in range(max_retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response.text
            except Exception as e:
                print(f"❌ 请求失败（{i+1}/{max_retries}）: {e}")
                if i < max_retries - 1:
                    time.sleep(2)
        return ""
    
    def parse_product_list(self, html: str) -> List[Dict]:
        """
        解析商品列表页
        """
        tree = etree.HTML(html)
        products = []
        
        # 使用XPath提取商品信息
        # 这里以books.toscrape.com为例
        product_nodes = tree.xpath('//article[@class="product_pod"]')
        
        for node in product_nodes:
            try:
                # 标题
                title = node.xpath('.//h3/a/@title')
                title = title[0] if title else ""
                
                # 价格
                price = node.xpath('.//p[@class="price_color"]/text()')
                price = price[0] if price else "0"
                
                # 评分
                rating_class = node.xpath('.//p[contains(@class, "star-rating")]/@class')
                if rating_class:
                    rating = rating_class[0].split()[-1]
                else:
                    rating = "Unknown"
                
                # 链接
                link = node.xpath('.//h3/a/@href')
                link = urljoin(self.base_url, link[0]) if link else ""
                
                # 图片
                image = node.xpath('.//img/@src')
                image = urljoin(self.base_url, image[0]) if image else ""
                
                # 库存
                stock = node.xpath('.//p[@class="instock availability"]/text()')
                stock = stock[1].strip() if len(stock) > 1 else "Unknown"
                
                product = {
                    'title': title,
                    'price': price,
                    'rating': rating,
                    'link': link,
                    'image': image,
                    'stock': stock
                }
                
                products.append(product)
                
            except Exception as e:
                print(f"⚠️ 解析商品失败: {e}")
                continue
        
        return products
    
    def download_image(self, url: str, filename: str) -> bool:
        """
        下载商品图片
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            filepath = os.path.join(self.images_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            print(f"⚠️ 下载图片失败 {url}: {e}")
            return False
    
    def crawl(self, start_page: int = 1, max_pages: int = 3):
        """
        执行爬取任务
        """
        print("=" * 60)
        print("🛒 开始爬取商品信息")
        print("=" * 60)
        
        for page in range(start_page, start_page + max_pages):
            print(f"\n📄 正在爬取第 {page} 页...")
            
            # 构造分页URL
            if page == 1:
                url = self.base_url
            else:
                url = f"{self.base_url}/catalogue/page-{page}.html"
            
            # 获取页面
            html = self.fetch(url)
            if not html:
                print(f"❌ 获取第 {page} 页失败")
                continue
            
            # 解析商品
            products = self.parse_product_list(html)
            print(f"✅ 找到 {len(products)} 个商品")
            
            # 下载图片（可选）
            for i, product in enumerate(products, 1):
                self.products.append(product)
                
                # 下载图片
                if product['image']:
                    img_filename = f"product_{len(self.products)}.jpg"
                    if self.download_image(product['image'], img_filename):
                        product['local_image'] = img_filename
                        print(f"  [{i}/{len(products)}] ✅ {product['title'][:30]}...")
                    else:
                        product['local_image'] = ""
                        print(f"  [{i}/{len(products)}] ⚠️ {product['title'][:30]}... (图片下载失败)")
                
                time.sleep(0.5)  # 延迟
            
            time.sleep(1)  # 页面间延迟
        
        print(f"\n🎉 爬取完成！共获取 {len(self.products)} 个商品")
    
    def save_to_json(self, filename: str = "products.json"):
        """保存为JSON"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON数据已保存到: {filepath}")
    
    def save_to_csv(self, filename: str = "products.csv"):
        """保存为CSV"""
        if not self.products:
            print("⚠️ 没有数据")
            return
        
        filepath = os.path.join(self.output_dir, filename)
        
        # 获取所有字段
        fieldnames = list(self.products[0].keys())
        
        with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.products)
        
        print(f"✅ CSV数据已保存到: {filepath}")
    
    def analyze(self):
        """数据分析"""
        if not self.products:
            print("⚠️ 没有数据")
            return
        
        print("\n" + "=" * 60)
        print("📊 数据分析")
        print("=" * 60)
        
        # 基本统计
        print(f"商品总数: {len(self.products)}")
        
        # 价格统计
        prices = []
        for p in self.products:
            price_str = p.get('price', '£0').replace('£', '').replace('$', '')
            try:
                price = float(price_str)
                prices.append(price)
            except:
                continue
        
        if prices:
            avg_price = sum(prices) / len(prices)
            max_price = max(prices)
            min_price = min(prices)
            
            print(f"\n价格统计:")
            print(f"  平均价格: £{avg_price:.2f}")
            print(f"  最高价格: £{max_price:.2f}")
            print(f"  最低价格: £{min_price:.2f}")
            
            # 找出最贵和最便宜的商品
            for p in self.products:
                price_str = p.get('price', '£0').replace('£', '').replace('$', '')
                try:
                    if float(price_str) == max_price:
                        print(f"  最贵商品: {p['title']} - {p['price']}")
                    if float(price_str) == min_price:
                        print(f"  最便宜: {p['title']} - {p['price']}")
                except:
                    pass
        
        # 评分统计
        ratings = {}
        for p in self.products:
            rating = p.get('rating', 'Unknown')
            ratings[rating] = ratings.get(rating, 0) + 1
        
        print(f"\n评分分布:")
        rating_order = ['Five', 'Four', 'Three', 'Two', 'One']
        for rating in rating_order:
            count = ratings.get(rating, 0)
            percentage = (count / len(self.products)) * 100
            print(f"  {rating} Star: {count} ({percentage:.1f}%)")
        
        # 库存统计
        in_stock = sum(1 for p in self.products if 'In stock' in p.get('stock', ''))
        print(f"\n库存统计:")
        print(f"  有货: {in_stock}")
        print(f"  无货: {len(self.products) - in_stock}")


# ==================== 示例使用 ====================

def example_ecommerce():
    """
    示例：爬取电商网站
    """
    print("\n" + "=" * 60)
    print("电商爬虫实战示例")
    print("=" * 60)
    
    # 创建爬虫实例
    crawler = EcommerceCrawler("http://books.toscrape.com")
    
    # 爬取数据
    crawler.crawl(start_page=1, max_pages=2)
    
    # 数据分析
    crawler.analyze()
    
    # 保存数据
    crawler.save_to_json()
    crawler.save_to_csv()
    
    print("\n✅ 完成！")


# ==================== 练习题 ====================

def exercises():
    """
    课后练习
    """
    print("\n" + "=" * 60)
    print("📝 课后练习")
    print("=" * 60 + "\n")
    
    print("""
【练习1】增强爬虫功能
在EcommerceCrawler基础上添加：
1. 商品详情页爬取（更多信息）
2. 商品分类爬取
3. 价格变动监控
4. 评论爬取

【练习2】数据可视化
使用matplotlib或pandas：
1. 绘制价格分布图
2. 绘制评分饼图
3. 生成商品对比表
4. 导出Excel报告

【练习3】智能分析
实现以下功能：
1. 性价比排序（评分/价格）
2. 热销商品识别
3. 价格异常检测
4. 推荐算法实现

【练习4】爬虫优化
优化项：
1. 实现断点续爬
2. 添加进度条显示
3. 支持多线程下载图片
4. 添加数据去重

提示：
- 使用pandas处理数据更方便
- matplotlib可以绘制图表
- 考虑添加日志系统
- 遵守网站爬虫协议
    """)


# ==================== 主函数 ====================

def main():
    """
    主函数
    """
    print("\n" + "=" * 60)
    print("第三阶段实战 - 电商爬虫")
    print("=" * 60)
    
    # 运行示例
    example_ecommerce()
    
    # 显示练习题
    exercises()
    
    print("\n" + "=" * 60)
    print("✅ 电商爬虫学习完成！")
    print("💡 核心要点：")
    print("   1. 使用XPath精确提取数据")
    print("   2. 批量下载图片资源")
    print("   3. 多格式数据存储（JSON/CSV）")
    print("   4. 数据统计分析")
    print("⏭️  下一步：学习 03_data_storage.py")
    print("=" * 60)


if __name__ == "__main__":
    main()

