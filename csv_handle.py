# -*- coding: gb2312 -*-
__author__ = 'WangYi'
__version__ = 0.1

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog  # qfiledialog用于弹出打开文件的窗口
from gui import Ui_Form

import matplotlib.pyplot as plt
import pandas as pd
import time
from datetime import datetime

from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


class Test(QWidget, Ui_Form):
    def __init__(self):
        super(Test, self).__init__()
        self.setupUi(self)

    # 类的变量
    tmdata = pd.DataFrame()
    plot_cfg = pd.DataFrame()
    fig_width = 640
    fig_hight = 480


    # 打开数据文件  注意:getOpenFileName返回值为元组 第一个参数为文件名
    def on_btn_openfile_click(self):
        filename = QFileDialog.getOpenFileName(caption='打开数据文件')

        skips = range(1, self.spinBox_del_rows.value())

        if self.radioButton_opendat.isChecked():  # 打开DAT文件
            seps = '\t'
        else:
            seps = ','

        # 获取当前时间
        now = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))

        if filename[0]:
            self.tmdata = pd.read_csv(filename[0], header=0, sep=seps, skiprows=skips, encoding='GB2312')
            # self.tmdata = pd.read_csv(filename[0], header=0, sep=seps, encoding='GB2312')  # 去除skiprows
            self.tmdata.replace(to_replace='--', value=0, inplace=True)  # 去除文件中-- 修改为0


            # 取出并显示第一行
            self.textEdit_log.append(now + '打开文件 ' + filename[0])
            self.textEdit_log.append('该文件第一行内容如下：')
            self.textEdit_log.append('列号---内容')
            j = 0
            for i in self.tmdata.columns:
                self.textEdit_log.append(str(j)+'---'+i)
                j += 1
        else:
            self.textEdit_log.append(now + '文件未打开')


    # 打开配置文件
    def on_btn_cfg_click(self):
        # 获取当前时间
        now = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))

        filename = self.lineEdit_cfg_path.text()
        if filename:
            self.plot_cfg = pd.read_csv(filename, header=0, sep=',', encoding='GB2312')
            self.textEdit_log.append(now + '成功打开配置文件 ' + filename)
        else:
            filename2 = QFileDialog.getOpenFileName(caption='打开配置文件')
            if filename2[0]:
                self.plot_cfg = pd.read_csv(filename2[0], header=0, sep=',', encoding='GB2312')
                self.textEdit_log.append(now + '打开配置文件 ' + filename2[0])
                self.lineEdit_cfg_path.setText(filename2[0])
            else:
                self.textEdit_log.append(now + '配置文件未打开')

        # filename = QFileDialog.getOpenFileName(caption='打开配置文件')
        # if filename[0]:
        #     self.plot_cfg = pd.read_csv(filename[0], header=0, sep=',', encoding='GB2312')
        #     self.textEdit_log.append(now + '打开配置文件 ' + filename[0])
        #
        # else:
        #     self.textEdit_log.append(now + '文件未打开')


    # 画图函数
    def on_btn_plot_click(self):
        # 获取横坐标
        xdat = list()
        for ii in self.tmdata.iloc[:, 0]:
            xdat.append(datetime.strptime(ii, '%Y年%m月%d日%H时%M分%S秒'))


        # 获取纵坐标
        startnum = self.spinBox_plot_start.value()
        endnum = self.spinBox_plot_end.value()
        if startnum < endnum:  # 绘制多曲线
            ydat = self.tmdata.iloc[:, startnum:endnum+1]
            ylegend = self.tmdata.columns[startnum:endnum+1]
        else:  # 绘制单曲线
            ydat = self.tmdata.iloc[:, startnum]
            ylegend = [self.tmdata.columns[startnum]]  # legend对于str型 需要用[] 否则只显示第一个元素

        # 画图
        fig_width = self.doubleSpinBox_width.value()/100
        fig_hight = self.doubleSpinBox_hight.value()/100
        fig = plt.figure(figsize=(fig_width, fig_hight))  #  figsize=(12.80, 9.6) 可以设置画布大小 1280*960
        ax = fig.add_subplot(111)
        ax.plot(xdat, ydat, linewidth=2)

        # 设置Y轴范围
        if self.radioButton_ylim_set.isChecked():
            ax.set_ylim(bottom=self.doubleSpinBox_ylim_min.value(), top=self.doubleSpinBox_ylim_max.value())
        else:
            pass

        # 设置图题 图例和坐标轴旋转
        ax.set_title(self.lineEdit_plot_tilte_content.text(), fontsize=self.spinBox_plot_title_fontsize.value())
        ax.legend(ylegend, loc=0, fontsize=10)
        for lb in ax.xaxis.get_ticklabels():
            lb.set_rotation(45)
            lb.set_fontsize(8)

        figname = self.lineEdit_plot_tilte_content.text() + '.png'
        plt.savefig(figname)
        plt.show()
        plt.close()

        now = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
        self.textEdit_log.append(now + '生成图片文件: ' + figname)

    # 清除函数
    def on_btn_clear_click(self):
        self.textEdit_log.clear()

    # 拆分CSV文件
    def on_btn_splitfile_click(self):
        csvfilename = self.lineEdit_split_filename.text()

        startnum = self.spinBox_split_start.value()
        endnum = self.spinBox_split_end.value()
        tt = [0]
        if startnum < endnum:  # 输出两列及以上
            for i in range(startnum, endnum+1):
                tt.append(i)
        else:  # 仅输出一列
            tt.append(startnum)

        out = self.tmdata.iloc[:, tt]

        out.to_csv(csvfilename, index=False, encoding='GB2312')

        now = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
        self.textEdit_log.append(now + '生成csv文件: ' + csvfilename)


    # 画图函数 被DPC自动画图函数调用
    def dpc_plot(self, startnum, endnum, figtitle, figfname):
        # 获取横坐标
        xdat = list()
        for ii in self.tmdata.iloc[:, 0]:
            xdat.append(datetime.strptime(ii, '%Y年%m月%d日%H时%M分%S秒'))

        # 获取纵坐标
        if startnum < endnum:  # 绘制多曲线
            ydat = self.tmdata.iloc[:, startnum:endnum + 1]
            ylegend = self.tmdata.columns[startnum:endnum + 1]
        else:  # 绘制单曲线
            ydat = self.tmdata.iloc[:, startnum]
            ylegend = [self.tmdata.columns[startnum]]  # legend对于str型 需要用[] 否则只显示第一个元素

        # 画图
        fig_width = self.doubleSpinBox_width.value()/100
        fig_hight = self.doubleSpinBox_hight.value()/100
        fig = plt.figure(figsize=(fig_width, fig_hight))  #  figsize=(12.80, 9.6) 可以设置画布大小 1280*960
        ax = fig.add_subplot(111)
        ax.plot(xdat, ydat, linewidth=2)

        # 设置图题 图例和坐标轴旋转
        ax.set_title(figtitle, fontsize=16)
        ax.legend(ylegend, loc=0, fontsize=10)
        for lb in ax.xaxis.get_ticklabels():
            lb.set_rotation(45)
            lb.set_fontsize(8)

        figname = figfname + '.png'
        plt.savefig(figname)
        # plt.show()
        plt.close()

        now = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
        self.textEdit_log.append(now + '生成图片文件: ' + figname)


    # DPC自动画图函数
    def on_btn_dpc_click(self):
        self.dpc_plot(startnum=1, endnum=4, figtitle='光机头部电压遥测', figfname='光机头部电压遥测')
        self.dpc_plot(startnum=5, endnum=8, figtitle='信息处理箱电压遥测', figfname='信息处理箱电压遥测')
        self.dpc_plot(startnum=9, endnum=10, figtitle='温控单元电压遥测', figfname='温控单元电压遥测')
        self.dpc_plot(startnum=11, endnum=11, figtitle='电机电压遥测', figfname='电机电压遥测')
        self.dpc_plot(startnum=17, endnum=21, figtitle='光机头部温度遥测', figfname='光机头部温度遥测')
        self.dpc_plot(startnum=22, endnum=23, figtitle='电单机温度遥测', figfname='电单机温度遥测')

    # 根据csv配置文件画图函数
    def on_btn_plotall_click(self):
        row_len = len(self.plot_cfg.index)
        for i in range(row_len):
            self.dpc_plot(startnum=self.plot_cfg.iloc[i, 0],
                          endnum=self.plot_cfg.iloc[i, 1],
                          figtitle=self.plot_cfg.iloc[i, 2],
                          figfname=self.plot_cfg.iloc[i, 2])


    # 数据剔除和替换函数
    def on_btn_replace_click(self):
        tt = self.doubleSpinBox_tt.value()  # 替换之前的值
        rr = self.doubleSpinBox_rr.value()  # 替换后的值
        replace_columns = self.spinBox_replace_col.value()

        now = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))

        if self.radioButton_gt.isChecked():  # 大于替换 遥测数据大于某值时认为异常 进行替换
            for i, dat in enumerate(self.tmdata.iloc[:, replace_columns]):
                if dat > tt:  # 大于 替换
                    self.tmdata.iloc[i, replace_columns] = rr
                else:
                    pass
            self.textEdit_log.append(now + '大于替换完成')
        else:  # 小于替换 遥测数据小于某值时认为异常 进行替换
            for i, dat in enumerate(self.tmdata.iloc[:, replace_columns]):
                if dat < tt:  # 大于 替换
                    self.tmdata.iloc[i, replace_columns] = rr
                else:
                    pass
            self.textEdit_log.append(now + '小于替换完成')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = Test()
    mywidget.show()
    sys.exit(app.exec_())
