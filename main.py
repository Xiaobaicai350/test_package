import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo 管理器")
        self.root.geometry("600x500")
        
        # 数据文件路径
        self.data_file = "todos.json"
        
        # 初始化数据
        self.todos = self.load_todos()
        
        # 创建界面
        self.create_widgets()
        
        # 刷新显示
        self.refresh_todo_list()
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 输入区域
        input_frame = ttk.LabelFrame(main_frame, text="添加新任务", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 任务输入
        ttk.Label(input_frame, text="任务:").grid(row=0, column=0, sticky=tk.W)
        self.task_entry = ttk.Entry(input_frame, width=40)
        self.task_entry.grid(row=0, column=1, padx=(5, 0), sticky=(tk.W, tk.E))
        
        # 分类选择
        ttk.Label(input_frame, text="分类:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.category_var = tk.StringVar(value="个人")
        category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, 
                                     values=["工作", "个人", "学习", "生活"])
        category_combo.grid(row=1, column=1, padx=(5, 0), sticky=(tk.W, tk.E), pady=(5, 0))
        
        # 添加按钮
        add_btn = ttk.Button(input_frame, text="添加任务", command=self.add_todo)
        add_btn.grid(row=2, column=1, sticky=tk.E, pady=(10, 0))
        
        # 配置列权重
        input_frame.columnconfigure(1, weight=1)
        
        # 过滤区域
        filter_frame = ttk.LabelFrame(main_frame, text="筛选", padding="10")
        filter_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(filter_frame, text="按分类筛选:").grid(row=0, column=0, sticky=tk.W)
        self.filter_var = tk.StringVar(value="全部")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                   values=["全部", "工作", "个人", "学习", "生活"])
        filter_combo.grid(row=0, column=1, padx=(5, 0))
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_todo_list())
        
        # 显示状态筛选
        ttk.Label(filter_frame, text="状态:").grid(row=0, column=2, padx=(20, 0), sticky=tk.W)
        self.status_var = tk.StringVar(value="全部")
        status_combo = ttk.Combobox(filter_frame, textvariable=self.status_var,
                                   values=["全部", "未完成", "已完成"])
        status_combo.grid(row=0, column=3, padx=(5, 0))
        status_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_todo_list())
        
        # 任务列表区域
        list_frame = ttk.LabelFrame(main_frame, text="任务列表", padding="10")
        list_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 创建Treeview (添加隐藏的ID列)
        columns = ('id', '任务', '分类', '状态', '创建时间')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # 定义列
        self.tree.heading('id', text='ID')
        self.tree.heading('任务', text='任务')
        self.tree.heading('分类', text='分类')
        self.tree.heading('状态', text='状态')
        self.tree.heading('创建时间', text='创建时间')
        
        # 设置列宽 (隐藏ID列)
        self.tree.column('id', width=0, stretch=False)
        self.tree.column('任务', width=250)
        self.tree.column('分类', width=80)
        self.tree.column('状态', width=80)
        self.tree.column('创建时间', width=150)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 配置权重
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 操作按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Button(btn_frame, text="标记完成", command=self.mark_complete).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="标记未完成", command=self.mark_incomplete).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="删除任务", command=self.delete_todo).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="清空已完成", command=self.clear_completed).pack(side=tk.RIGHT)
        
        # 配置主窗口权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 绑定回车键
        self.task_entry.bind('<Return>', lambda e: self.add_todo())
    
    def load_todos(self):
        """从JSON文件加载todos"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_todos(self):
        """保存todos到JSON文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def add_todo(self):
        """添加新任务"""
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showwarning("警告", "请输入任务内容")
            return
        
        todo = {
            'id': len(self.todos) + 1,
            'task': task,
            'category': self.category_var.get(),
            'completed': False,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.todos.append(todo)
        self.save_todos()
        self.task_entry.delete(0, tk.END)
        self.refresh_todo_list()
        messagebox.showinfo("成功", "任务添加成功")
    
    def refresh_todo_list(self):
        """刷新任务列表显示"""
        # 清空现有项目
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 获取筛选条件
        filter_category = self.filter_var.get()
        filter_status = self.status_var.get()
        
        # 过滤并显示todos
        for todo in self.todos:
            # 分类筛选
            if filter_category != "全部" and todo['category'] != filter_category:
                continue
            
            # 状态筛选
            if filter_status == "已完成" and not todo['completed']:
                continue
            elif filter_status == "未完成" and todo['completed']:
                continue
            
            status = "✓ 已完成" if todo['completed'] else "○ 未完成"
            
            item_id = self.tree.insert('', tk.END, values=(
                todo['id'],  # ID列 (隐藏)
                todo['task'],
                todo['category'],
                status,
                todo['created_at']
            ))
    
    def get_selected_todo_id(self):
        """获取选中的todo ID"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择一个任务")
            return None
        
        item = selection[0]
        values = self.tree.item(item, 'values')
        return int(values[0])  # ID在第一列
    
    def mark_complete(self):
        """标记任务为完成"""
        todo_id = self.get_selected_todo_id()
        if todo_id is None:
            return
        
        for todo in self.todos:
            if todo['id'] == todo_id:
                todo['completed'] = True
                break
        
        self.save_todos()
        self.refresh_todo_list()
    
    def mark_incomplete(self):
        """标记任务为未完成"""
        todo_id = self.get_selected_todo_id()
        if todo_id is None:
            return
        
        for todo in self.todos:
            if todo['id'] == todo_id:
                todo['completed'] = False
                break
        
        self.save_todos()
        self.refresh_todo_list()
    
    def delete_todo(self):
        """删除任务"""
        todo_id = self.get_selected_todo_id()
        if todo_id is None:
            return
        
        if messagebox.askyesno("确认", "确定要删除这个任务吗？"):
            self.todos = [todo for todo in self.todos if todo['id'] != todo_id]
            self.save_todos()
            self.refresh_todo_list()
    
    def clear_completed(self):
        """清空已完成的任务"""
        completed_count = sum(1 for todo in self.todos if todo['completed'])
        
        if completed_count == 0:
            messagebox.showinfo("提示", "没有已完成的任务")
            return
        
        if messagebox.askyesno("确认", f"确定要删除 {completed_count} 个已完成的任务吗？"):
            self.todos = [todo for todo in self.todos if not todo['completed']]
            self.save_todos()
            self.refresh_todo_list()


def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
