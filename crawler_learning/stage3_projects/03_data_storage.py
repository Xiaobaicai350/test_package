"""
第三阶段实战 - 数据存储

项目：学习爬虫数据的各种存储方式
技术：CSV、JSON、Excel、MySQL
"""

import json
import csv
import os
from typing import List, Dict
from datetime import datetime

# ==================== 1. JSON存储 ====================

class JsonStorage:
    """
    JSON格式存储
    
    优点：
    - 结构化，可嵌套
    - 易读易写
    - 支持复杂数据类型
    
    缺点：
    - 文件较大
    - 不适合超大数据
    """
    
    @staticmethod
    def save(data: List[Dict], filename: str):
        """
        保存数据到JSON文件
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ JSON保存成功: {filename}")
        except Exception as e:
            print(f"❌ JSON保存失败: {e}")
    
    @staticmethod
    def load(filename: str) -> List[Dict]:
        """
        从JSON文件加载数据
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ JSON加载成功: {filename}")
            return data
        except Exception as e:
            print(f"❌ JSON加载失败: {e}")
            return []
    
    @staticmethod
    def append(new_data: Dict, filename: str):
        """
        追加数据到JSON文件
        """
        # 先加载现有数据
        if os.path.exists(filename):
            data = JsonStorage.load(filename)
        else:
            data = []
        
        # 追加新数据
        data.append(new_data)
        
        # 保存
        JsonStorage.save(data, filename)


# ==================== 2. CSV存储 ====================

class CsvStorage:
    """
    CSV格式存储
    
    优点：
    - 文件小
    - Excel可直接打开
    - 通用性强
    
    缺点：
    - 不支持嵌套结构
    - 类型信息丢失
    """
    
    @staticmethod
    def save(data: List[Dict], filename: str):
        """
        保存数据到CSV文件
        """
        if not data:
            print("⚠️ 没有数据")
            return
        
        try:
            # 获取所有字段名
            fieldnames = list(data[0].keys())
            
            with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            print(f"✅ CSV保存成功: {filename}")
        except Exception as e:
            print(f"❌ CSV保存失败: {e}")
    
    @staticmethod
    def load(filename: str) -> List[Dict]:
        """
        从CSV文件加载数据
        """
        try:
            data = []
            with open(filename, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(dict(row))
            
            print(f"✅ CSV加载成功: {filename}")
            return data
        except Exception as e:
            print(f"❌ CSV加载失败: {e}")
            return []
    
    @staticmethod
    def append(new_data: Dict, filename: str):
        """
        追加数据到CSV文件
        """
        try:
            # 检查文件是否存在
            file_exists = os.path.exists(filename)
            
            with open(filename, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=new_data.keys())
                
                # 如果文件不存在，写入表头
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(new_data)
            
            print(f"✅ CSV追加成功")
        except Exception as e:
            print(f"❌ CSV追加失败: {e}")


# ==================== 3. 文本文件存储 ====================

class TextStorage:
    """
    纯文本存储
    
    适用场景：
    - 日志记录
    - 简单文本数据
    """
    
    @staticmethod
    def save(data: str, filename: str):
        """保存文本"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(data)
            print(f"✅ 文本保存成功: {filename}")
        except Exception as e:
            print(f"❌ 文本保存失败: {e}")
    
    @staticmethod
    def append(data: str, filename: str):
        """追加文本"""
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(data + '\n')
        except Exception as e:
            print(f"❌ 文本追加失败: {e}")


# ==================== 4. MySQL存储（示例） ====================

class MySQLStorage:
    """
    MySQL数据库存储
    
    优点：
    - 支持大数据量
    - 支持复杂查询
    - 数据安全性高
    
    缺点：
    - 需要安装数据库
    - 配置相对复杂
    
    注意：需要安装 pymysql: pip install pymysql
    """
    
    def __init__(self, host='localhost', port=3306, user='root', 
                 password='', database='crawler_db'):
        """
        初始化数据库连接
        """
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database
        }
        self.conn = None
    
    def connect(self):
        """连接数据库"""
        try:
            import pymysql
            self.conn = pymysql.connect(**self.config)
            print("✅ 数据库连接成功")
            return True
        except ImportError:
            print("⚠️ 请先安装pymysql: pip install pymysql")
            return False
        except Exception as e:
            print(f"❌ 数据库连接失败: {e}")
            return False
    
    def create_table(self, table_name: str):
        """
        创建表（示例）
        """
        if not self.conn:
            print("⚠️ 未连接数据库")
            return
        
        try:
            cursor = self.conn.cursor()
            
            sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                price DECIMAL(10, 2),
                rating VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            cursor.execute(sql)
            self.conn.commit()
            print(f"✅ 表 {table_name} 创建成功")
        except Exception as e:
            print(f"❌ 创建表失败: {e}")
    
    def insert(self, table_name: str, data: Dict):
        """
        插入数据
        """
        if not self.conn:
            print("⚠️ 未连接数据库")
            return
        
        try:
            cursor = self.conn.cursor()
            
            # 构造SQL
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            cursor.execute(sql, list(data.values()))
            self.conn.commit()
            print(f"✅ 数据插入成功")
        except Exception as e:
            print(f"❌ 数据插入失败: {e}")
    
    def query(self, table_name: str, limit: int = 10) -> List[Dict]:
        """
        查询数据
        """
        if not self.conn:
            print("⚠️ 未连接数据库")
            return []
        
        try:
            cursor = self.conn.cursor()
            
            sql = f"SELECT * FROM {table_name} LIMIT {limit}"
            cursor.execute(sql)
            
            # 获取列名
            columns = [desc[0] for desc in cursor.description]
            
            # 构造字典列表
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            print(f"✅ 查询成功，返回 {len(results)} 条记录")
            return results
        except Exception as e:
            print(f"❌ 查询失败: {e}")
            return []
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()
            print("✅ 数据库连接已关闭")


# ==================== 5. 存储管理类 ====================

class StorageManager:
    """
    存储管理类（统一接口）
    """
    
    def __init__(self, storage_type: str = 'json'):
        """
        初始化
        
        Args:
            storage_type: 存储类型 (json/csv/mysql)
        """
        self.storage_type = storage_type
        self.output_dir = "crawler_data"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def save(self, data: List[Dict], name: str = "data"):
        """
        保存数据（自动选择格式）
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if self.storage_type == 'json':
            filename = os.path.join(self.output_dir, f"{name}_{timestamp}.json")
            JsonStorage.save(data, filename)
        
        elif self.storage_type == 'csv':
            filename = os.path.join(self.output_dir, f"{name}_{timestamp}.csv")
            CsvStorage.save(data, filename)
        
        elif self.storage_type == 'both':
            # 同时保存为JSON和CSV
            json_file = os.path.join(self.output_dir, f"{name}_{timestamp}.json")
            csv_file = os.path.join(self.output_dir, f"{name}_{timestamp}.csv")
            JsonStorage.save(data, json_file)
            CsvStorage.save(data, csv_file)
        
        else:
            print(f"⚠️ 不支持的存储类型: {self.storage_type}")


# ==================== 示例和测试 ====================

def example_storage():
    """
    存储示例
    """
    print("\n" + "=" * 60)
    print("数据存储示例")
    print("=" * 60 + "\n")
    
    # 示例数据
    products = [
        {
            'title': 'Python编程入门',
            'price': 89.00,
            'rating': 'Five',
            'author': '张三',
            'pub_date': '2024-01-01'
        },
        {
            'title': 'Java核心技术',
            'price': 128.00,
            'rating': 'Four',
            'author': '李四',
            'pub_date': '2024-01-02'
        },
        {
            'title': '算法导论',
            'price': 158.00,
            'rating': 'Five',
            'author': '王五',
            'pub_date': '2024-01-03'
        }
    ]
    
    output_dir = "storage_examples"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. JSON存储
    print("1️⃣ JSON存储")
    json_file = os.path.join(output_dir, "products.json")
    JsonStorage.save(products, json_file)
    loaded_json = JsonStorage.load(json_file)
    print(f"   加载数据: {len(loaded_json)} 条\n")
    
    # 2. CSV存储
    print("2️⃣ CSV存储")
    csv_file = os.path.join(output_dir, "products.csv")
    CsvStorage.save(products, csv_file)
    loaded_csv = CsvStorage.load(csv_file)
    print(f"   加载数据: {len(loaded_csv)} 条\n")
    
    # 3. 追加数据
    print("3️⃣ 追加数据")
    new_product = {
        'title': 'Web开发实战',
        'price': 99.00,
        'rating': 'Four',
        'author': '赵六',
        'pub_date': '2024-01-04'
    }
    JsonStorage.append(new_product, json_file)
    CsvStorage.append(new_product, csv_file)
    
    # 4. 使用管理类
    print("\n4️⃣ 使用存储管理类")
    manager = StorageManager(storage_type='both')
    manager.save(products, name="managed_products")
    
    print("\n✅ 所有示例执行完成！")
    print(f"📁 文件保存在: {output_dir}/")


# ==================== 存储方式对比 ====================

def storage_comparison():
    """
    存储方式对比
    """
    print("\n" + "=" * 60)
    print("📊 存储方式对比")
    print("=" * 60 + "\n")
    
    comparison = """
存储方式       适用场景              优点                  缺点
─────────────────────────────────────────────────────────────
JSON        小中型数据            结构化、易读          文件较大
            配置文件              支持嵌套              
            API数据              

CSV         表格数据              文件小                不支持嵌套
            Excel分析            通用性强              类型丢失
            简单列表              

TXT         日志文件              简单快速              无结构
            临时数据              占用极小              不便查询

MySQL       大量数据              支持查询              需要安装
            复杂关系              高性能                配置复杂
            多用户访问            数据安全              

MongoDB     文档数据              灵活模式              需要学习
            大数据                高扩展性              占用大

Redis       缓存数据              极速读写              内存限制
            临时状态              支持丰富类型          数据易失

【推荐方案】
- 学习测试：JSON/CSV
- 小型项目：JSON + CSV
- 中型项目：MySQL
- 大型项目：MySQL + Redis
- 超大规模：分布式数据库
    """
    
    print(comparison)


# ==================== 练习题 ====================

def exercises():
    """
    课后练习
    """
    print("\n" + "=" * 60)
    print("📝 课后练习")
    print("=" * 60 + "\n")
    
    print("""
【练习1】实现Excel存储
使用openpyxl或pandas：
1. 保存数据到Excel
2. 支持多个Sheet
3. 添加样式（标题行加粗、颜色）
4. 自动调整列宽

【练习2】实现SQLite存储
使用SQLite（无需安装）：
1. 创建数据库和表
2. 插入爬虫数据
3. 实现CRUD操作
4. 导出为CSV

【练习3】数据去重
实现去重功能：
1. 基于URL去重
2. 基于标题去重
3. 保存去重日志
4. 支持增量更新

【练习4】数据转换
实现格式转换：
1. JSON转CSV
2. CSV转Excel
3. 数据库导出为JSON
4. 批量处理多个文件

【练习5】综合项目
完整爬虫项目：
1. 爬取数据
2. 清洗处理
3. 多格式存储
4. 数据可视化报告

提示：
- SQLite适合学习，无需安装
- pandas处理数据很方便
- 考虑添加备份机制
- 大数据量时注意内存
    """)


# ==================== 主函数 ====================

def main():
    """
    主函数
    """
    print("\n" + "=" * 60)
    print("第三阶段实战 - 数据存储")
    print("=" * 60)
    
    # 运行示例
    example_storage()
    
    # 显示对比
    storage_comparison()
    
    # 显示练习
    exercises()
    
    print("\n" + "=" * 60)
    print("✅ 数据存储学习完成！")
    print("💡 核心要点：")
    print("   1. JSON适合结构化小数据")
    print("   2. CSV适合表格数据和Excel分析")
    print("   3. MySQL适合大量数据和复杂查询")
    print("   4. 根据项目规模选择存储方式")
    print("⏭️  下一步：进入第四阶段学习动态网页爬取")
    print("=" * 60)


if __name__ == "__main__":
    main()

