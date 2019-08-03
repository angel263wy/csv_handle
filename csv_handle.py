# -*- coding: gb2312 -*-
__author__ = 'WangYi'
__version__ = 0.1

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog  # qfiledialog���ڵ������ļ��Ĵ���
from gui import Ui_Form

import matplotlib.pyplot as plt
import pandas as pd
import time
from datetime import datetime

from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']  # ָ��Ĭ������
mpl.rcParams['axes.unicode_minus'] = False  # �������ͼ���Ǹ���'-'��ʾΪ���������


class Test(QWidget, Ui_Form):
    def __init__(self):
        super(Test, self).__init__()
        self.setupUi(self)

    # ��ı���
    tmdata = pd.DataFrame()
    plot_cfg = pd.DataFrame()
    fig_width = 640
    fig_hight = 480


    # �������ļ�  ע��:getOpenFileName����ֵΪԪ�� ��һ������Ϊ�ļ���
    def on_btn_openfile_click(self):
        filename = QFileDialog.getOpenFileName(caption='�������ļ�')

        skips = range(1, self.spinBox_del_rows.value())

        if self.radioButton_opendat.isChecked():  # ��DAT�ļ�
            seps = '\t'
        else:
            seps = ','

        # ��ȡ��ǰʱ��
        now = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))

        if filename[0]:
            self.tmdata = pd.read_csv(filename[0], header=0, sep=seps, skiprows=skips, encoding='GB2312')
            # self.tmdata = pd.read_csv(filename[0], header=0, sep=seps, encoding='GB2312')  # ȥ��skiprows
            self.tmdata.replace(to_replace='--', value=0, inplace=True)  # ȥ���ļ���-- �޸�Ϊ0


            # ȡ������ʾ��һ��
            self.textEdit_log.append(now + '���ļ� ' + filename[0])
            self.textEdit_log.append('���ļ���һ���������£�')
            self.textEdit_log.append('�к�---����')
            j = 0
            for i in self.tmdata.columns:
                self.textEdit_log.append(str(j)+'---'+i)
                j += 1
        else:
            self.textEdit_log.append(now + '�ļ�δ��')


    # �������ļ�
    def on_btn_cfg_click(self):
        # ��ȡ��ǰʱ��
        now = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))

        filename = self.lineEdit_cfg_path.text()
        if filename:
            self.plot_cfg = pd.read_csv(filename, header=0, sep=',', encoding='GB2312')
            self.textEdit_log.append(now + '�ɹ��������ļ� ' + filename)
        else:
            filename2 = QFileDialog.getOpenFileName(caption='�������ļ�')
            if filename2[0]:
                self.plot_cfg = pd.read_csv(filename2[0], header=0, sep=',', encoding='GB2312')
                self.textEdit_log.append(now + '�������ļ� ' + filename2[0])
                self.lineEdit_cfg_path.setText(filename2[0])
            else:
                self.textEdit_log.append(now + '�����ļ�δ��')

        # filename = QFileDialog.getOpenFileName(caption='�������ļ�')
        # if filename[0]:
        #     self.plot_cfg = pd.read_csv(filename[0], header=0, sep=',', encoding='GB2312')
        #     self.textEdit_log.append(now + '�������ļ� ' + filename[0])
        #
        # else:
        #     self.textEdit_log.append(now + '�ļ�δ��')


    # ��ͼ����
    def on_btn_plot_click(self):
        # ��ȡ������
        xdat = list()
        for ii in self.tmdata.iloc[:, 0]:
            xdat.append(datetime.strptime(ii, '%Y��%m��%d��%Hʱ%M��%S��'))


        # ��ȡ������
        startnum = self.spinBox_plot_start.value()
        endnum = self.spinBox_plot_end.value()
        if startnum < endnum:  # ���ƶ�����
            ydat = self.tmdata.iloc[:, startnum:endnum+1]
            ylegend = self.tmdata.columns[startnum:endnum+1]
        else:  # ���Ƶ�����
            ydat = self.tmdata.iloc[:, startnum]
            ylegend = [self.tmdata.columns[startnum]]  # legend����str�� ��Ҫ��[] ����ֻ��ʾ��һ��Ԫ��

        # ��ͼ
        fig_width = self.doubleSpinBox_width.value()/100
        fig_hight = self.doubleSpinBox_hight.value()/100
        fig = plt.figure(figsize=(fig_width, fig_hight))  #  figsize=(12.80, 9.6) �������û�����С 1280*960
        ax = fig.add_subplot(111)
        ax.plot(xdat, ydat, linewidth=2)

        # ����Y�᷶Χ
        if self.radioButton_ylim_set.isChecked():
            ax.set_ylim(bottom=self.doubleSpinBox_ylim_min.value(), top=self.doubleSpinBox_ylim_max.value())
        else:
            pass

        # ����ͼ�� ͼ������������ת
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
        self.textEdit_log.append(now + '����ͼƬ�ļ�: ' + figname)

    # �������
    def on_btn_clear_click(self):
        self.textEdit_log.clear()

    # ���CSV�ļ�
    def on_btn_splitfile_click(self):
        csvfilename = self.lineEdit_split_filename.text()

        startnum = self.spinBox_split_start.value()
        endnum = self.spinBox_split_end.value()
        tt = [0]
        if startnum < endnum:  # ������м�����
            for i in range(startnum, endnum+1):
                tt.append(i)
        else:  # �����һ��
            tt.append(startnum)

        out = self.tmdata.iloc[:, tt]

        out.to_csv(csvfilename, index=False, encoding='GB2312')

        now = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
        self.textEdit_log.append(now + '����csv�ļ�: ' + csvfilename)


    # ��ͼ���� ��DPC�Զ���ͼ��������
    def dpc_plot(self, startnum, endnum, figtitle, figfname):
        # ��ȡ������
        xdat = list()
        for ii in self.tmdata.iloc[:, 0]:
            xdat.append(datetime.strptime(ii, '%Y��%m��%d��%Hʱ%M��%S��'))

        # ��ȡ������
        if startnum < endnum:  # ���ƶ�����
            ydat = self.tmdata.iloc[:, startnum:endnum + 1]
            ylegend = self.tmdata.columns[startnum:endnum + 1]
        else:  # ���Ƶ�����
            ydat = self.tmdata.iloc[:, startnum]
            ylegend = [self.tmdata.columns[startnum]]  # legend����str�� ��Ҫ��[] ����ֻ��ʾ��һ��Ԫ��

        # ��ͼ
        fig_width = self.doubleSpinBox_width.value()/100
        fig_hight = self.doubleSpinBox_hight.value()/100
        fig = plt.figure(figsize=(fig_width, fig_hight))  #  figsize=(12.80, 9.6) �������û�����С 1280*960
        ax = fig.add_subplot(111)
        ax.plot(xdat, ydat, linewidth=2)

        # ����ͼ�� ͼ������������ת
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
        self.textEdit_log.append(now + '����ͼƬ�ļ�: ' + figname)


    # DPC�Զ���ͼ����
    def on_btn_dpc_click(self):
        self.dpc_plot(startnum=1, endnum=4, figtitle='���ͷ����ѹң��', figfname='���ͷ����ѹң��')
        self.dpc_plot(startnum=5, endnum=8, figtitle='��Ϣ�������ѹң��', figfname='��Ϣ�������ѹң��')
        self.dpc_plot(startnum=9, endnum=10, figtitle='�¿ص�Ԫ��ѹң��', figfname='�¿ص�Ԫ��ѹң��')
        self.dpc_plot(startnum=11, endnum=11, figtitle='�����ѹң��', figfname='�����ѹң��')
        self.dpc_plot(startnum=17, endnum=21, figtitle='���ͷ���¶�ң��', figfname='���ͷ���¶�ң��')
        self.dpc_plot(startnum=22, endnum=23, figtitle='�絥���¶�ң��', figfname='�絥���¶�ң��')

    # ����csv�����ļ���ͼ����
    def on_btn_plotall_click(self):
        row_len = len(self.plot_cfg.index)
        for i in range(row_len):
            self.dpc_plot(startnum=self.plot_cfg.iloc[i, 0],
                          endnum=self.plot_cfg.iloc[i, 1],
                          figtitle=self.plot_cfg.iloc[i, 2],
                          figfname=self.plot_cfg.iloc[i, 2])


    # �����޳����滻����
    def on_btn_replace_click(self):
        tt = self.doubleSpinBox_tt.value()  # �滻֮ǰ��ֵ
        rr = self.doubleSpinBox_rr.value()  # �滻���ֵ
        replace_columns = self.spinBox_replace_col.value()

        now = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))

        if self.radioButton_gt.isChecked():  # �����滻 ң�����ݴ���ĳֵʱ��Ϊ�쳣 �����滻
            for i, dat in enumerate(self.tmdata.iloc[:, replace_columns]):
                if dat > tt:  # ���� �滻
                    self.tmdata.iloc[i, replace_columns] = rr
                else:
                    pass
            self.textEdit_log.append(now + '�����滻���')
        else:  # С���滻 ң������С��ĳֵʱ��Ϊ�쳣 �����滻
            for i, dat in enumerate(self.tmdata.iloc[:, replace_columns]):
                if dat < tt:  # ���� �滻
                    self.tmdata.iloc[i, replace_columns] = rr
                else:
                    pass
            self.textEdit_log.append(now + 'С���滻���')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = Test()
    mywidget.show()
    sys.exit(app.exec_())
