#根据之前计算准确率的函数在各个缩放系数下分别得到的结果进行可视化演示
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 添加这条可以让图形显示中文

x_axis_data = [0.7, 0.75, 0.8, 0.85, 0.90,0.95,1]
y_axis_data = [0.03, 0.46, 0.58, 0.72, 0.88,0.98,1]

# plot中参数的含义分别是横轴值，纵轴值，线的形状，颜色，透明度,线的宽度和标签
plt.plot(x_axis_data, y_axis_data, 'ro-', color='#4169E1', alpha=0.8, linewidth=1)

# 显示标签，如果不加这句，即使在plot中加了label='一些数字'的参数，最终还是不会显示标签
plt.legend(loc="upper left")
plt.xlabel('缩放系数')
plt.ylabel('检测准确率')

plt.show()
# plt.savefig('demo.jpg')  # 保存该图片
