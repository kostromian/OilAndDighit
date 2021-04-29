import random

class Company():
    def __init__(self, name, mother, id):
        self.id = id
        self.name = name
        self.atributes = {}
        self.mother = mother

class Buf():
    def __init__(self, name, mother):
        self.name = name
        self.atributes = {}
        self.status = {}
        self.imp_depend = 0 # общая импортозависимость
        self.count_mln_our = 0 # млн инвестировано в отечественные проекты
        self.share_mln_our = 0 # доля инвестированных миллионов в отечественные
        self.count_prj_our = 0 # количество отечественных проектов
        self.share_prj_our = 0 # доля отечественных проектов
        self.count_mln_imp = 0 # млн инвестировано в импортные проекты
        self.share_mln_imp = 0 # доля инвестированных млн в импортные
        self.count_prj_imp = 0 # количество импортных проектов
        self.share_prj_imp = 0 # доля импортных проектов
        self.mother = mother
        self.x = random.randint(0, 100)
        self.y = random.randint(0, 100)

def read_csv(name):
    with open(name, "r") as f:
        text = f.read()
    text = text.split('\n')
    return text

def parser_data(file, companys):
    header_file = file[0].split(';')
    metrics = header_file[3:]
    del file[0]
    for str in file:
        row = str.split(';')
        buf = {}
        company = Company(row[1], row[2], row[0])
        k = 3
        for head in metrics:
            buf_metric = row[k].split()
            buf[head] = [buf_metric]
            k += 1
        company.atributes = buf
        companys.append(company)

    buf_name = []
    new_companys = []
    for company in companys:
        if not company.name in buf_name:
            buf_name.append(company.name)
            new_companys.append(company)
        else:
            for new_c in new_companys:
                if new_c.name == company.name:
                    for k,v in company.atributes.items():
                        new_c.atributes[k].append(company.atributes[k][0])
    return new_companys

def get_metric(buf_company, company, metric):
    m_i = []
    m_o = []
    for i in company.atributes[metric]:
        if i[0][0] == 'i':
            m_i.append(i)
        else:
            m_o.append(i)
    buf_company.atributes[metric] = {}
    buf_company.atributes[metric]['import'] = m_i
    buf_company.atributes[metric]['our'] = m_o

def get_status(buf_company):
    buf_company.status['developed'] = 0
    buf_company.status['implemented'] = 0
    buf_company.status['circulation'] = 0
    for atrib in buf_company.atributes.values():
        for k,v in atrib.items():
            for i in v:
                if i[2] == '1':
                    buf_company.status['developed'] += 1
                elif i[2] == '2':
                    buf_company.status['implemented'] += 1
                else:
                    buf_company.status['circulation'] += 1

def get_depend(buf_company):
    sum_i = 0
    sum_o = 0
    for atribute in buf_company.atributes.values():
        for k,v in atribute.items():
            if k == 'import':
                sum_i += len(v)
            else:
                sum_o += len(v)
    buf_company.count_prj_imp = sum_i
    buf_company.count_prj_our = sum_o
    buf_company.imp_depend = round(sum_i/(sum_i + sum_o)*100)

def get_mln_count(buf_company):
    sum_o = 0
    sum_i = 0
    for atribute in buf_company.atributes.values():
        for k,v in atribute.items():
            if k == 'import':
                for i in v:
                    sum_i += int(i[1])
            else:
                for i in v:
                    sum_o += int(i[1])
    buf_company.count_mln_imp = sum_i
    buf_company.count_mln_our = sum_o

def get_mln_share(buf_company):
    buf_company.share_mln_our = round(buf_company.count_mln_our/(buf_company.count_mln_our +buf_company.count_mln_imp) * 100)
    buf_company.share_mln_imp = round(100 - buf_company.share_mln_our)


def get_prj_share(buf_company):
    buf_company.share_prj_our = round(100 - buf_company.imp_depend)

if __name__ == '__main__':
    data_csv = read_csv('data4.csv')
    listCompany = []
    companys = parser_data(data_csv, listCompany)
    metrics = list(companys[0].atributes.keys())
    statistic_company = []
    for company in companys:
        buf = Buf(companys[0].name, companys[0].mother)
        for metric in metrics:
            get_metric(buf, companys[0], metric)
        get_status(buf)
        get_depend(buf)
        get_mln_count(buf)
        get_mln_share(buf)
        get_prj_share(buf)
        statistic_company.append(buf)

    # print(statistic_company[0].atributes)
    # print(statistic_company[0].status)
    # print(statistic_company[0].count_prj_imp)
    # print(statistic_company[0].count_prj_our)
    # print(statistic_company[0].imp_depend)
    # print(statistic_company[0].count_mln_imp)
    # print(statistic_company[0].count_mln_our)
    # print(statistic_company[0].share_mln_imp)
    # print(statistic_company[0].share_mln_our)
    # print(statistic_company[0].share_prj_our)
