import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
from typing import List, Tuple


class UserPackSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("用户礼包发放工具")
        self.root.geometry("800x700")
        
        # 接口配置
        self.api1_url = "http://10.102.32.14/pack/sendSingle"
        self.api2_url = "http://10.102.40.32/service/content/ledu/right/giveByKefu"
        
        # 接口1固定参数
        self.pack_id = 4006
        self.pack_name = "乐读补偿礼包_不包含乐读_魂守"
        self.desc = "客服已沟通补发"
        self.use_flag = 0
        
        # 统计信息
        self.success_count = 0
        self.error_count = 0
        
        # 创建界面
        self.create_widgets()
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 输入区域
        input_frame = ttk.LabelFrame(main_frame, text="输入用户ID（每行一个）", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 用户ID输入框
        self.user_id_text = scrolledtext.ScrolledText(input_frame, height=10, width=50)
        self.user_id_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置输入区域权重
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        # 按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.execute_btn = ttk.Button(btn_frame, text="开始执行", command=self.execute_sending)
        self.execute_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_btn = ttk.Button(btn_frame, text="清空结果", command=self.clear_results)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # 统计信息区域
        stats_frame = ttk.LabelFrame(main_frame, text="统计信息", padding="10")
        stats_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.stats_label = ttk.Label(stats_frame, text="成功: 0 | 错误: 0", font=("Arial", 12, "bold"))
        self.stats_label.grid(row=0, column=0, sticky=tk.W)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="处理结果", padding="10")
        result_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建Treeview显示结果
        columns = ('用户ID', '接口1', '接口2', '状态')
        self.result_tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=15)
        
        # 定义列
        self.result_tree.heading('用户ID', text='用户ID')
        self.result_tree.heading('接口1', text='接口1状态')
        self.result_tree.heading('接口2', text='接口2状态')
        self.result_tree.heading('状态', text='整体状态')
        
        # 设置列宽
        self.result_tree.column('用户ID', width=150)
        self.result_tree.column('接口1', width=150)
        self.result_tree.column('接口2', width=150)
        self.result_tree.column('状态', width=200)
        
        # 滚动条
        result_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=result_scrollbar.set)
        
        # 布局
        self.result_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        result_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 配置权重
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def parse_user_ids(self) -> List[str]:
        """解析用户ID列表"""
        text = self.user_id_text.get("1.0", tk.END).strip()
        if not text:
            return []
        
        # 按行分割，去除空行和空白字符
        user_ids = []
        for line in text.split('\n'):
            line = line.strip()
            if line:
                user_ids.append(line)
        
        return user_ids
    
    def is_already_received(self, message: str, data: str = "") -> bool:
        """判断是否为已领取状态（不算错误）"""
        if not message and not data:
            return False
        
        message_str = str(message).lower() if message else ""
        data_str = str(data).lower() if data else ""
        combined = message_str + " " + data_str
        
        # 检查是否包含已领取相关的关键词
        received_keywords = ["已领取", "已购买", "already received", "already purchased"]
        return any(keyword in combined for keyword in received_keywords)
    
    def call_api1(self, user_id: str) -> Tuple[bool, str]:
        """调用接口1：发送礼包"""
        try:
            payload = {
                "userIds": [int(user_id)],
                "packId": self.pack_id,
                "packName": self.pack_name,
                "desc": self.desc,
                "useFlag": self.use_flag
            }
            
            response = requests.post(
                self.api1_url,
                headers={'Content-Type': 'application/json'},
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result.get('message', '')
                data = result.get('data', '')
                
                # 检查是否成功
                if result.get('success') and result.get('code') == 0:
                    return True, "成功"
                # 检查是否为已领取状态（不算错误）
                elif self.is_already_received(message, data):
                    return True, "已领取"
                else:
                    return False, f"失败: {message or data or '未知错误'}"
            else:
                return False, f"HTTP错误: {response.status_code}"
        
        except requests.exceptions.RequestException as e:
            return False, f"请求异常: {str(e)}"
        except Exception as e:
            return False, f"异常: {str(e)}"
    
    def call_api2(self, user_id: str) -> Tuple[bool, str]:
        """调用接口2：发放权益"""
        try:
            data = {'userId': user_id}
            
            response = requests.post(
                self.api2_url,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result.get('message')
                data_str = result.get('data', '')
                
                # 检查是否成功
                if result.get('code') == 0:
                    # 检查data中是否包含已购买信息（接口2的data可能包含"已购买: X"）
                    if self.is_already_received(str(message) if message else "", data_str):
                        return True, "已领取"
                    return True, "成功"
                # 检查是否为已领取状态（不算错误）
                elif self.is_already_received(str(message) if message else "", data_str):
                    return True, "已领取"
                else:
                    return False, f"失败: {message or data_str or '未知错误'}"
            else:
                return False, f"HTTP错误: {response.status_code}"
        
        except requests.exceptions.RequestException as e:
            return False, f"请求异常: {str(e)}"
        except Exception as e:
            return False, f"异常: {str(e)}"
    
    def execute_sending(self):
        """执行发放流程"""
        # 解析用户ID
        user_ids = self.parse_user_ids()
        
        if not user_ids:
            messagebox.showwarning("警告", "请输入至少一个用户ID")
            return
        
        # 重置统计
        self.success_count = 0
        self.error_count = 0
        
        # 清空结果树
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        # 禁用执行按钮
        self.execute_btn.config(state='disabled')
        
        # 更新UI
        self.root.update()
        
        try:
            # 串行处理每个用户ID
            for idx, user_id in enumerate(user_ids):
                # 调用接口1
                api1_success, api1_msg = self.call_api1(user_id)
                
                # 如果接口1失败，立即终止
                if not api1_success:
                    self.error_count += 1
                    item = self.result_tree.insert('', tk.END, values=(
                        user_id,
                        f"✗ {api1_msg}",
                        "未执行",
                        "✗ 失败"
                    ), tags=('error',))
                    
                    # 更新统计
                    self.update_stats()
                    
                    # 显示错误信息并终止
                    error_msg = f"处理到用户ID {user_id} 时发生错误（第 {idx + 1} 个用户）\n\n"
                    error_msg += f"接口1失败: {api1_msg}\n"
                    error_msg += "已终止执行，未调用接口2"
                    messagebox.showerror("执行失败", error_msg)
                    break
                
                # 接口1成功，继续调用接口2
                api2_success, api2_msg = self.call_api2(user_id)
                
                # 判断整体状态
                if api2_success:
                    overall_status = "✓ 成功"
                    self.success_count += 1
                    tag = 'success'
                else:
                    overall_status = "✗ 失败"
                    self.error_count += 1
                    tag = 'error'
                    
                    # 接口2失败，立即终止
                    # 格式化接口1的显示消息
                    api1_display = f"✓ {api1_msg}" if api1_success else f"✗ {api1_msg}"
                    
                    item = self.result_tree.insert('', tk.END, values=(
                        user_id,
                        api1_display,
                        f"✗ {api2_msg}",
                        overall_status
                    ), tags=(tag,))
                    
                    # 更新统计
                    self.update_stats()
                    
                    # 显示错误信息并终止
                    error_msg = f"处理到用户ID {user_id} 时发生错误（第 {idx + 1} 个用户）\n\n"
                    error_msg += f"接口1: {api1_msg}\n"
                    error_msg += f"接口2失败: {api2_msg}"
                    messagebox.showerror("执行失败", error_msg)
                    break
                
                # 两个接口都成功，格式化显示消息
                api1_display = f"✓ {api1_msg}" if api1_success else f"✗ {api1_msg}"
                api2_display = f"✓ {api2_msg}" if api2_success else f"✗ {api2_msg}"
                
                item = self.result_tree.insert('', tk.END, values=(
                    user_id,
                    api1_display,
                    api2_display,
                    overall_status
                ), tags=(tag,))
                
                # 更新统计
                self.update_stats()
                
                # 滚动到最新结果
                self.result_tree.see(item)
                self.root.update()
            
            # 如果全部成功
            if self.error_count == 0:
                messagebox.showinfo("执行完成", f"所有用户处理完成！\n成功: {self.success_count} 个")
        
        except Exception as e:
            messagebox.showerror("异常", f"执行过程中发生异常: {str(e)}")
        
        finally:
            # 重新启用执行按钮
            self.execute_btn.config(state='normal')
            
            # 配置标签颜色
            self.result_tree.tag_configure('success', foreground='green')
            self.result_tree.tag_configure('error', foreground='red')
    
    def update_stats(self):
        """更新统计信息"""
        self.stats_label.config(text=f"成功: {self.success_count} | 错误: {self.error_count}")
    
    def clear_results(self):
        """清空结果"""
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        self.success_count = 0
        self.error_count = 0
        self.update_stats()


def main():
    root = tk.Tk()
    app = UserPackSenderApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()

