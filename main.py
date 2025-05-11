import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QRadioButton, QHBoxLayout, QCheckBox
from datetime import datetime


# 定义生成大乐透号码的函数
def generate_lottery_numbers(favorite_front_numbers=None, favorite_back_numbers=None):
    """
    随机生成一组大乐透号码。
    前区号码范围为 1-35，后区号码范围为 1-12。
    返回值:
        tuple: 包含两个列表 (前区号码, 后区号码)
    """
    if favorite_front_numbers is None:
        favorite_front_numbers = []
    if favorite_back_numbers is None:
        favorite_back_numbers = []

    front_numbers = sorted(random.sample(range(1, 36), 5 - len(favorite_front_numbers)))
    back_numbers = sorted(random.sample(range(1, 13), 2 - len(favorite_back_numbers)))
    return sorted(favorite_front_numbers + front_numbers), sorted(favorite_back_numbers + back_numbers)


# 定义生成双色球号码的函数
def generate_double_color_ball_numbers(favorite_red_numbers=None, favorite_blue_number=None):
    """
    随机生成一组双色球号码。
    红球范围为 1-33，蓝球范围为 1-16。
    返回值:
        tuple: 包含两个列表 (红球号码, 蓝球号码)
    """
    if favorite_red_numbers is None:
        favorite_red_numbers = []
    if favorite_blue_number is None:
        favorite_blue_number = []

    red_numbers = sorted(random.sample(range(1, 34), 6 - len(favorite_red_numbers)))
    blue_number = random.randint(1, 16) if not favorite_blue_number else favorite_blue_number[0]
    return sorted(favorite_red_numbers + red_numbers), blue_number


# 记录生成的号码到 history.log 文件
def log_to_file(numbers):
    with open("history.log", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} - {numbers}\n")


# 创建主窗口
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("彩票号码生成器")
        self.setGeometry(100, 100, 800, 600)

        # 创建控件
        label = QLabel("请选择彩票类型并输入生成的组数：")
        self.radio_dale_tou = QRadioButton("大乐透")
        self.radio_double_color = QRadioButton("双色球")
        self.radio_dale_tou.setChecked(True)  # 默认选择大乐透

        # 添加提示文字和输入框
        count_label = QLabel("请输入生成组数：")
        self.entry_count = QLineEdit()
        self.entry_count.setFixedWidth(100)  # 设置输入框宽度为100像素

        button = QPushButton("生成号码")
        self.result_text = QTextEdit()

        # 前区号码选择
        self.favorite_front_checkboxes = []
        self.front_checkbox_layout = QVBoxLayout()

        # 后区号码选择
        self.favorite_back_checkboxes = []
        self.back_checkbox_layout = QVBoxLayout()

        # 绑定按钮点击事件
        button.clicked.connect(self.generate_and_display)

        # 动态生成复选框
        self.update_favorite_numbers_ui()

        # 布局管理
        layout = QVBoxLayout()

        # 添加单选按钮布局
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_dale_tou)
        radio_layout.addWidget(self.radio_double_color)

        # 添加生成组数的布局
        count_layout = QHBoxLayout()
        count_layout.addWidget(count_label)
        count_layout.addWidget(self.entry_count)
        count_layout.addStretch()  # 添加弹性空间，使控件靠左对齐

        layout.addWidget(label)
        layout.addLayout(radio_layout)
        layout.addLayout(count_layout)
        layout.addWidget(QLabel("选择喜欢的前区号码（多选）："))
        layout.addLayout(self.front_checkbox_layout)
        layout.addWidget(QLabel("选择喜欢的后区号码（多选）："))
        layout.addLayout(self.back_checkbox_layout)
        layout.addWidget(button)
        layout.addWidget(self.result_text)
        self.setLayout(layout)

        # 监听单选按钮切换事件
        self.radio_dale_tou.toggled.connect(self.update_favorite_numbers_ui)
        self.radio_double_color.toggled.connect(self.update_favorite_numbers_ui)

    def update_favorite_numbers_ui(self):
        """根据彩票类型更新前区和后区号码的范围"""
        lottery_type = self.get_selected_lottery_type()

        # 清空现有的复选框
        for checkbox in self.favorite_front_checkboxes:
            checkbox.deleteLater()
        for checkbox in self.favorite_back_checkboxes:
            checkbox.deleteLater()
        self.favorite_front_checkboxes.clear()
        self.favorite_back_checkboxes.clear()

        # 更新前区号码范围
        if lottery_type == "大乐透":
            front_range = range(1, 36)  # 大乐透前区号码范围
            back_range = range(1, 13)  # 大乐透后区号码范围
        elif lottery_type == "双色球":
            front_range = range(1, 34)  # 双色球前区号码范围
            back_range = range(1, 17)  # 双色球后区号码范围

        # 添加前区号码复选框
        self._add_checkboxes(front_range, self.front_checkbox_layout, self.favorite_front_checkboxes)

        # 添加后区号码复选框
        self._add_checkboxes(back_range, self.back_checkbox_layout, self.favorite_back_checkboxes)

    def _add_checkboxes(self, number_range, layout, checkbox_list):
        """通用方法：动态生成复选框并添加到指定布局"""
        row_layout = QHBoxLayout()  # 每行的布局
        for i, num in enumerate(number_range):
            checkbox = QCheckBox(str(num))
            checkbox_list.append(checkbox)
            row_layout.addWidget(checkbox)

            # 每5个复选框换一行
            if (i + 1) % 5 == 0 or i == len(number_range) - 1:
                layout.addLayout(row_layout)
                row_layout = QHBoxLayout()  # 新建一行

    def get_selected_lottery_type(self):
        """获取用户选择的彩票类型"""
        if self.radio_dale_tou.isChecked():
            return "大乐透"
        elif self.radio_double_color.isChecked():
            return "双色球"

    def generate_and_display(self):
        try:
            count = int(self.entry_count.text())
            if count <= 0:
                raise ValueError("组数必须是正整数！")
        except ValueError:
            self.result_text.setText("输入错误：请输入一个有效的正整数作为组数！")
            return

        lottery_type = self.get_selected_lottery_type()  # 获取用户选择的彩票类型

        # 获取用户选择的喜欢号码
        favorite_front_numbers = [int(cb.text()) for cb in self.favorite_front_checkboxes if cb.isChecked()]
        favorite_back_numbers = [int(cb.text()) for cb in self.favorite_back_checkboxes if cb.isChecked()]

        results = []
        for _ in range(count):
            if lottery_type == "大乐透":
                numbers = generate_lottery_numbers(favorite_front_numbers, favorite_back_numbers)
            elif lottery_type == "双色球":
                numbers = generate_double_color_ball_numbers(favorite_front_numbers, favorite_back_numbers)
            results.append(numbers)
            log_to_file(numbers)  # 记录到日志文件

        output = f"\n生成的{lottery_type}号码如下：\n"
        for i, numbers in enumerate(results, start=1):
            if lottery_type == "大乐透":
                output += f"第{i}组 - 前区号码: {numbers[0]}, 后区号码: {numbers[1]}\n"
            elif lottery_type == "双色球":
                output += f"第{i}组 - 红球号码: {numbers[0]}, 蓝球号码: {numbers[1]}\n"
        output += f"\n已生成 {count} 组号码，并记录到 history.log 文件中！"
        self.result_text.setText(output)


# 主程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())