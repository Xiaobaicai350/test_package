"""
第六阶段 - IP代理池

实现一个完整的代理池系统
"""

import requests
import time
from typing import List, Dict, Optional
import random

# ==================== 1. 代理池设计 ====================

def proxy_pool_design():
    """
    代理池设计思路
    """
    print("=" * 60)
    print("1. 代理池设计")
    print("=" * 60 + "\n")
    
    print("""
【代理池架构】

┌─────────────┐
│ 代理爬取模块  │ → 从免费网站爬取代理
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 代理存储模块  │ → 存储到数据库/内存
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 代理检测模块  │ → 定时检测可用性
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 代理提供模块  │ → 提供API接口
└─────────────┘

【核心功能】

1. 代理获取
   - 爬取免费代理网站
   - 支持多个来源
   - 自动去重

2. 代理验证
   - 检测是否可用
   - 测试响应速度
   - 匿名度检测

3. 代理维护
   - 定时清理失效代理
   - 动态更新代理池
   - 计分机制

4. 代理提供
   - 随机获取
   - 按速度排序
   - API接口

【数据结构】

Proxy:
  - ip: IP地址
  - port: 端口
  - protocol: 协议(http/https)
  - speed: 速度(ms)
  - score: 评分(0-100)
  - last_check: 最后检测时间
  - fail_count: 失败次数
    """)


# ==================== 2. 代理类 ====================

class Proxy:
    """
    代理对象
    """
    
    def __init__(self, ip: str, port: int, protocol: str = "http"):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.speed = 0  # 响应时间(ms)
        self.score = 100  # 初始评分
        self.fail_count = 0
        self.last_check = 0
    
    @property
    def url(self) -> str:
        """返回代理URL"""
        return f"{self.protocol}://{self.ip}:{self.port}"
    
    @property
    def dict(self) -> Dict:
        """返回requests使用的格式"""
        return {
            "http": self.url,
            "https": self.url,
        }
    
    def __str__(self):
        return f"{self.ip}:{self.port} (score:{self.score}, speed:{self.speed}ms)"


# ==================== 3. 代理池类 ====================

class ProxyPool:
    """
    代理池管理类
    """
    
    def __init__(self):
        self.proxies: List[Proxy] = []
        self.test_url = "http://httpbin.org/ip"  # 测试URL
    
    def add_proxy(self, proxy: Proxy):
        """添加代理"""
        # 去重
        for p in self.proxies:
            if p.ip == proxy.ip and p.port == proxy.port:
                return
        
        self.proxies.append(proxy)
        print(f"✅ 添加代理: {proxy}")
    
    def test_proxy(self, proxy: Proxy, timeout: int = 5) -> bool:
        """
        测试代理是否可用
        
        Returns:
            True: 可用
            False: 不可用
        """
        try:
            start_time = time.time()
            
            response = requests.get(
                self.test_url,
                proxies=proxy.dict,
                timeout=timeout
            )
            
            elapsed = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                proxy.speed = int(elapsed)
                proxy.fail_count = 0
                proxy.score = min(100, proxy.score + 10)
                proxy.last_check = time.time()
                return True
            else:
                proxy.fail_count += 1
                proxy.score = max(0, proxy.score - 20)
                return False
                
        except Exception as e:
            proxy.fail_count += 1
            proxy.score = max(0, proxy.score - 20)
            return False
    
    def validate_all(self):
        """验证所有代理"""
        print(f"\n🔍 开始验证 {len(self.proxies)} 个代理...")
        
        valid_count = 0
        for i, proxy in enumerate(self.proxies, 1):
            print(f"[{i}/{len(self.proxies)}] 测试 {proxy.ip}:{proxy.port}...", end=" ")
            
            if self.test_proxy(proxy):
                print(f"✅ 可用 ({proxy.speed}ms)")
                valid_count += 1
            else:
                print("❌ 失败")
            
            time.sleep(0.5)  # 避免请求过快
        
        print(f"\n✅ 验证完成！可用: {valid_count}/{len(self.proxies)}")
        
        # 清理评分过低的代理
        self.clean_bad_proxies()
    
    def clean_bad_proxies(self, min_score: int = 20):
        """清理低分代理"""
        before_count = len(self.proxies)
        self.proxies = [p for p in self.proxies if p.score >= min_score]
        after_count = len(self.proxies)
        
        if before_count > after_count:
            print(f"🗑️  清理了 {before_count - after_count} 个低分代理")
    
    def get_proxy(self, random_choice: bool = True) -> Optional[Proxy]:
        """
        获取一个代理
        
        Args:
            random_choice: True=随机，False=最快的
        """
        if not self.proxies:
            return None
        
        if random_choice:
            return random.choice(self.proxies)
        else:
            # 返回速度最快且评分高的
            valid_proxies = [p for p in self.proxies if p.score > 50]
            if not valid_proxies:
                return None
            return min(valid_proxies, key=lambda x: x.speed)
    
    def get_all_proxies(self, min_score: int = 50) -> List[Proxy]:
        """获取所有高分代理"""
        return [p for p in self.proxies if p.score >= min_score]
    
    def statistics(self):
        """统计信息"""
        if not self.proxies:
            print("⚠️ 代理池为空")
            return
        
        print("\n" + "=" * 60)
        print("📊 代理池统计")
        print("=" * 60)
        print(f"总代理数: {len(self.proxies)}")
        
        # 按评分分类
        excellent = len([p for p in self.proxies if p.score >= 80])
        good = len([p for p in self.proxies if 50 <= p.score < 80])
        bad = len([p for p in self.proxies if p.score < 50])
        
        print(f"优秀(≥80分): {excellent}")
        print(f"良好(50-79分): {good}")
        print(f"较差(<50分): {bad}")
        
        # 平均速度
        avg_speed = sum(p.speed for p in self.proxies) / len(self.proxies)
        print(f"平均响应: {avg_speed:.0f}ms")
        
        # 最快代理
        fastest = min(self.proxies, key=lambda x: x.speed if x.speed > 0 else float('inf'))
        print(f"最快代理: {fastest}")


# ==================== 4. 代理爬取 ====================

def crawl_free_proxies():
    """
    爬取免费代理
    
    注意：免费代理质量不高，仅供学习
    """
    print("\n" + "=" * 60)
    print("4. 爬取免费代理")
    print("=" * 60 + "\n")
    
    print("""
【免费代理网站】

1. https://www.kuaidaili.com/free/
2. https://www.89ip.cn/
3. https://www.xicidaili.com/
4. http://www.66ip.cn/

【爬取示例】
    """)
    
    example = '''
from bs4 import BeautifulSoup
import requests

def crawl_kuaidaili():
    """爬取快代理"""
    url = "https://www.kuaidaili.com/free/"
    headers = {
        "User-Agent": "Mozilla/5.0 ..."
    }
    
    proxies_list = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 解析表格
        rows = soup.select('table tbody tr')
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                ip = cols[0].text.strip()
                port = int(cols[1].text.strip())
                protocol = cols[3].text.strip().lower()
                
                proxy = Proxy(ip, port, protocol)
                proxies_list.append(proxy)
        
        return proxies_list
        
    except Exception as e:
        print(f"爬取失败: {e}")
        return []

# 使用
proxies = crawl_kuaidaili()
for proxy in proxies:
    pool.add_proxy(proxy)
    '''
    
    print(example)


# ==================== 5. 使用示例 ====================

def usage_example():
    """
    使用示例
    """
    print("\n" + "=" * 60)
    print("5. 使用示例")
    print("=" * 60 + "\n")
    
    # 创建代理池
    pool = ProxyPool()
    
    # 手动添加一些测试代理（实际应该爬取）
    test_proxies = [
        Proxy("8.8.8.8", 8080),  # 示例（不可用）
        Proxy("1.1.1.1", 8080),  # 示例（不可用）
    ]
    
    for proxy in test_proxies:
        pool.add_proxy(proxy)
    
    # 验证代理
    # pool.validate_all()  # 实际运行时取消注释
    
    # 统计信息
    # pool.statistics()
    
    print("""
【在爬虫中使用代理池】

# 创建代理池
pool = ProxyPool()

# 添加代理
proxies = crawl_free_proxies()
for proxy in proxies:
    pool.add_proxy(proxy)

# 验证代理
pool.validate_all()

# 使用代理爬取
def fetch_with_proxy(url):
    max_retries = 3
    
    for i in range(max_retries):
        proxy = pool.get_proxy()  # 获取代理
        
        if not proxy:
            print("⚠️ 没有可用代理")
            return None
        
        try:
            response = requests.get(
                url,
                proxies=proxy.dict,
                timeout=10
            )
            
            if response.status_code == 200:
                # 成功，增加代理评分
                proxy.score = min(100, proxy.score + 5)
                return response.text
            
        except Exception as e:
            print(f"❌ 代理失败: {proxy.ip}:{proxy.port}")
            # 失败，降低代理评分
            proxy.score = max(0, proxy.score - 10)
            proxy.fail_count += 1
    
    return None

# 爬取数据
html = fetch_with_proxy("https://example.com")
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
【练习1】完善代理池
增强ProxyPool类：
1. 持久化存储（Redis/SQLite）
2. 定时自动更新
3. API接口（Flask）
4. 并发测试代理

【练习2】爬取多个代理源
实现多源爬取：
1. 爬取3-5个免费代理网站
2. 合并去重
3. 批量验证
4. 保存高质量代理

【练习3】智能评分系统
优化评分机制：
1. 根据速度评分
2. 根据成功率评分
3. 根据匿名度评分
4. 综合评分排序

【练习4】代理API服务
实现Web API：
1. GET /proxy - 获取随机代理
2. GET /proxy/all - 获取所有代理
3. POST /proxy/test - 测试代理
4. GET /proxy/stats - 统计信息

【练习5】生产级代理池
完整项目：
1. 多源爬取
2. 并发测试
3. 持久化存储
4. 定时更新（每小时）
5. Web管理界面
6. 接口文档

提示：
- 免费代理质量不高
- 考虑使用付费代理
- Redis适合存储代理
- 使用多线程测试
- 添加监控和日志
    """)


# ==================== 主函数 ====================

def main():
    """
    主函数
    """
    print("\n" + "=" * 60)
    print("第六阶段 - IP代理池")
    print("=" * 60)
    
    proxy_pool_design()
    crawl_free_proxies()
    usage_example()
    exercises()
    
    print("\n" + "=" * 60)
    print("✅ 代理池学习完成！")
    print("💡 核心要点：")
    print("   1. 代理池四大模块：获取、验证、维护、提供")
    print("   2. 评分机制管理代理质量")
    print("   3. 定时检测清理失效代理")
    print("   4. 免费代理质量低，生产环境用付费")
    print("\n🎉 恭喜！完成全部6个阶段的爬虫学习！")
    print("=" * 60)


if __name__ == "__main__":
    main()

