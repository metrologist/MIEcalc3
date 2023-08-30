"""
load_utility.py creates/manages load profiles so that they can be added to a MIEcalc3 project workbook.
1/ Process half-hour data in the the form of kWh and kvarh into %current, phase angle, kWh form.
2/ Generate load profiles with nominally uniform or normal kWh distribution across a range of current and phase angle
combinations.

It will likely be made available under the Help menu as 'Load utility'.
"""
import csv
import openpyxl  # for xlsx and xlsxm
from statistics import NormalDist
from random import random, uniform
from math import sqrt, atan, pi

class Load_Utility(object):
    def __init__(self, source, output):
        """

        :param source: dictionary of input file_name (file, sheet), or generator parameters
        :param output: name of output csv file
        """
        self.output = output
        if source['type']=='normal':
            self.centre_angle = source['centre_angle']
            self.centre_current = source['centre_current']
        elif source['type']=='uniform':
            self.angle_range = source['angle_range']
            self.current_range = source['current_range']
        elif source['type']=='kwkvar_file':
            self.kwkvar_file = source['file_name']
        else:
            print('Load_Utility dictionary problem', source, output)

    def uniform(self):
        n = 4000  # the number of points to be calculated
        data = []
        for i in range(n):
            row = []
            current = uniform(self.current_range[0], self.current_range[1])
            if current > 120:  # limit to 120 % maximum
                current = 120
            angle = uniform(self.angle_range[0], self.angle_range[1])
            if abs(angle) == 90:  # avoid infinite tan
                angle = 89.9
            row.append(current)
            row.append(angle)
            row.append(1)  # energy
            data.append(row)
        self.store_file(data)

    def normal(self):
        n = 10  # the number of points to be calculated
        data = []
        for i in range(n):
            row = []
            current = NormalDist(mu=self.centre_current[0], sigma=self.centre_current[1]).inv_cdf(random())
            if current > 120:
                current = 120
            if current < 0:
                current = 0
            angle = NormalDist(mu=self.centre_angle[0], sigma=self.centre_angle[1]).inv_cdf(random())
            if abs(angle) == 90:  # avoid infinite tan
                angle = 89.9
            row.append(current)
            row.append(angle)
            row.append(1)  # energy
            data.append(row)
        self.store_file(data)

    def kwkvar(self, current, voltage, phases):
        """
        Only functions for a single quadrant, deducing phase angle from the ratio of var to W.
        :return:
        """
        ib = current  # 100 % current value
        v = voltage # voltage
        ph = phases # number of phases
        wb = openpyxl.load_workbook(self.kwkvar_file[0], data_only=True)
        sheetxnames = wb.sheetnames
        if self.kwkvar_file[1] in sheetxnames:
            sh = wb[self.kwkvar_file[1]]
            file_list = []
            for row in sh.values:
                temp_file_list = []
                temp_file_list.append(row[0])
                temp_file_list.append(row[1])
                temp_file_list.append(row[2])
                file_list.append(temp_file_list)
            data = []
            for i in range(1, len(file_list)):  # assume first line is header
                row = []
                wh = file_list[i][1]  # second column has energy
                varh = file_list[i][2]  # third column has reactive 'energy'
                va = sqrt(wh ** 2 + varh ** 2)
                current = va / ph / v * 2 /ib *100
                row.append(current)
                if wh == 0:
                    if varh == 0:
                        angle = 0
                    else:
                        angle = 90
                else:
                    angle = atan(varh / wh) * 180 / pi
                row.append(angle)
                row.append(wh)
                data.append(row)
            self.store_file(data)
        else:
            print('worksheet not found')

    def store_file(self, data_list):
        with open(self.output, 'w', newline='') as f:
            c = csv.writer(f)
            for x in data_list:
                c.writerow(x)


if __name__ == "__main__":
    definition1 = {'type': 'normal', 'centre_angle': (30, 5), 'centre_current': (20, 10) }
    definition2 = {'type': 'uniform', 'angle_range': (0, 30), 'current_range': (1, 20) }
    definition3 = {'type': 'kwkvar_file', 'file_name': ('217001251.ls1.xlsx', 'Cat3 800-5 CTs') }

    myload1 = Load_Utility(definition1, 'load_test1.csv')
    myload1.normal()
    myload2 = Load_Utility(definition2, 'load_test2.csv')
    myload2.uniform()
    myload3 = Load_Utility(definition3, 'load_test3.csv')
    myload3.kwkvar(5, 230, 3)
