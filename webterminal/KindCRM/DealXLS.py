import xlrd
import xlwt
import calendar
import re
import datetime
import json

# begintime = "8:30"
# endtime = "17:30"
def addtwodict(thedict,key1,key2,val):
    if key1 in thedict:
        thedict[key1].update({key2:val})
    else:
        thedict.update({key1:{key2:val}})

class DealXLS(object):

    def __init__(self):
        #self.result = list()
        self.result = dict()
        self.keys = list()

    def readXLS(self,filename):
        workbook = xlrd.open_workbook(filename,encoding_override='gbk')
        sheet_names= workbook.sheet_names()
        for sheet_name in sheet_names:
            sheet2 = workbook.sheet_by_name(sheet_name)
            print(sheet2.ncols,sheet2.nrows)
            # sheet_name_rows = sheet2.row_values(3) # 获取第四行内容
            # cols = sheet2.col_values(1) # 获取第二列内容
            self.keys = sheet2.row_values(0)
            for i in range(1,sheet2.nrows):
                sheet_name_rows = sheet2.row_values(i)
                list(map(lambda x:x.strip(),[str(x) for x in sheet_name_rows]))
                try:
                    self.result[sheet_name_rows[0]][sheet_name_rows[1]]
                except KeyError:
                    addtwodict(self.result,sheet_name_rows[0],sheet_name_rows[1],list())
                self.result[sheet_name_rows[0]][sheet_name_rows[1]].append(sheet_name_rows)
                print("num:%s name:%s len:%s"%(sheet_name_rows[0],sheet_name_rows[1],len(self.result[sheet_name_rows[0]][sheet_name_rows[1]])))


    def writeXLS(self,filename):
        wb = xlwt.Workbook()
        sheet = wb.add_sheet("my worksheet",cell_overwrite_ok=True)
        matchObj = re.search(r'(\d{4})\-(\d{1,2})\-(\d{1,2})', filename)
        if matchObj:
            year = matchObj.group(1)
            month = matchObj.group(2)
            day = matchObj.group(3)
        (workday,days) = calendar.monthrange(int(year),int(month))
        header = ['序号','姓名','岗位']
        list(map(lambda x:header.append(x),[ str(day) for day in range(1,days+1)]))
        header = header + ['','备注','扣款','签字确认']
        i = 0
        for option in header:
            sheet.write(0,i,option)
            i += 1
        startseq = 0
        print(self.result)
        for employeenum,employeeinfo in self.result.items():
            startseq += 1
            flag = 1
            for employeename,employeedetail in employeeinfo.items():

                for detailinfo in employeedetail:
                    if flag == 1:
                        sheet.write(startseq,0,startseq)
                        sheet.write(startseq,1,detailinfo[1])
                        sheet.write(startseq, 2, detailinfo[2])
                    isnormal = True if detailinfo[12] == 1 else False
                    #print("+"*10,detailinfo[2])
                    if detailinfo[2] == None or detailinfo[2] == "":
                        continue
                    day = re.match(r'\d+\-\d+\-(\d+)',detailinfo[2]).group(1)
                    print("employeename:", employeename, len(employeedetail),day)
                    data = chr(8730) if isnormal else ""
                    cols = int(day) + 2
                    sheet.write(startseq,cols,data)
        wb.save(filename)

    def getstatus(self,*args,**kwargs):
        if args[2] == 1:
            return True
        elif args[2] == 0:
            return False
        else:
            if args[0]:
                (hours,minus) = re.match(r'(\d+)\:(\d+)',args[0])
                if int(hours) < 8:
                    return args[1]
                else:
                    return args[0]
            else:
                return args[0]




if __name__ == '__main__':
    obj= DealXLS()
    obj.readXLS("KQ_file/2018-6-30.xls")
    obj.writeXLS("KQ_file/2018-06-30-result.xls")

