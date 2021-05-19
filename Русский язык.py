import sys
import os
import shutil
import csv

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('designs/MainForm.ui', self)
        
        self.add_info_to_class_button.clicked.connect(self.add_info_to_class)
        self.create_class_button.clicked.connect(self.create_class)
        self.inf_button.clicked.connect(self.look_inf)
        
    def add_info_to_class(self):
        self.add_info_to_class_form = AddInfoToClassForm(self)
        self.add_info_to_class_form.show()
        
    def create_class(self):
        self.create_class_form = CreateClassForm(self)
        self.create_class_form.show()
        
    def look_inf(self):
        self.look_inf = LookMainInf(self)
        self.look_inf.show()
        

class AddInfoToClassForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('designs/AddInfoToClassForm.ui', self)
        
        self.add_inf_add_information_button.clicked.connect(
            self.add_inf_add_information_to_class)
        self.add_inf_inf_button.clicked.connect(self.look_add_inf_inf)
        
    def add_inf_add_information_to_class(self, *args):
        n_str_keys = 1
        n_str_keys_additional = 2
        
        max_score_for_tasks = [1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 
                               2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 
                               1, 6, 1, 1, 2, 2, 3, 3, 2, 2, 1, 1, 25]        

        protocol_name = self.add_inf_protocol_name_line_edit.text()
        name_class = ''.join(self.add_inf_class_name_line_edit.text().
                             lower().split())
        
        with open(protocol_name) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            data = list(reader)
        
        work_date = data[0][0][len(data[2][1]) - 10:]     
        
        the_directory = os.getcwd()
        class_main_directory = the_directory + '/' + name_class
        class_actual_directory = class_main_directory + '/' + \
            name_class + ' — актуальная версия'
        class_reserve_directory = class_main_directory + '/' + \
            name_class + ' — резервная версия'
        risk_group_directory = class_actual_directory + '/' + \
            name_class + ' — группа риска'
        
        works_directory = class_actual_directory + '/' + \
                    name_class + ' — работы'
        the_work_file = works_directory + '/' + work_date + '.csv'
                
        self.list_of_risk_student_file = risk_group_directory + '/' + \
            name_class + ' — группа риска.txt'        
        self.risk_student_file_csv = risk_group_directory + '/' + \
            name_class + ' — группа риска.csv'
        
        for j in range(len(data[n_str_keys])):
            if data[n_str_keys][j].lower() == 'класс':
                if data[n_str_keys + 3][j]:
                    n_key_class = j
            elif data[n_str_keys][j].lower() == 'фио учителя':
                if data[n_str_keys + 3][j]:
                    n_key_teacher_full_name = j
            elif data[n_str_keys][j].lower() == 'фио обучающегося':
                if data[n_str_keys + 2][j]:
                    n_key_student_full_name = j
            elif data[n_str_keys][j].lower() in ('задание 1', '1 задание'):
                task_1 = j
            elif data[n_str_keys][j].lower() in ('задание 27', '27 задание'):
                task_27 = j
                additional_criterion_1 = j
                additional_criterion_12 = j + 11
            elif '27' in data[n_str_keys][j].lower() \
                 and 'итого' in data[n_str_keys][j].lower():
                task_27_total = j
            elif 'первич' in data[n_str_keys][j].lower():
                score = j
            elif 'стобалл' in data[n_str_keys][j].lower():
                score_100 = j
            elif data[n_str_keys][j].lower() in ('оценка', 'отметка'):
                mark = j
        
        shutil.copytree(class_actual_directory, class_reserve_directory)
        
        the_work = []
        the_work.append(data[n_str_keys][n_key_student_full_name:])
        
        class_score = [0] * 39
        n_students = 0        
        
        f_class = False
        
        for row in data:
            if ''.join(row[n_key_class].split()).lower() == \
               ''.join(name_class.lower().split()):
                f_class = True
                row[n_key_student_full_name] = ' '.join(x.capitalize() for x in
                                        row[n_key_student_full_name].split())            
                if row[score_100]:
                    if int(row[score_100]) <= 39 and row[task_1].lower() not \
                            in ('н', 'отс', 'n'):
                        self.add_to_risk_group_list(
                            row[n_key_student_full_name]) 
                    
                    personal_data = [[work_date]]
                    for i in range(task_1, mark + 1):
                        personal_data[0].append(row[i])                  
                        
                    full_personal_filename_path = class_actual_directory + '/' \
                        + row[n_key_student_full_name] + '.csv'
                    with open(full_personal_filename_path) as csvfile:
                        reader = csv.reader(csvfile, delimiter=';')
                        pf_data = list(reader)
                    pf_data[-1] = personal_data[0]
                    count_works = len(pf_data) - 4                   
                    for i in range(4, len(pf_data)):
                        if pf_data[i][1].lower() in ('', 'отс'):
                            count_works -= 1
                    
                    persentage = ['Доля выполнения']
                    for i in range(1, 40):
                        task_i = 0                           
                        for ii in range(4, len(pf_data)):
                            if pf_data[ii][1].lower() not in ('', 'отс'):
                                task_i += int(pf_data[ii][i])                          
                        persent = task_i / (count_works * 
                                            max_score_for_tasks[i - 1])            
                        persentage.append('%.2f' % persent)
                    pf_data.append(persentage)
                                                           
                    with open(full_personal_filename_path, 
                              'w', newline='') as personal_file:
                        writer=csv.writer(personal_file, delimiter=';', 
                                          quotechar='"', 
                                          quoting=csv.QUOTE_MINIMAL)
                        for row_pd in pf_data:
                            writer.writerow(row_pd)
                else:
                    with open(full_personal_filename_path) as csvfile:
                        reader = csv.reader(csvfile, delimiter=';')
                        pf_data = list(reader) 
                    pf_data[0][2] = pf_data[0][2][:-1] \
                        + str(int(personal_data[0][2][-1]) + 1)
                    pf_data.insert(-1, [work_date, 'ОТС'])
                        
                        
                    with open(full_personal_filename_path, 
                              'w', newline='') as personal_file:
                        writer=csv.writer(personal_file, delimiter=';', 
                                          quotechar='"', 
                                          quoting=csv.QUOTE_MINIMAL)
                        for row_pd in pf_data:
                            writer.writerow(row_pd)
                if row[task_1].lower() not in ('н', 'отс', 'n'):
                    for i in range(task_1, score):
                        class_score[i - task_1] += int(row[i])
                    n_students += 1
                the_work.append(row[n_key_student_full_name:]) 
        
        if f_class:            
            persentage = ['Доля выполнения']
            for i in range(len(class_score)):
                persent = class_score[i] / (n_students * max_score_for_tasks[i])            
                persentage.append('%.2f' % persent)
            the_work.append(persentage)
            
            with open(the_work_file, 'w', newline='') as work_file:
                writer=csv.writer(work_file, delimiter=';', 
                                  quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row_tw in the_work:
                    writer.writerow(row_tw)
        else:
            pass  
        
        self.add_inf_add_information_button.setEnabled(False)
        
    def add_to_risk_group_list(self, student_name):
        file1 = open(self.list_of_risk_student_file, 'r', encoding='utf-8')
        rg_names = file1.read().split(', ')
        file1.close()
        if student_name not in rg_names:
            rg_names.append(student_name)
            with open(self.list_of_risk_student_file, 'w', 
                      encoding='utf-8') as file:
                file.write(', '.join(rg_names))
                
    def look_add_inf_inf(self):
        self.look_add_inf_inf = LookAddInfInf(self)
        self.look_add_inf_inf.show()    
                
        
class CreateClassForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        uic.loadUi('designs/CreateClassForm.ui', self)
        
        self.cr_cl_create_class_button.clicked.connect(self.cr_cl_create_class)
        self.cr_cl_info_button.clicked.connect(self.look_cr_cl_inf)
        
    def cr_cl_create_class(self, *args):
        n_str_keys = 1
        n_str_keys_additional = 2
        protocol_name = self.cr_cl_protocol_name_lineedit.text()
        
        max_score_for_tasks = [1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 
                               2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 
                               1, 6, 1, 1, 2, 2, 3, 3, 2, 2, 1, 1, 25]        
        
        with open(protocol_name) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            data = list(reader)
            
        work_date = data[0][0][len(data[2][1]) - 10:]
        
        for j in range(len(data[n_str_keys])):
            if data[n_str_keys][j].lower() == 'класс':
                if data[n_str_keys + 3][j]:
                    n_key_class = j
            elif data[n_str_keys][j].lower() == 'фио учителя':
                if data[n_str_keys + 3][j]:
                    n_key_teacher_full_name = j
            elif data[n_str_keys][j].lower() == 'фио обучающегося':
                if data[n_str_keys + 2][j]:
                    n_key_student_full_name = j
            elif data[n_str_keys][j].lower() in ('задание 1', '1 задание'):
                task_1 = j
            elif data[n_str_keys][j].lower() in ('задание 27', '27 задание'):
                task_27 = j
                additional_criterion_1 = j
                additional_criterion_12 = j + 11
            elif '27' in data[n_str_keys][j].lower() \
                 and 'итого' in data[n_str_keys][j].lower():
                task_27_total = j
            elif 'первич' in data[n_str_keys][j].lower():
                score = j
            elif 'стобалл' in data[n_str_keys][j].lower():
                score_100 = j
            elif data[n_str_keys][j].lower() in ('оценка', 'отметка'):
                mark = j
                         
        name_class = ''.join(self.cr_cl_class_name_lineedit.text().
                             lower().split())
        
        the_directory = os.getcwd()
        class_main_directory = the_directory + '/' + name_class
        os.mkdir(class_main_directory)
        
        class_actual_directory = class_main_directory + '/' + \
            name_class + ' — актуальная версия'
        risk_group_directory = class_actual_directory + '/' + \
            name_class + ' — группа риска'
        
        os.makedirs(risk_group_directory)
        
        works_directory = class_actual_directory + '/' + \
                    name_class + ' — работы'
        the_work_file = works_directory + '/' + work_date + '.csv'
        os.mkdir(works_directory)
                
        self.list_of_risk_student_file = risk_group_directory + '/' + \
            name_class + ' — группа риска.txt'
        
        self.risk_student_file_csv = risk_group_directory + '/' + \
            name_class + ' — группа риска.csv'
        
        with open(self.list_of_risk_student_file, 
                  'w', encoding='utf-8') as file:
            pass   
        
        the_work = []
        the_work.append(data[n_str_keys][n_key_student_full_name:])
        
        class_score = [0] * 39
        n_students = 0
        
        f_class = False
        
        for row in data:
            if ''.join(row[n_key_class].split()).lower() == \
               ''.join(name_class.lower().split()):
                f_class = True
                row[n_key_student_full_name] = ' '.join(x.capitalize() for x in
                    row[n_key_student_full_name].split())
                if row[score_100]:
                    if int(row[score_100]) <= 39 and row[task_1].lower() not \
                            in ('н', 'отс', 'n'):
                        self.add_to_risk_group_list(
                            row[n_key_student_full_name])
                the_work.append(row[n_key_student_full_name:])                
                
                personal_data = []
                first_row = [data[data.index(row)][n_key_student_full_name]]
                personal_data.append(first_row)
                personal_data.append([])
                third_row = ['Работа (дата)']
                fourth_row = ['']
                fifth_row = [work_date]
                for i in range(task_1, mark + 1):
                    third_row.append(data[n_str_keys][i])
                    fourth_row.append(data[n_str_keys_additional][i])
                    fifth_row.append(row[i])
                personal_data.append(third_row)
                personal_data.append(fourth_row)
                personal_data.append(fifth_row)
                pers_persentage = ['Доля выполнения']
                if row[task_1].lower() not in ('н', 'отс', 'n'):
                    for i in range(1, 40):
                        pers_persent = int(personal_data[4][i]) / \
                            max_score_for_tasks[i - 1]            
                        pers_persentage.append('%.2f' % pers_persent)
                    personal_data.append(pers_persentage)
                else:
                    pers_persentage.append([0] * 39)
                    personal_data.append(pers_persentage)

                full_personal_filename_path = class_actual_directory + '/' \
                    + row[n_key_student_full_name] + '.csv'
                with open(full_personal_filename_path, 
                          'w', newline='') as personal_file:
                    writer=csv.writer(personal_file, delimiter=';', 
                                      quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    for row_pd in personal_data:
                        writer.writerow(row_pd)
                        
                file_lrg = open(self.list_of_risk_student_file, 'r', 
                                encoding='utf-8')
                rg_names = file_lrg.read().split(', ')
                file_lrg.close()

                if row[task_1].lower() not in ('н', 'отс', 'n'):
                    for i in range(task_1, score):
                        class_score[i - task_1] += int(row[i])
                    n_students += 1
        
        if f_class:            
            persentage = ['Доля выполнения']
            for i in range(len(class_score)):
                persent = class_score[i] / (n_students * max_score_for_tasks[i])            
                persentage.append('%.2f' % persent)
            the_work.append(persentage)
            
            with open(the_work_file, 'w', newline='') as work_file:
                writer=csv.writer(work_file, delimiter=';', 
                                  quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row_tw in the_work:
                    writer.writerow(row_tw)
        else:
            pass
        
        self.cr_cl_create_class_button.setEnabled(False)
                        
    def add_to_risk_group_list(self, student_name):
        file1 = open(self.list_of_risk_student_file, 'r', encoding='utf-8')
        rg_names = file1.read().split(', ')
        file1.close()
        if student_name not in rg_names:
            rg_names.append(student_name)
            with open(self.list_of_risk_student_file, 'w', 
                      encoding='utf-8') as file:
                file.write(', '.join(rg_names))
                
    def look_cr_cl_inf(self):
        self.look_cr_cl_inf = LookCrClInf(self)
        self.look_cr_cl_inf.show()        
        

class LookMainInf(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        uic.loadUi('designs/MainInf.ui', self)
        
class LookAddInfInf(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        uic.loadUi('designs/AddInfInf.ui', self)
        
class LookCrClInf(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        uic.loadUi('designs/CrClInf.ui', self)
            
     
        
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainForm()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
