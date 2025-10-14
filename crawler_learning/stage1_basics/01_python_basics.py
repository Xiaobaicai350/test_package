"""
第一阶段 - Python基础速成（针对Java开发者）

本文件包含Python基础语法，帮助有Java基础的开发者快速上手Python
"""

# ==================== 1. 数据类型对比 ====================

def data_types_demo():
    """
    Python基础数据类型演示
    类比Java：int, String, List, Map, Set
    """
    print("=" * 50)
    print("1. Python数据类型演示")
    print("=" * 50)
    
    # 整数和浮点数（无需声明类型）
    age = 25  # Java: int age = 25;
    price = 99.99  # Java: double price = 99.99;
    
    # 字符串（支持单引号和双引号）
    name = "Python爬虫"  # Java: String name = "Python爬虫";
    
    # 布尔值（首字母大写）
    is_active = True  # Java: boolean isActive = true;
    
    # 列表（类似Java的ArrayList）
    numbers = [1, 2, 3, 4, 5]  # Java: List<Integer> numbers = new ArrayList<>();
    mixed = [1, "hello", 3.14, True]  # Python支持混合类型
    
    # 字典（类似Java的HashMap）
    person = {  # Java: Map<String, Object> person = new HashMap<>();
        "name": "张三",
        "age": 28,
        "skills": ["Python", "Java", "爬虫"]
    }
    
    # 元组（不可变列表）
    coordinates = (10, 20)  # Java中没有直接对应的类型
    
    # 集合（类似Java的HashSet）
    unique_numbers = {1, 2, 3, 4, 5}  # Java: Set<Integer> = new HashSet<>();
    
    # 打印结果
    print(f"姓名: {name}, 年龄: {age}, 价格: {price}")
    print(f"列表: {numbers}")
    print(f"字典: {person}")
    print(f"集合: {unique_numbers}")
    print()


# ==================== 2. 字符串操作 ====================

def string_operations():
    """
    Python字符串操作（比Java更简洁）
    """
    print("=" * 50)
    print("2. 字符串操作")
    print("=" * 50)
    
    text = "  Python Web Crawler  "
    
    # Java: text.toLowerCase()
    print(f"小写: {text.lower()}")
    
    # Java: text.toUpperCase()
    print(f"大写: {text.upper()}")
    
    # Java: text.trim()
    print(f"去空格: '{text.strip()}'")
    
    # Java: text.replace("Python", "Java")
    print(f"替换: {text.replace('Python', 'Java')}")
    
    # Java: text.split(" ")
    words = text.strip().split(" ")
    print(f"分割: {words}")
    
    # 字符串格式化（Python特色）
    name = "小明"
    age = 25
    
    # 方式1: f-string（推荐）
    message1 = f"{name}今年{age}岁"
    
    # 方式2: format方法
    message2 = "{}今年{}岁".format(name, age)
    
    # 方式3: %格式化（旧式）
    message3 = "%s今年%d岁" % (name, age)
    
    print(f"格式化: {message1}")
    print()


# ==================== 3. 列表操作 ====================

def list_operations():
    """
    列表操作（类比Java的ArrayList）
    """
    print("=" * 50)
    print("3. 列表操作")
    print("=" * 50)
    
    # 创建列表
    fruits = ["苹果", "香蕉", "橙子"]
    
    # 添加元素 - Java: list.add()
    fruits.append("葡萄")
    print(f"添加后: {fruits}")
    
    # 插入元素 - Java: list.add(index, element)
    fruits.insert(1, "草莓")
    print(f"插入后: {fruits}")
    
    # 删除元素 - Java: list.remove()
    fruits.remove("香蕉")
    print(f"删除后: {fruits}")
    
    # 获取元素 - Java: list.get(0)
    first = fruits[0]
    print(f"第一个元素: {first}")
    
    # 切片（Python特色）
    subset = fruits[1:3]  # 获取索引1到2的元素
    print(f"切片[1:3]: {subset}")
    
    # 列表推导式（Python特色，非常强大）
    numbers = [1, 2, 3, 4, 5]
    # Java: 需要for循环
    squares = [n ** 2 for n in numbers]  # 计算平方
    print(f"平方列表: {squares}")
    
    # 带条件的列表推导式
    even_numbers = [n for n in numbers if n % 2 == 0]
    print(f"偶数: {even_numbers}")
    print()


# ==================== 4. 字典操作 ====================

def dict_operations():
    """
    字典操作（类比Java的HashMap）
    """
    print("=" * 50)
    print("4. 字典操作")
    print("=" * 50)
    
    # 创建字典
    student = {
        "name": "李华",
        "age": 20,
        "major": "计算机科学"
    }
    
    # 获取值 - Java: map.get("name")
    name = student.get("name")
    print(f"姓名: {name}")
    
    # 添加/修改 - Java: map.put("grade", "A")
    student["grade"] = "A"
    print(f"添加成绩后: {student}")
    
    # 删除 - Java: map.remove("age")
    del student["age"]
    print(f"删除年龄后: {student}")
    
    # 遍历 - Java: for(Map.Entry entry : map.entrySet())
    print("遍历字典:")
    for key, value in student.items():
        print(f"  {key}: {value}")
    
    # 检查键是否存在
    if "name" in student:
        print("包含name键")
    print()


# ==================== 5. 函数定义 ====================

def function_demo():
    """
    函数定义演示
    """
    print("=" * 50)
    print("5. 函数定义")
    print("=" * 50)
    
    # 基本函数 - Java: public int add(int a, int b)
    def add(a, b):
        return a + b
    
    result = add(10, 20)
    print(f"10 + 20 = {result}")
    
    # 默认参数
    def greet(name, greeting="你好"):
        return f"{greeting}, {name}!"
    
    print(greet("小明"))
    print(greet("小明", "早上好"))
    
    # 可变参数 - Java: public void print(String... args)
    def sum_all(*numbers):
        return sum(numbers)
    
    print(f"求和: {sum_all(1, 2, 3, 4, 5)}")
    
    # 关键字参数
    def create_person(**kwargs):
        return kwargs
    
    person = create_person(name="王五", age=30, city="北京")
    print(f"创建人物: {person}")
    print()


# ==================== 6. 类和对象 ====================

class WebPage:
    """
    网页类演示（类比Java的类定义）
    
    Java对比:
    public class WebPage {
        private String url;
        private String content;
        
        public WebPage(String url) {
            this.url = url;
        }
    }
    """
    
    # 类变量（类似Java的static变量）
    total_pages = 0
    
    def __init__(self, url, title=""):
        """
        构造函数（类似Java的构造器）
        __init__ 相当于 Java的构造方法
        """
        self.url = url  # 实例变量（类似Java的this.url）
        self.title = title
        self.content = ""
        WebPage.total_pages += 1
    
    def fetch(self):
        """
        实例方法（类似Java的public方法）
        """
        self.content = f"从 {self.url} 获取的内容"
        return self.content
    
    def __str__(self):
        """
        toString方法（类似Java的toString()）
        """
        return f"WebPage(url={self.url}, title={self.title})"
    
    @classmethod
    def get_total_pages(cls):
        """
        类方法（类似Java的static方法）
        """
        return cls.total_pages


def class_demo():
    """
    类和对象使用演示
    """
    print("=" * 50)
    print("6. 类和对象")
    print("=" * 50)
    
    # 创建对象 - Java: WebPage page = new WebPage("...");
    page1 = WebPage("https://www.example.com", "示例网站")
    page2 = WebPage("https://www.python.org", "Python官网")
    
    print(page1)
    print(page1.fetch())
    print(f"总页面数: {WebPage.get_total_pages()}")
    print()


# ==================== 7. 异常处理 ====================

def exception_handling():
    """
    异常处理（类比Java的try-catch）
    """
    print("=" * 50)
    print("7. 异常处理")
    print("=" * 50)
    
    # Python: try-except-finally
    # Java: try-catch-finally
    try:
        result = 10 / 0
    except ZeroDivisionError as e:  # Java: catch (ArithmeticException e)
        print(f"捕获异常: {e}")
    except Exception as e:  # Java: catch (Exception e)
        print(f"其他异常: {e}")
    finally:  # Java: finally
        print("finally块执行")
    
    # 多个异常
    try:
        data = {"name": "test"}
        value = data["age"]
    except (KeyError, ValueError) as e:
        print(f"捕获多个异常: {e}")
    
    print()


# ==================== 8. 文件操作 ====================

def file_operations():
    """
    文件操作演示
    """
    print("=" * 50)
    print("8. 文件操作")
    print("=" * 50)
    
    # 写文件
    # Python的with语句会自动关闭文件（类似Java的try-with-resources）
    with open("test.txt", "w", encoding="utf-8") as f:
        f.write("Python爬虫学习\n")
        f.write("第一行内容\n")
        f.write("第二行内容\n")
    print("文件写入成功")
    
    # 读文件
    with open("test.txt", "r", encoding="utf-8") as f:
        content = f.read()
        print(f"文件内容:\n{content}")
    
    # 按行读取
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        print(f"共{len(lines)}行")
    
    print()


# ==================== 9. Lambda表达式 ====================

def lambda_demo():
    """
    Lambda表达式（类比Java 8的Lambda）
    """
    print("=" * 50)
    print("9. Lambda表达式")
    print("=" * 50)
    
    # Python: lambda x: x * 2
    # Java: (x) -> x * 2
    double = lambda x: x * 2
    print(f"Lambda: {double(5)}")
    
    # 在列表操作中使用
    numbers = [1, 2, 3, 4, 5]
    
    # map - Java: stream().map()
    doubled = list(map(lambda x: x * 2, numbers))
    print(f"Map结果: {doubled}")
    
    # filter - Java: stream().filter()
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"Filter结果: {evens}")
    
    # sorted - Java: stream().sorted()
    words = ["banana", "apple", "cherry"]
    sorted_words = sorted(words, key=lambda x: len(x))
    print(f"排序结果: {sorted_words}")
    
    print()


# ==================== 主函数 ====================

def main():
    """
    主函数 - 运行所有示例
    """
    print("\n" + "=" * 50)
    print("Python基础速成 - 针对Java开发者")
    print("=" * 50 + "\n")
    
    data_types_demo()
    string_operations()
    list_operations()
    dict_operations()
    function_demo()
    class_demo()
    exception_handling()
    file_operations()
    lambda_demo()
    
    print("=" * 50)
    print("✅ Python基础学习完成！")
    print("💡 建议：多动手练习，对比Java的写法")
    print("⏭️  下一步：学习 02_http_requests.py")
    print("=" * 50)


if __name__ == "__main__":
    # Python的main入口
    # Java对比: public static void main(String[] args)
    main()

