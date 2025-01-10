import matplotlib.pyplot as plt


global start
global end
# 1. 从文件中读取数据
def read_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read().strip()
    return [int(bit) for bit in data]

# 2. 提取波动周边信号
def extract_wave(data):
    
    data = process(data)
    # 初始化变量
    first_wave_index = None
    last_wave_index = None
    prev_bit = data[0]
    # 遍历数据，记录第一个和最后一个波动点
    for time, bit in enumerate(data[first_wave_index:]):
        if bit != prev_bit:  # 检测到变化点
            if first_wave_index is None:  # 先判断波动开始是否存在，不存在就赋值
                first_wave_index = time
                last_wave_index = time
    
            if time - last_wave_index < 20000:
                last_wave_index = time
                prev_bit = bit

    # 确保第一个和最后一个波动点有效
    if first_wave_index is None or last_wave_index is None:
        return [], []  # 如果没有波动，返回空列表

    # 计算记录范围
    print(first_wave_index)
    print(last_wave_index)
    start_index = max(0, first_wave_index - 20)
    end_index = min(len(data), last_wave_index + 21)

    # 提取范围内的信号和时间点
    # time_points = list(range(start_index, end_index))
    
    
    time_points = list(range(1, end_index - start_index + 1))
    global start
    global end
    start = start_index
    end = end_index
    signal_levels = data[start_index:end_index]

    return time_points, signal_levels
    
    

def process(data):  #预处理掉杂波
    first_wave_index = None
    index = 0
    next_wave_index = None
    prev_bit = data[0]
    for time, bit in enumerate(data):
        if bit != prev_bit:  # 检测到变化点
            if first_wave_index is None:  # 先判断波动开始是否存在，不存在就赋值
                first_wave_index = time
                index = 1
            elif index == 1:
                index = index + 1
            elif index == 2:
                next_wave_index = time
                index = 0
            
            last_wave_index = time
            prev_bit = bit
    print("first_wave_index:",first_wave_index)
    print("data[first_wave_index]:",data[first_wave_index])
    print("data[first_wave_index - 1]:",data[first_wave_index - 1])
    print("next_wave_index:",next_wave_index)
    if next_wave_index - first_wave_index > 20000:
        data[first_wave_index] = data[first_wave_index - 1]
        return process(data)
    
    return data
    
# 3. 绘制波形图并保存为图片
def save_wave_image(time_points, signal1, signal2, output_path):
    """
    Plots two signals on the same figure and saves the image.

    Args:
        time_points (list): The x-axis values.
        signal1 (list): The y-axis values for the first signal.
        signal2 (list): The y-axis values for the second signal.
        output_path (str): The file path where the image will be saved.

    Returns:
        None
    """
    width = max(12, len(time_points) / 50)  # 根据数据长度动态调整宽度
    plt.figure(figsize=(width, 4), constrained_layout=True)  # 自动调整布局

    # 绘制第一个图形
    # plt.plot(time_points, signal1, 'b-', label="Signal 1")  # 蓝色实线
    plt.step(time_points, signal1, where='mid', label="Signal 1", color='b')
    # 绘制第二个图形
    # plt.plot(time_points, signal2, 'r-', label="Signal 2")  # 红色实线
    plt.step(time_points, signal2, where='mid', label="Signal 2", color='r')
    # 设置坐标范围
    plt.xlim(min(time_points), max(time_points))
    plt.ylim(-0.1, 1.1)

    # 设置刻度优化
    plt.yticks([0, 4])
    plt.xticks(rotation=45)  # 横轴刻度旋转，避免重叠

    # 添加图例和网格
    plt.legend(loc="upper right")  # 图例在右上角
    plt.grid(True)

    # 保存图片，确保内容完整
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Waveform image saved to {output_path}")

# 主程序
file_path = "output_SDA.txt"  # 替换为你的文件路径
file_path1 = "output_SCL.txt" 
output_image_path = "gpio_waveform.png"  # 图片保存路径
data = read_data(file_path)
data1 = read_data(file_path1)
time_points, signal_levels = extract_wave(data)

# 把data1的对应部分取出来就行
signal_levels1 = data1[start:end]
signal_levels1 = [x + 2 for x in signal_levels1]
save_wave_image(time_points, signal_levels, signal_levels1 , output_image_path)
