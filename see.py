import requests
import sys
from tabulate import tabulate

if len(sys.argv) != 4:
    sys.exit("enter in valid format !\n*python see.py <symbol> <dob> <academic_year>")

smbl = sys.argv[1]
dob = sys.argv[2]
yr = sys.argv[3]

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://result.see.gov.np',
    'Referer': 'http://result.see.gov.np/result',
    'X-Requested-With': 'XMLHttpRequest',
}

years = {2080:7, 2079:6, 2078:5, 2077:4, 2076:3, 2075:2, 2074: 1}

if int(yr) not in years:
    sys.exit("Only available of following years:\n2080, 2079, 2078, 2077, 2076, 2075, 2074")

data = 'model[AcademicYearId]='+str(years[int(yr)])+'&model[DateOfBirthBS]='+dob+'&model[SymbolNo]='+smbl #'&model%5BAcademicYears%5D%5B0%5D%5BId%5D=7&model%5BAcademicYears%5D%5B0%5D%5BDescription%5D=2080+(+80+)&model%5BAcademicYears%5D%5B1%5D%5BId%5D=6&model%5BAcademicYears%5D%5B1%5D%5BDescription%5D=2079+(+79+)&model%5BAcademicYears%5D%5B2%5D%5BId%5D=5&model%5BAcademicYears%5D%5B2%5D%5BDescription%5D=2078+(+78+)&model%5BAcademicYears%5D%5B3%5D%5BId%5D=4&model%5BAcademicYears%5D%5B3%5D%5BDescription%5D=2077+(+77+)&model%5BAcademicYears%5D%5B4%5D%5BId%5D=3&model%5BAcademicYears%5D%5B4%5D%5BDescription%5D=2076+(+76+)&model%5BAcademicYears%5D%5B5%5D%5BId%5D=2&model%5BAcademicYears%5D%5B5%5D%5BDescription%5D=2075+(+75+)&model%5BAcademicYears%5D%5B6%5D%5BId%5D=1&model%5BAcademicYears%5D%5B6%5D%5BDescription%5D=2074+(+74+)'

response = requests.post('http://result.see.gov.np/Result/Index', headers=headers, data=data, verify=False)

data = response.json()
if not data["IsSuccess"]:
    sys.exit("Something went wrong !")

name = data["Data"]["StudentName"]
symbol = data["Data"]["SymbolNo"]
gender = data["Data"]["Sex"]
school = data["Data"]["SchoolName"]
gpa = data["Data"]["GPA"]

subjects = data["Data"]["MarksRecord"] 
marks=[]
for subject in subjects:
    marks.append([subject["SubjectName"], subject["THOG"], subject["PROG"], subject["TotalOG"], subject["TotalGP"]])
marks.append(["Grade Point Average (GPA)","","","",gpa])

# define the headers
headers = ["SubjectName", "Theory", "Practical", "TotalGrade", "TotalGPA"]
print("Name:", name)
print("Gender:", gender)
print("SchoolName:", school)
print(tabulate(marks, headers=headers, tablefmt="grid"))