# 데이터 모니터링 및 시각화 : 시간 간격 모니터링, 로트추가, USL, LSL, Max, Mink값 추가
from tkinter import *
import matplotlib
from babel.numbers import *
from tkinter import ttk
import numpy as np
import pymysql
import csv
import tkinter.messagebox
# import gradio  # 웹앱 구현시
from tkinter import messagebox
import matplotlib.pyplot as plt
# plt.rcParams['axes.unicode_minus'] = False
# matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.font_manager as fm
from matplotlib.animation import FuncAnimation
from itertools import count
import matplotlib.pyplot as plt2
import pandas as pd
from tkcalendar import DateEntry
import statistics
import datetime as dt

root = Tk()
root.title("데이터 시각화")
root.geometry('{}x{}'.format(1400, 750))
root.resizable(width=True, height=True)

# from tkinter import *
# import menubar as menubar
# from babel.numbers import *
# from tkinter import ttk
# import numpy as np
# import pymysql
# import csv
# import tkinter.messagebox
# from tkinter import messagebox
# import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm
# from matplotlib.animation import FuncAnimation
# import pandas as pd
# from tkcalendar import DateEntry

# root = Tk()
# monitor_height = root.winfo_screenheight()  #모니터 해상도 가로 크기를 가져옴
# monitor_width = root.winfo_screenwidth()    #모니터 해상도 세로 크기를 가져옴
# root.title("데이터 시각화")
# # root.grid(font= "arial", size = 20)
# root.geometry('{}x{}'.format(1400,700))
# # root.geometry('{}x{}'.format(monitor_height, monitor_width))
# root.resizable(width=True, height=True)


q1 = StringVar()        # 월 시작일자 변수 선업 / q1과 cal1 ?
q2 = StringVar()        # 월 시작일자 변수 선언
q3 = StringVar()        # 장비 선택 변수 선언
q4 = StringVar()        # 품번 선택 변수 선언
q5 = StringVar()        # 타점 시간 선택 선업
cal1 = StringVar()          # 월 시작일자 선택  - 전역변수로 설정할 것 글로벌 노
cal2 = StringVar()          # 월 종료일자 선택
i_textEntry = StringVar()   # 품번 입력 변수
i_cmbWno = StringVar()      # 장비 콤보 리스트 변수 선언
i_cmbWno1 = StringVar()     # 타점 간격시간 콤보 리스트 변수 선언
total_cnt0 = StringVar()      # 온도 카운트 변수 선언
total_cnt1 = StringVar()      # 속도 카운트 변수 선언
total_cnt2 = StringVar()      # 수분 카운트 변수 선언
interval_time1 = StringVar()     # 타점 간격시간/  # 1분 60초 ,  10초 (1000 = 1초)  타점시간 간격
year1 = dt.datetime.now()
year_date = year1.year   # 해당 년도를 가져옴

# total_max1 = StringVar() # 셋팅온도/속도 최소값(min)
# total_max2 = StringVar()  # 수분 최소값(min)
# total_max0 = StringVar()  # 값이 없을 경우 최소값(min)
# total_min1 = StringVar()  # 셋팅온도 최소값(min)
# total_min2 = StringVar() # 속도 최소값(min)
# total_min0 = StringVar()  # 값이 없을 경우 최소값(min)
interval_time = 5000

# 서버 정보 입력  ===============================
company_name = "와이파인텍(주)"
host_ip = "211.43.12.154"
port_no = 33306
user_id = "kovis"
password_no = "wf#00599"
db_name = "k102wf"
charset_no = "utf8"

list_3 = ["킬른1호기", "킬른2호기", "킬른3호기", "수분측정_1층", "수분측정_2층"]
list_4 = ["3초", "5초", "10초", "30초"]   # 타점간격 시간
list_5_time = {'3초':3000, '5초':5000, '10초':10000, '30초':30000}    # 타점간격 시간
# # list_4 = ["5초", "10초", "30초", "1분", "2분", "5분", "10분"]   # 타점간격 시간
# list_5_time = {'5초':5000, '10초':10000, '30초':30000, '1분':60000, '2분':120000, '5분':300000, '10분':600000}    # 타점간격 시간
# list_3 = ["", "킬른1호기", "킬른2호기", "킬른3호기", "수분측정_1층", "수분측정_2층"]  #조건 공란시 "" 추가


def donothing():
    print('Just Do nothing Brooo....')

# 상단 메뉴 만들기 ==================================================================================================
# main start
TopMenu = Menu(root)
root.config(menu = TopMenu)

# file Menu
submenu1 = Menu(TopMenu, tearoff=0)
TopMenu.add_cascade(menu=submenu1, label = "File")
submenu1.add_command(label = "Open File", command=donothing)
submenu1.add_command(label = "Save", command=donothing)
submenu1.add_command(label = "Save as", command=donothing)
submenu1.add_separator()
submenu1.add_command(label="Exit", command= root.quit)

# edit Menu
submenu2 = Menu(TopMenu, tearoff=0)
TopMenu.add_cascade(menu=submenu2, label = "Edit")
submenu2.add_command(label = "Undo", command=donothing)
submenu2.add_separator()
submenu2.add_command(label = "Cut", command=donothing)
submenu2.add_command(label = "Copy", command=donothing)
submenu2.add_command(label = "Delete", command=donothing)
submenu2.add_command(label = "Select All", command=donothing)

# help Menu
helpmenu = Menu(TopMenu, tearoff=0)
TopMenu.add_cascade(menu=helpmenu, label = "Help")
helpmenu.add_command(label = "Help Index", command=donothing)
helpmenu.add_command(label = "About...", command=donothing)

# 관리한계선 UCL, LCL 계산시 A2, D3, D4 상수 계산(관리도 계수표)  ====================================================================
def A2_cal(sample_n):    #sample_n 샘플링수
    global A2
    global D3
    global D4

    d2_list= {2:1.128, 3:1.693, 4:2.059, 5:2.326, 6:2.534, 7:2.704, 8:2.847, 9:2.97, 10:3.078, 11:3.173, 12:3.258, 13:3.336, 14:3.407, 15:3.472, 16:3.532, 17:3.588, 18:3.64, 19:3.689, 20:3.735}
    d3_list= {2:0.8525, 3:0.8884, 4:0.8798, 5:0.8641, 6:0.848, 7:0.8332, 8:0.8198, 9:0.8078, 10:0.7971, 11:0.7873, 12:0.7785, 13:0.7704, 14:0.763, 15:0.7562, 16:0.7499, 17:0.7441, 18:0.7386, 19:0.7335, 20:0.7287}
    d4_list= {2:0.954, 3:1.588, 4:1.978, 5:2.257, 6:2.472, 7:2.645, 8:2.791, 9:2.915, 10:3.024, 11:3.121, 12:3.207, 13:3.285, 14:3.356, 15:3.422, 16:3.482, 17:3.538, 18:3.591, 19:3.64, 20:3.686}

    A2 = 3 / (d2_list[sample_n] * (sample_n ** 0.5))        # xbar UCL, LCL 계산 상수값
    D4 = 1 + (3*(d3_list[sample_n]/d2_list[sample_n]))      # R UCL, LCL 계산 상수값
    D3 = 1 - (3*(d3_list[sample_n]/d2_list[sample_n]))      # R UCL, LCL 계산 상수값

# ==Function============================================================================================================
def btnClose():
    root.quit()

# == 그래프 자동 업데이트 ============================================================================================================
def animate1(i):
    plt.clf()  # 그래프 초기화
    q1 = cal1.get()  # 전역변수로 설정할 것 글로벌 노
    q2 = cal2.get()
    q3 = i_cmbWno.get()   # 장비 선택
    q4 = i_textEntry.get() # 품번 입력
    conn = pymysql.connect(host=host_ip, port=port_no, user=user_id, password=password_no, db=db_name,
                           charset=charset_no)
    curs = conn.cursor()
    sql = "SELECT a.id, a.v11, a.v12, b.wtit, d.bno, b.wno  FROM k7dg a \
                               left join aw b on a.wcd = b.wcd \
                               left join wo c on a.lno = c.oid \
                               left join ab d on c.bcd = d.bcd \
                               WHERE DATE_FORMAT(a.itime, '%Y-%m-%d%h%i%s%') between '" + q1 + '000000' + "' and '" + q2 + '235959' + "' \
                               and wtit LIKE '" + q3 + "' \
                               and bno LIKE '%" + q4 + "%' \
                               order by id asc;"

    f = open('wifine_temp1.csv', 'w', encoding='utf-8', newline='')

    wr = csv.writer(f)
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        wr.writerow([row[1], row[2]])
    conn.commit()
    conn.close()
    f.close()
    # print(row)

    # 라인 그래프 그리기 ===================================
    df = pd.read_csv("./wifine_temp1.csv", header=None, names=['temp1', 'temp2'])
    plt.style.use('fivethirtyeight')
    plt.rc('font', family='Malgun Gothic')

    plt.cla()
    plt.plot(df['temp1'], 'o--', label='셋업온도', color='red', linewidth=1)
    plt.plot(df['temp2'], '*--', label='내부온도', color='blue', linewidth=1)
    plt.title(company_name + ' 건조기 Data 수집 및 분석', fontsize=15)
    # plt.legend(loc='best')
    plt.xlabel('시간(1분 간격)', fontsize=11)
    plt.ylabel('온도(℃)', fontsize=11)

    # Max, min값 구하기
    temp_min_id1 = np.argmin(df.temp1)  # get min id in all
    temp_max_id1 = np.argmax(df.temp1)  # get max id in all
    temp_min_id2 = np.argmin(df.temp2)  # get min id in all
    temp_max_id2 = np.argmax(df.temp2)  # get max id in all
    print("temp_min_id1 = ", temp_min_id1)
    print("temp_max_id1 = ", temp_max_id1)
    print("temp_min_id2 = ", temp_min_id2)
    print("temp_max_id2 = ", temp_max_id2)

    # temp_max_id1 = np.argmax(temp_max_id1[df.temp1 < 0.59])  # get max in specific range 관리범위 UCL 내
    # temp_min_id1 = np.argmin(temp_min_id1[(df.temp1 > 0.56) & (df.temp1 < 0.62)])  # get min in specific range 관리범위 LCL 내

    # Max, min값 그래프에 표시하기
    plt.plot(temp_max_id1, df.temp1[temp_max_id1], 'v', label=round(df.temp1[temp_max_id1], 2), ms=10, color='cyan')
    plt.plot(temp_max_id1, df.temp1[temp_max_id1], '+', label=round(temp_max_id1, 2), ms=10, color='black')
    plt.plot(temp_min_id1, df.temp1[temp_min_id1], '^', label=round(df.temp1[temp_min_id1], 2), ms=10, color='cyan')
    plt.plot(temp_min_id1, df.temp1[temp_min_id1], '+', label=round(temp_min_id1, 2), ms=10, color='black')
    plt.plot(temp_max_id2, df.temp2[temp_max_id2], 'v', label=round(df.temp2[temp_max_id2], 2), ms=10, color='yellow')
    plt.plot(temp_max_id2, df.temp2[temp_max_id2], '+', label=round(temp_max_id2, 2), ms=10, color='black')
    plt.plot(temp_min_id2, df.temp2[temp_min_id2], '^', label=round(df.temp2[temp_min_id2], 2), ms=10, color='yellow')
    plt.plot(temp_min_id2, df.temp2[temp_min_id2], '+', label=round(temp_min_id2, 2), ms=10, color='black')
    # plt.plot(temp_min_id2, df.temp2[temp_min_id2], 'o', label=round(temp_min_id2, 2), ms=10, color='yellow')
    plt.text(temp_min_id1, df.temp1[temp_min_id1], 'Min 온도(셋업)', fontsize=14, color='r', va='baseline', ha='left')
    plt.text(temp_max_id1, df.temp1[temp_max_id1], 'Max 온도(셋업)', fontsize=14, color='r', va='baseline', ha='left')
    plt.text(temp_min_id2, df.temp1[temp_min_id2], 'Min 온도(내부)', fontsize=14, color='b', va='baseline', ha='left')
    plt.text(temp_max_id2, df.temp1[temp_max_id2], 'Max 온도(내부)', fontsize=14, color='b', va='baseline', ha='left')
    plt.legend(loc='best', ncol=1, fontsize=10, frameon=False, shadow=False)    # 범례 표시하기
    # df.annotate('MAX온도', xy=(temp_max_id1, df.temp1[temp_max_id1]), xytext=(temp_max_id1, df.temp1[temp_max_id1]+20), arrowprops=dict(arrowstyle='->', color='gray'))
    # df.annotate('MAX온도', xy=(temp_max_id1, df.temp1[temp_max_id1]), xytext=(0.7, 0.95), fontsize=14, textcoords='axes fraction', arrowprops=dict(arrowstyle='->', color='gray', connectionstyle='arc3, rad=-.2'))
    # df.annotate('MAX온도', xy=(temp_max_id1, df.temp1[temp_max_id1]), xytext=(0.7, 0.95), fontsize=14, textcoords='axes fraction', arrowprops=dict(facecolor='black', width=1, shrink=0.1, headwidth=10))
    # Max, min값 그래프에 표시하기

# # 사례 1
# bb_f_text = '여아출생수: %d' %babyboom_f
# bb_m_text = '여아출생수: %d' %babyboom_m
# bbox_props_f = dict(boxstyle='round', fc='w', ec='r', lw=2) # 박스스타일 둥근모서리 사각형, fc='w' 사각형을 흰색으로 채움, ec='r' 외곽선을 빨간색 선, lw = w 선두께를 2
# bbox_props_m = dict(boxstyle='round', fc='w', ec='b', lw=2)
# ax.annotate(bb_f_text, (1958, babyboom_f), xytext=(0.8, 0.95), textcoords='axes fraction', bbox=bbox_props_f)   #xytext의 인자는 가로방향, 세로방향의 비율로 지정
# ax.annotate(bb_f_text, (1958, babyboom_m), xytext=(0.8, 0.95),
#             textcoords='axes fraction', bbox=bbox_props_f)

def animate2(i):
    plt.clf()  # 그래프 초기화
    q1 = cal1.get()  # 전역변수로 설정할 것 글로벌 노
    q2 = cal2.get()
    q3 = i_cmbWno.get()   # 장비 선택
    q4 = i_textEntry.get() # 품번 입력
    conn = pymysql.connect(host=host_ip, port=port_no, user=user_id, password=password_no, db=db_name,
                           charset=charset_no)
    curs = conn.cursor()
    sql = "SELECT a.id, a.v13, a.v14, b.wtit, d.bno, b.wno  FROM k7dg a \
            left join aw b on a.wcd = b.wcd \
            left join wo c on a.lno = c.oid \
            left join ab d on c.bcd = d.bcd \
            WHERE DATE_FORMAT(a.itime, '%Y-%m-%d%h%i%s%') between '" + q1 + '000000' + "' and '" + q2 + '235959' + "' \
            and wtit LIKE '" + q3 + "' \
            and bno LIKE '%" + q4 + "%' \
            order by id asc;"

    f = open('wifine_sp1.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        wr.writerow([row[1], row[2]])
    conn.commit()
    conn.close()
    f.close()

    # 1개 라인 그래프 그리기 ===================================
    df = pd.read_csv("./wifine_sp1.csv", header=None, names=['sp1', 'sp2'])
    plt.style.use('fivethirtyeight')
    plt.rc('font', family='Malgun Gothic')
    plt.cla()
    plt.plot(df['sp1'], 'o--', label='투입속도', color='red', linewidth=1)
    plt.plot(df['sp2'], '*--', label='내부속도', color='blue', linewidth=1)
    plt.title(company_name + ' 건조기 Data 수집 및 분석', fontsize=16)
    plt.legend(loc='best')
    plt.ylabel('속도(Hz)', fontsize=11)
    plt.xlabel('시간(1분 간격)', fontsize=11)

    # # 상하 2개 그래프 그리기 ===================================
    # df = pd.read_csv("./wifine_sp1.csv", header=None, names=['sp1', 'sp2'])
    # plt.style.use('fivethirtyeight')
    # plt.rc('font', family='Malgun Gothic')
    #
    # plt.cla()
    # ax1 = plt.subplot(2, 1, 1)
    # ax2 = plt.subplot(2, 1, 2)
    # ax1.plot(df['sp1'], 'o--', label='투입속도', color='red', linewidth=1)
    # ax2.plot(df['sp2'], '*--', label='내부속도', color='blue', linewidth=1)
    #
    # ax1.set_title("투입속도")
    # ax2.set_title("내부속도")
    # plt.legend(loc='best')
    # plt.ylabel('속도(Hz)', fontsize=11)
    # plt.xlabel('시간(1분 간격)', fontsize=11)

def animate3(i):
    plt.clf()  # 그래프 초기화
    q1 = cal1.get()  # 전역변수로 설정할 것 글로벌 노
    q2 = cal2.get()
    q3 = i_cmbWno.get()   # 장비 선택
    q4 = i_textEntry.get() # 품번 입력

    conn = pymysql.connect(host=host_ip, port=port_no, user=user_id, password=password_no, db=db_name,
                           charset=charset_no)
    curs = conn.cursor()
    sql = "SELECT a.id, a.v21, b.wtit, d.bno, b.wno  FROM k7dg a \
          left join aw b on a.wcd = b.wcd \
          left join wo c on a.lno = c.oid \
          left join ab d on c.bcd = d.bcd \
          WHERE DATE_FORMAT(a.itime, '%Y-%m-%d%h%i%s%') between '" + q1 + '000000' + "' and '" + q2 + '235959' + "' \
          and wtit LIKE '%" + q3 + "%' \
          and bno LIKE '%" + q4 + "%' \
          order by id asc;"

    f = open('wifine_mo1.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        wr.writerow([row[1]])
    conn.commit()
    conn.close()
    f.close()

    # 히스토그램 그리기1  ========================================================
    df = pd.read_csv("./wifine_mo1.csv", header=None, names=['mo1'])

    plt.style.use('fivethirtyeight')
    plt.rc('font', family='Malgun Gothic')
    bar_su = round(float(total_cnt2) ** (1 / 2))  # 히스토그램 구간의 계급의 수를 구함
    # bar_su = 5 * log10(length(total_cnt2))  # 경험치에 의한 방법
    # bar_su = 1 + 3.3 * math.log(total_cnt2)           # k:계급의 수, N:총 도수
    plt.cla()
    plt.hist(x=df['mo1'], bins=bar_su, rwidth=0.70, label='수분', color='blue')  # bins=10 막대수
    plt.title(company_name + 'IoT 공정 모니터링', fontsize=16)
    plt.legend(loc='best')
    plt.ylabel('수분', fontsize=11)
    plt.xlabel('시간(1분 간격)', fontsize=11)

    # 히스토그램 그리기2  ========================================================
    # df = pd.read_csv("./wifine_mo1.csv", header=None, names=['mo1'])
    # # df.columns()  # 컬럼명이 있는 경우만 사용
    # bar_su = round(float(total_cnt2)**(1/2))   # 히스토그램 구간의 계급의 수를 구함
    # # bar_su = round(total_cnt2**(1/2))   # 히스토그램 구간의 계급의 수를 구함
    # plt.cla()
    # df.plot(kind='hist', bins=bar_su, color='coral', figsize=(10, 5))
    # plt.title(company_name + ' IoT 공정 모니터링', fontsize=20)
    # plt.ylabel('수분', fontsize=12)
    # plt.xlabel('시간(1분 간격)', fontsize=12)

def animate4(i):      # Xbar 관리도 그리기
    plt.clf()  # 그래프 초기화
    q1 = cal1.get()  # 전역변수로 설정할 것 글로벌 노
    q2 = cal2.get()
    q3 = i_cmbWno.get()  # 장비 선택
    q4 = i_textEntry.get()  # 품번 입력
    conn = pymysql.connect(host=host_ip, port=port_no, user=user_id, password=password_no, db=db_name,
                           charset=charset_no)
    curs = conn.cursor()
    sql = "SELECT a.id, a.v11, a.v12, b.wtit, d.bno, b.wno  FROM k7dg a \
                               left join aw b on a.wcd = b.wcd \
                               left join wo c on a.lno = c.oid \
                               left join ab d on c.bcd = d.bcd \
                               WHERE DATE_FORMAT(a.itime, '%Y-%m-%d%h%i%s%') between '" + q1 + '000000' + "' and '" + q2 + '235959' + "' \
                               and wtit LIKE '" + q3 + "' \
                               and bno LIKE '%" + q4 + "%' \
                               order by id asc;"

    f = open('wifine_temp1.csv', 'w', encoding='utf-8', newline='')

    wr = csv.writer(f)
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        wr.writerow([row[1], row[2]])
    conn.commit()
    conn.close()
    f.close()

    df = pd.read_csv("./wifine_temp1.csv", header=None, names=['temp1', 'temp2'])

    temp_x_bar = []     # average
    temp_r = []         # range of the values
    temp_s = []         # standard deviation
    total_low = df.shape[0]
    sample_su = df.shape[1]  # 샘플 수 확인
    print("df = ", df)                    # 값 확인용
    print("total_low = ", total_low)      # 값 확인용
    print("sample_su = ", sample_su)      # 값 확인용

    for group in np.array(df):
        temp_x_bar.append(group.mean())
        temp_r.append(group.max() - group.min())
        temp_s.append(np.std(group))

    A2_cal(sample_su)   # A2 값 계산
    print(temp_x_bar, temp_r, temp_s, A2_cal)  # 값 확인용

    # Xbar Chart ==========================================================================================================
    fig = plt.figure(figsize=(15, 8))
    plt.rc('font', family='Malgun Gothic')
    plt.plot(temp_x_bar, linestyle='-', marker='o', color='black')
    plt.axhline((statistics.mean(temp_x_bar) + A2 * statistics.mean(temp_r)), color='red', linestyle='--')
    plt.axhline((statistics.mean(temp_x_bar) - A2 * statistics.mean(temp_r)), color='red', linestyle='dashed')
    plt.axhline((statistics.mean(temp_x_bar)), color='blue')
    plt.title('X-bar Chart(TEST)', fontsize=20)
    plt.xlabel('온도', fontsize=15)
    plt.ylabel('평균(Mean)', fontsize=15)
    plt.show()

    # # UCL, LCL을 벗어나는 값의 리스트 보기
    temp_out_list = []  # UCL, LCL을 벗어나는 값의 리스트
    i = 0
    controled = True
    for group in temp_x_bar:
        if group > statistics.mean(temp_x_bar) + A2 * statistics.mean(temp_r) or \
                group < statistics.mean(temp_x_bar) - A2 * statistics.mean(temp_r):
            tkinter.messagebox.showwarning("경고 메세지(Warning!)", '관리한계선을 벗어난 리스트 : number {}'.format(i))
            print('관리한계선을 벗어난 리스트 -> number {}'.format(i))
            temp_out_list.append(i)
            controled = False
        i += 1

    if controled == True:
        tkinter.messagebox.showwarning("결과 메세지(Good!)", "모든 값이 관리범위 내에 존재함!")
        print('모든 값이 관리범위 내에 존재함!')

# == 온도 grape display==================================================================================================
def btnLinegraph1():
    plt.close()
    # plt.clf()  # 그래프 초기화
    q1 = cal1.get()  # 전역변수로 설정할 것 글로벌 노
    q2 = cal2.get()
    q3 = i_cmbWno.get()   # 장비 선택
    q4 = i_textEntry.get() # 품번 입력
    q5 = i_cmbWno1.get()    # 타점 시간 선택
    interval_time1 = list_5_time[q5]      # 타점 시간 선택
    # print("interval_time1 = ", interval_time1)

    if (q3 == "" or q4 == ""):  # 미입력시 오류 메세지 조건문
        tkinter.messagebox.showwarning("필수조건 입력", "장비번호와 품목번호를 입력하세요")
    elif (q3 == list_3[3] or q3 == list_3[4]):
        tkinter.messagebox.showwarning("장비선택 오류", "생산 장비번호로 변경하세요^^!")
    elif (total_cnt1 == 0):
        tkinter.messagebox.showwarning("에러 메세지", "입력 데이터가 없습니다.")
    elif (q3 == list_3[0] or q3 == list_3[1] or q3 == list_3[2]):
        ani = FuncAnimation(plt.gcf(), animate1, interval=interval_time1)
        plt.tight_layout()
        plt.show()

    else:
        tkinter.messagebox.showwarning("에러 메세지", "검색조건을 확인하세요^^!")

# 속도 그래프 display =======================================================
def btnLinegraph2():
    plt.close()
    # plt.clf()  # 그래프 초기화
    q1 = cal1.get()  # 전역변수로 설정할 것 글로벌 노
    q2 = cal2.get()
    q3 = i_cmbWno.get()   # 장비 선택
    q4 = i_textEntry.get() # 품번 입력
    q5 = i_cmbWno1.get()    # 타점 시간 선택
    interval_time1 = list_5_time[q5]

    print(total_cnt0, total_cnt2, total_cnt2)
    if (q3 == "" or q4 == ""):  # 미입력시 오류 메세지 조건문
        tkinter.messagebox.showwarning("필수조건 입력", "장비번호와 품목번호를 입력하세요")
    elif (q3 == list_3[3] or q3 == list_3[4]):
        tkinter.messagebox.showwarning("장비선택 오류", "생산 장비번호로 변경하세요^^!")
    elif (total_cnt2 == 0):
        tkinter.messagebox.showwarning("에러 메세지", "입력 데이터가 없습니다.")
    elif (q3 == list_3[0] or q3 == list_3[1] or q3 == list_3[2]):
        ani = FuncAnimation(plt.gcf(), animate2, interval=interval_time1)
        plt.tight_layout()
        plt.show()

    else:
        tkinter.messagebox.showwarning("에러 메세지", "검색조건을 확인하세요^^!")

# 수분 그프 display =======================================================
def btnLinegraph3():
    plt.close()
    # plt.clf()  # 그래프 초기화
    q1 = cal1.get()  # 전역변수로 설정할 것 글로벌 노
    q2 = cal2.get()
    q3 = i_cmbWno.get()   # 장비 선택
    q4 = i_textEntry.get() # 품번 입력
    q5 = i_cmbWno1.get()    # 타점 시간 선택
    interval_time1 = list_5_time[q5]

    if (q3 == "" or q4 == ""):  # 미입력시 오류 메세지 조건문
        tkinter.messagebox.showwarning("필수조건 입력", "장비번호와 품목번호를 입력하세요")
    elif (q3 == list_3[0] or q3 == list_3[1] or q3 == list_3[2]):
        tkinter.messagebox.showwarning("장비선택 오류", "측정 장비번호로 변경하세요^^!")
    elif (total_cnt0 == 0):
        tkinter.messagebox.showwarning("에러 메세지", "입력 데이터가 없습니다.")
    elif (q3 == list_3[3] or q3 == list_3[4]):
        ani = FuncAnimation(plt.gcf(), animate3, interval=interval_time1)
        plt.tight_layout()
        plt.show()

    else:
        tkinter.messagebox.showwarning("에러 메세지", "검색조건을 확인하세요^^!")

# Xbar 관리도 그리기
def Xbar_chart1():
    plt.close()
    # plt.clf()  # 그래프 초기화
    q1 = cal1.get()  # 전역변수로 설정할 것 글로벌 노
    q2 = cal2.get()
    q3 = i_cmbWno.get()   # 장비 선택
    q4 = i_textEntry.get() # 품번 입력
    q5 = i_cmbWno1.get()    # 타점 시간 선택
    interval_time1 = list_5_time[q5]      # 타점 시간 선택

    if (q3 == "" or q4 == ""):  # 미입력시 오류 메세지 조건문
        tkinter.messagebox.showwarning("필수조건 입력", "장비번호와 품목번호를 입력하세요")
    elif (q3 == list_3[3] or q3 == list_3[4]):
        tkinter.messagebox.showwarning("장비선택 오류", "생산 장비번호로 변경하세요^^!")
    elif (total_cnt1 == 0):
        tkinter.messagebox.showwarning("에러 메세지", "입력 데이터가 없습니다.")
    elif (q3 == list_3[0] or q3 == list_3[1] or q3 == list_3[2]):
        ani = FuncAnimation(plt.gcf(), animate4, interval=interval_time1)
        plt.tight_layout()
        plt.show()

    else:
        tkinter.messagebox.showwarning("에러 메세지", "검색조건을 확인하세요^^!")

# 버튼 내용 삭제 =======================================================
def btnConditionReset():
    # cal1.set("")
    # cal2.set("")
    i_cmbWno.set("")
    i_cmbWno1.set("")
    i_textEntry.set("")

    # q1 = cal1.get()  # 전역변수로 설정할 것 글로벌 노
    # q2 = cal2.get()
    # q3 = i_cmbWno.get()   # 장비 선택
    # q4 = i_textEntry.get() # 품번 입력
    # q5 = i_cmbWno1.get()    # 타점 시간 선택

# 테이블 검색하기 ========================================================
def btnSelect():  # 검색실행 버튼 클릭~
    q1 = cal1.get()  # 전역변수로 설정할 것 글로벌 노
    q2 = cal2.get()
    q3 = i_cmbWno.get()   # 장비 선택
    q4 = i_textEntry.get() # 품번 입력
    q5 = i_cmbWno1.get()    # 타점 시간 선택

    global total_cnt0
    global total_cnt1
    global total_cnt2
    global total_t_min0  # 셋팅온도 최소값(min)
    global total_t_max0  # 셋팅온도 최대값(max)
    global total_t_min1  # 내부온도 최소값(min)
    global total_t_max1  # 내부온도 최대값(max)
    global total_s_min2  # 투입속도 최소값(min)
    global total_s_max2  # 투입속도 최대값(max)
    global total_s_min3  # 내부속도 최소값(min)
    global total_s_max3  # 내부속도 최대값(max)
    global total_m_min4  # 수분 최소값(min)
    global total_m_max4  # 수분 최대값(max)

    conn = pymysql.connect(host=host_ip, port=port_no, user=user_id, password=password_no, db=db_name,
                           charset=charset_no)
    curs = conn.cursor()
    sql = "SELECT a.id, a.itime, case a.stat when '1' then '가동' when '0' then '비가동' else '수분' end as stat, \
          b.wtit, d.bno, d.btit, a.v11, a.v12, a.v13, a.v14, a.v21, a.lno \
          FROM k7dg a \
          left join aw b on a.wcd = b.wcd \
          left join wo c on a.lno = c.oid \
          left join ab d on c.bcd = d.bcd \
          WHERE DATE_FORMAT(a.itime, '%Y-%m-%d%h%i%s%') between '" + q1 + '000000' + "' and '" + q2 + '235959' + "' \
          and wtit LIKE '%" + q3 + "%' AND bno LIKE '%" + q4 + "%' \
          order by id desc;"

    # print(sql)
    curs.execute(sql)
    rows = curs.fetchall()
    conn.commit()
    # conn.close()
    update(rows)

    # 다중 select문을 통해 카운터값을 계산
    # count 불러오기
    sql1 = "select f.cnt0, a.cnt1, e.cnt2 from \
        (select count(f.id) as cnt0 from k7dg f \
        left join aw b on f.wcd = b.wcd \
        left join wo c on f.lno = c.oid \
        left join ab d on c.bcd = d.bcd \
        WHERE DATE_FORMAT(f.itime, '%Y-%m-%d%h%i%s%') between '" + q1 + '000000' + "' and '" + q2 + '235959' + "' \
        and wtit LIKE '%" + q3 + "%' AND bno LIKE '%" + q4 + "%') f, \
        (select count(a.v11) as cnt1 from k7dg a \
        left join aw b on a.wcd = b.wcd \
        left join wo c on a.lno = c.oid \
        left join ab d on c.bcd = d.bcd \
        WHERE DATE_FORMAT(a.itime, '%Y-%m-%d%h%i%s%') between '" + q1 + '000000' + "' and '" + q2 + '235959' + "' \
        and wtit LIKE '%" + q3 + "%' AND bno LIKE '%" + q4 + "%') a, \
        (select count(e.v21) as cnt2 from k7dg e \
        left join aw b on e.wcd = b.wcd \
        left join wo c on e.lno = c.oid \
        left join ab d on c.bcd = d.bcd \
        WHERE DATE_FORMAT(e.itime, '%Y-%m-%d%h%i%s%') between '" + q1 + '000000' + "' and '" + q2 + '235959' + "' \
        and wtit LIKE '%" + q3 + "%' AND bno LIKE '%" + q4 + "%') e;"

    curs.execute(sql1)
    row_cnt = curs.fetchall()
    total_cnt0 = format(row_cnt[0][0], ',d')  # 장비번호, 품목번호로 조건이 없을 경우 전체 카운터 수
    total_cnt1 = format(row_cnt[0][1], ',d')  # 온도 속도 측정 카운터 수
    total_cnt2 = format(row_cnt[0][2], ',d')  # 수분 측정 카운터 수
    print(total_cnt0, total_cnt1, total_cnt2)   # count 확인용
    conn.commit()
    # conn.close()

    # 최소값, 최대값 불러오기
    sql = "select min(e.v11),max(e.v11), min(e.v12), max(e.v12), min(e.v13), max(e.v13), min(e.v14),max(e.v14), min(f.v21), max(f.v21) from \
        (SELECT a.id, a.itime, case a.stat when '1' then '가동' when '0' then '비가동' else '수분' end as stat, \
        b.wtit, d.bno, d.btit, a.v11, a.v12, a.v13, a.v14, a.v21, a.lno \
        FROM k7dg a \
        left join aw b on a.wcd = b.wcd \
        left join wo c on a.lno = c.oid \
        left join ab d on c.bcd = d.bcd \
        WHERE DATE_FORMAT(a.itime, '%Y-%m-%d%h%i%s%') between '" + q1 + '000000' + "' and '" + q2 + '235959' + "' \
        and wtit LIKE '%" + q3 + "%' AND bno LIKE '%" + q4 + "%') e, \
        (SELECT a.id, a.itime, case a.stat when '1' then '가동' when '0' then '비가동' else '수분' end as stat, \
        b.wtit, d.bno, d.btit, a.v11, a.v12, a.v13, a.v14, a.v21, a.lno \
        FROM k7dg a \
        left join aw b on a.wcd = b.wcd \
        left join wo c on a.lno = c.oid \
        left join ab d on c.bcd = d.bcd \
        WHERE DATE_FORMAT(a.itime, '%Y-%m-%d%h%i%s%') between '" + q1 + '000000' + "' and '" + q2 + '235959' + "' \
        and wtit LIKE '%" + q3 + "%' AND bno LIKE '%" + q4 + "%') f;"

    curs.execute(sql)
    conn.commit()
    minmax1 = curs.fetchall()
    # conn.close()

    total_t_min0 = minmax1[0][0]  #셋업 min 온도
    total_t_max0 = minmax1[0][1]  #셋업 max 온도
    total_t_min1 = minmax1[0][2]  #실내 min 온도
    total_t_max1 = minmax1[0][3]  #실내 max 온도
    total_s_min2 = minmax1[0][4]  #투입 min 속도
    total_s_max2 = minmax1[0][5]  #투입 max 속도
    total_s_min3 = minmax1[0][6]  #내부 min 속도
    total_s_max3 = minmax1[0][7]  #내부 max 속도
    total_m_min4 = minmax1[0][8]  #수분 min
    total_m_max4 = minmax1[0][9]  #수분 max
    # print("minmax = ", minmax1)   # min, max 출력

    if (q3 == list_3[0] or q3 == list_3[1] or q3 == list_3[2]):  # 장비 온도 3개
        lbl_10_Bottom = Label(BottomFrame1, text=total_cnt1, bg="#FFFFFF", anchor=E, width=10)  # 검색 카운터를 출력
        lbl_10_Bottom.grid(row=0, column=1)

    elif (q3 == list_3[3] or q3 == list_3[4]):  # 수분 측정기값 2개
        lbl_21_Bottom = Label(BottomFrame1, text=total_cnt2, bg="#FFFFFF", anchor=E, width=10)   # 검색 카운터를 출력
        lbl_21_Bottom.grid(row=0, column=1)

    elif (q3 == "" and q4 == ""):  # 값이 없을 경우
        lbl_30_Bottom = Label(BottomFrame1, text=total_cnt0, bg="#FFFFFF", anchor=E, width=10)  # 검색 카운터를 출력
        lbl_30_Bottom.grid(row=0, column=1)

    lbl_11_Bottom = Label(BottomFrame1, text=total_t_min0, bg="#FFFFFF", anchor=E, width=7)  #셋업 min 온도 출력
    lbl_11_Bottom.grid(row=1, column=4, padx=2)
    lbl_12_Bottom = Label(BottomFrame1, text=total_t_max0, bg="#FFFFFF", anchor=E, width=7)  #셋업 max 온도 출력
    lbl_12_Bottom.grid(row=0, column=4, padx=2)
    lbl_13_Bottom = Label(BottomFrame1, text=total_t_min1, bg="#FFFFFF", anchor=E, width=7)  #실내 min 온도 출력
    lbl_13_Bottom.grid(row=1, column=5, padx=2)
    lbl_14_Bottom = Label(BottomFrame1, text=total_t_max1, bg="#FFFFFF", anchor=E, width=7)  #실내 max 온도 출력
    lbl_14_Bottom.grid(row=0, column=5, padx=2)
    lbl_15_Bottom = Label(BottomFrame1, text=total_s_min2, bg="#FFFFFF", anchor=E, width=7)  #투입 min 속도 출력
    lbl_15_Bottom.grid(row=1, column=6, padx=2)
    lbl_16_Bottom = Label(BottomFrame1, text=total_s_max2, bg="#FFFFFF", anchor=E, width=7)  #투입 max 속도 출력
    lbl_16_Bottom.grid(row=0, column=6, padx=2)
    lbl_17_Bottom = Label(BottomFrame1, text=total_s_min3, bg="#FFFFFF", anchor=E, width=7)  #내부 min 속도 출력
    lbl_17_Bottom.grid(row=1, column=7, padx=2)
    lbl_18_Bottom = Label(BottomFrame1, text=total_s_max3, bg="#FFFFFF", anchor=E, width=7)  #내부 max 속도 출력
    lbl_18_Bottom.grid(row=0, column=7, padx=2)
    lbl_22_Bottom = Label(BottomFrame1, text=total_m_min4, bg="#FFFFFF", anchor=E, width=7)  # 수분 min 출력
    lbl_22_Bottom.grid(row=1, column=8, padx=2)
    lbl_23_Bottom = Label(BottomFrame1, text=total_m_max4, bg="#FFFFFF", anchor=E, width=7)  # 수분 max 출력
    lbl_23_Bottom.grid(row=0, column=8, padx=2)
    lbl_40_Bottom = Label(BottomFrame1, text="셋팅온도", bg="#FFFFFF", anchor=E, width=8)
    lbl_40_Bottom.grid(row=2, column=4, padx=6)
    lbl_41_Bottom = Label(BottomFrame1, text="내부온도", bg="#FFFFFF", anchor=E, width=8)
    lbl_41_Bottom.grid(row=2, column=5, padx=6)
    lbl_42_Bottom = Label(BottomFrame1, text="투입속도", bg="#FFFFFF", anchor=E, width=8)
    lbl_42_Bottom.grid(row=2, column=6, padx=6)
    lbl_43_Bottom = Label(BottomFrame1, text="내부속도", bg="#FFFFFF", anchor=E, width=8)
    lbl_43_Bottom.grid(row=2, column=7, padx=6)
    lbl_44_Bottom = Label(BottomFrame1, text="수분값", bg="#FFFFFF", anchor=E, width=8)
    lbl_44_Bottom.grid(row=2, column=8, padx=6)

    ## Count_Function    #다른쪽에서는 변수명을 변경하여 사용할 것

    # 라이트 프레임 온도 표시
    global wtit_10
    global wtit_11
    global wtit_12
    global wtit_13
    global wtit_14
    global wtit_20
    global wtit_21
    global wtit_22
    global wtit_23
    global wtit_24
    global wtit_25
    global wtit_31
    global wtit_32
    global wtit_33
    global wtit_34
    global wtit_35

    ###### 1호기 가동
    conn = pymysql.connect(host=host_ip, port=port_no, user=user_id, password=password_no, db=db_name,
                           charset=charset_no)
    curs = conn.cursor()
    sql = "SELECT id, case stat when '1' then '가동' when '0' then '비가동' else '수분' end as stat, \
          v11, v12, v13, v14, v21  \
          FROM k7dg WHERE wcd='W0001' \
          order by id desc limit 1;"
    curs.execute(sql)
    rows1 = curs.fetchall()
    conn.commit()
    # print(rows1)

    wtit_10 = rows1[0][1]
    wtit_11 = round(rows1[0][2])
    wtit_12 = round(rows1[0][3])
    wtit_13 = format(round(rows1[0][4]), ',d')
    wtit_14 = rows1[0][5]
    if rows1[0][5] is not None:
        wtit_14 = round(rows1[0][5])
    else:
        wtit_14 = '0'

    if wtit_10 == '가동':
        textEntry1_rightframe1 = Label(RightFrame1, text=wtit_10, width=6, font=('arial', 25, 'bold'), fg="green", anchor='center',
                                       bg="white").grid(row=0, column=0, pady=10)
    else:
        textEntry1_rightframe1 = Label(RightFrame1, text=wtit_10, width=6, font=('arial', 25, 'bold'), fg="red",
                                       bg="white").grid(row=0, column=0, pady=10)
    textEntry2_rightframe1 = Label(RightFrame1, text=wtit_11, width=6, font=('arial', 35, 'bold'), fg="black",
                                   bg="white").grid(row=2, column=0, pady=5)
    textEntry3_rightframe1 = Label(RightFrame1, text=wtit_12, width=6, font=('arial', 35, 'bold'), fg="black",
                                   bg="white").grid(row=4, column=0, pady=5)
    textEntry4_rightframe1 = Label(RightFrame1, text=wtit_13, width=6, font=('arial', 35, 'bold'), fg="black",
                                   bg="white").grid(row=6, column=0, pady=5)
    textEntry5_rightframe1 = Label(RightFrame1, text=wtit_14, width=6, font=('arial', 35, 'bold'), fg="black",
                                   bg="white").grid(row=8, column=0, pady=5)

    ###### 2호기 가동
    conn = pymysql.connect(host=host_ip, port=port_no, user=user_id, password=password_no, db=db_name,
                           charset=charset_no)
    curs = conn.cursor()
    sql = "SELECT id, case stat when '1' then '가동' when '0' then '비가동' else '수분' end as stat, \
          v11, v12, v13, v14, v21 \
          FROM k7dg WHERE wcd='W0002' \
          order by id desc limit 1;"
    curs.execute(sql)
    rows2 = curs.fetchall()
    conn.commit()
    # print(rows2)

    wtit_21 = rows2[0][1]
    wtit_22 = round(rows2[0][2])
    wtit_23 = round(rows2[0][3])
    wtit_24 = format(round(rows2[0][4]), ',d')
    wtit_25 = rows2[0][5]
    if rows2[0][5] is not None:
        wtit_25 = round(rows2[0][5])
    else:
        wtit_25 = '0'

    if wtit_21 == '가동':
        textEntry1_rightframe2 = Label(RightFrame2, text=wtit_21, width=6, font=('arial', 25, 'bold'), fg="green",
                                       bg="white").grid(row=0, column=0, pady=10)
    else:
        textEntry1_rightframe2 = Label(RightFrame2, text=wtit_21, width=6, font=('arial', 25, 'bold'), fg="red",
                                       bg="white").grid(row=0, column=0, pady=10)
    textEntry2_rightframe2 = Label(RightFrame2, text=wtit_22, width=6, font=('arial', 35, 'bold'), fg="black",
                                   bg="white").grid(row=2, column=0, pady=5)
    textEntry3_rightframe2 = Label(RightFrame2, text=wtit_23, width=6, font=('arial', 35, 'bold'), fg="black",
                                   bg="white").grid(row=4, column=0, pady=5)
    textEntry4_rightframe2 = Label(RightFrame2, text=wtit_24, width=6, font=('arial', 35, 'bold'), fg="black",
                                   bg="white").grid(row=6, column=0, pady=5)
    textEntry5_rightframe2 = Label(RightFrame2, text=wtit_25, width=6, font=('arial', 35, 'bold'), fg="black",
                                   bg="white").grid(row=8, column=0, pady=5)

    ###### 3호기 가동
    conn = pymysql.connect(host=host_ip, port=port_no, user=user_id, password=password_no, db=db_name, charset=charset_no)
    curs = conn.cursor()

    sql = "SELECT id, case stat when '1' then '가동' when '0' then '비가동' else '수분' end as stat, \
          v11, v12, v13, v14, v21 FROM k7dg \
          WHERE wcd='W0003' \
          order by id desc limit 1;"
    curs.execute(sql)
    rows3 = curs.fetchall()
    conn.commit()
    conn.close()
    # print(rows3)

    wtit_31 = (rows3[0][1])
    wtit_32 = round(rows3[0][2])
    wtit_33 = round(rows3[0][3])
    wtit_34 = format(round(rows3[0][4]),',d')
    wtit_35 = rows3[0][5]
    if rows3[0][5] is not None:
        wtit_35 = round(rows3[0][5])
    else:
        wtit_35 = '0'

    if wtit_31 == '가동':
        textEntry1_rightframe3 = Label(RightFrame3, text=wtit_31, width=6, font=('arial', 25, 'bold'), fg="green",
                                   bg="white").grid(row=0, column=0, pady=10)
    else:
        textEntry1_rightframe3 = Label(RightFrame3, text=wtit_31, width=6, font=('arial', 25, 'bold'), fg="red",
                                       bg="white").grid(row=0, column=0, pady=10)
    textEntry2_rightframe3 = Label(RightFrame3, text=wtit_32, width=6, font=('arial', 35, 'bold'), fg="black",
                                   bg="white").grid(row=2, column=0, pady=5)
    textEntry3_rightframe3 = Label(RightFrame3, text=wtit_33, width=6, font=('arial', 35, 'bold'), fg="black",
                                   bg="white").grid(row=4, column=0, pady=5)
    textEntry4_rightframe3 = Label(RightFrame3, text=wtit_34, width=6, font=('arial', 35, 'bold'), fg="black",
                                   bg="white").grid(row=6, column=0, pady=5)
    textEntry5_rightframe3 = Label(RightFrame3, text=wtit_35, width=6, font=('arial', 35, 'bold'), fg="black",
                                   bg="white").grid(row=8, column=0, pady=5)


# ===화면 처음 열면 테이블에 있는 Data 가져오기===============================================================================

def update(rows):
    my_tree.delete(*my_tree.get_children())
    for i in rows:
        my_tree.insert('', 'end', values=i)
        # btnSelect
        # print(i)
        # print(rows)


# ===윈도우 화면 나가기====================================================================================================

def btnExit():
    root.quit()

# ==Frame================================================================================================================
root.grid_rowconfigure(1, weight=1)         #세로 확대 자동
root.grid_columnconfigure(0, weight=1)      #가로 확대 자동
root.grid_rowconfigure(1, weight=1)         #세로 확대 자동
root.grid_columnconfigure(1, weight=1)      #가로 확대 자동
root.grid_rowconfigure(1, weight=1)         #세로 확대 자동
root.grid_columnconfigure(2, weight=1)      #가로 확대 자동
root.grid_rowconfigure(1, weight=1)         #세로 확대 자동
root.grid_columnconfigure(3, weight=1)      #가로 확대 자동
root.grid_rowconfigure(2, weight=1)         #세로 확대 자동
root.grid_columnconfigure(0, weight=1)      #가로 확대 자동
root.grid_rowconfigure(2, weight=1)         #세로 확대 자동
root.grid_columnconfigure(1, weight=1)      #가로 확대 자동
# root.grid_rowconfigure(2, weight=1)         #세로 확대 자동
# root.grid_columnconfigure(2, weight=1)      #가로 확대 자동

TopFrame = Frame(root, width=1400, height=50, bg="#FFFFFF")
LeftFrame = Frame(root, width=560, height=800, bg="#FFFFFF")
RightFrame1 = LabelFrame(root, text="킬른1호기", width=200, height=800, bg="#FFFFFF", font=('arial', 12, 'bold'))
RightFrame2 = LabelFrame(root, text="킬른2호기", width=200, height=800, bg="#FFFFFF", font=('arial', 12, 'bold'))
RightFrame3 = LabelFrame(root, text="킬른3호기", width=200, height=800, bg="#FFFFFF", font=('arial', 12, 'bold'))
BottomFrame1 = Frame(root, width=560, height=20, bg="#FFFFFF")
BottomFrame2 = Frame(root, width=200, height=20, bg="#FFFFFF")
# BottomFrame3 = Frame(root, width=200, height=20, bg="#FFFFFF")

# ====================================================================================================================
TopFrame.grid(row=0, columnspan=4, sticky="nw")
LeftFrame.grid(row=1, column=0, sticky="nsew")
RightFrame1.grid(row=1, column=1, sticky="nsew")
RightFrame2.grid(row=1, column=2, sticky="nsew")
RightFrame3.grid(row=1, column=3, sticky="nsew")
BottomFrame1.grid(row=2, column=0, sticky="nsew")
BottomFrame2.grid(row=2, column=1, sticky="nsew")
# BottomFrame1.grid(row=2, column=0, columnspan=4, sticky="nsew")
# BottomFrame2.grid(row=2, column=1, columnspan=4, sticky="nsew")
# BottomFrame3.grid(row=2, column=2, columnspan=4, sticky="nw")

# ===TopFrame============================================================================================================

lbl_1 = Label(TopFrame, text="기간", width=5, anchor=E, bg="white")
lbl_1.grid(row=1, column=1, ipadx=20, pady=2)

cal1 = DateEntry(TopFrame, date_pattern='yyyy-mm-dd', dateformat=3, width=11, anchor=CENTER, background='darkblue', foreground='white',
                 Calendar=year_date)
cal1.grid(row=1, column=2, sticky='w', pady=2)
# print("cal1=")
# print(cal1)

lbl_2 = Label(TopFrame, text="~", bg="white").grid(row=1, column=3, padx=2, pady=2)

cal2 = DateEntry(TopFrame, date_pattern='yyyy-mm-dd', dateformat=3, width=11, background='darkblue', foreground='white',
                 borderwidth=4, Calendar=year_date)
cal2.grid(row=1, column=4, sticky='w', pady=2)

lbl_3 = Label(TopFrame, text="장비번호", width=5, anchor=E, bg="white").grid(row=1, column=5, ipadx=10, pady=2)
cmbWno = ttk.Combobox(TopFrame, textvariable=i_cmbWno, value=list_3, width=15)
cmbWno.current(0)  # 설비 리스트 중에 0번째 설비를 초기값으로 list_3 = ["T001", "T002",""]
cmbWno.grid(row=1, column=6, padx=5, pady=2)

lbl_4 = Label(TopFrame, text="품목번호", width=5, anchor=E, bg="white").grid(row=1, column=7, ipadx=10, pady=2)
textEntry = Entry(TopFrame, width=10, textvariable=i_textEntry).grid(row=1, column=8, ipadx=5, pady=2)

btnSelect = Button(TopFrame, text="검색실행", command=btnSelect).grid(row=1, column=9, padx=10, ipadx=10, pady=2)
# btnSelect = Button(TopFrame, text="검색실행", command=btnSelect).grid(row=1, column=9, padx=15, ipadx=20, pady=24)
btnReset = Button(TopFrame, text="조건삭제", command=btnConditionReset).grid(row=1, column=10, padx=10, ipadx=10, pady=2)
lbl_5 = Label(TopFrame, text="타점간격", width=5, anchor=E, bg="white").grid(row=1, column=11, ipadx=5, pady=2)
cmbWno = ttk.Combobox(TopFrame, textvariable=i_cmbWno1, value=list_4, width=10)
cmbWno.current(0)  # 설비 리스트 중에 0번째 설비를 초기값으로 list_4 1번째 값
cmbWno.grid(row=1, column=12, padx=10, pady=2)
btnLinegraph1 = Button(TopFrame, text="온도 그래프", command=btnLinegraph1, bg="yellow").grid(row=1, column=13, padx=10,
                                                                                         ipadx=5, pady=2)
btnLinegraph1 = Button(TopFrame, text="관리도", command=Xbar_chart1, bg="cyan").grid(row=2, column=13, padx=10,
                                                                                         ipadx=20, pady=2)
btnLinegraph2 = Button(TopFrame, text="속도 그래프", command=btnLinegraph2, bg="yellow").grid(row=1, column=14, padx=10,
                                                                                         ipadx=5, pady=2)
btnLinegraph3 = Button(TopFrame, text="수분 그래프", command=btnLinegraph3, bg="yellow").grid(row=1, column=15, padx=10,
                                                                                         ipadx=5, pady=2)
btnClose = Button(TopFrame, text="닫기", command=btnClose).grid(row=1, column=16, padx=10, ipadx=20, pady=2)
# btnClose = Button(TopFrame, text="닫기", command=btnClose and plt.close()).grid(row=1, column=14, padx=15, ipadx=20, pady=24)

# ===RightFrame1-1=========================================================================================================

textEntry1_rightframe1 = Label(RightFrame1, text="준비", width=6, font=('arial', 25, 'bold'), fg="black", anchor=CENTER,
                               bg="white").grid(row=0, column=0, pady=5)

lbl_2_rightframe1 = Label(RightFrame1, text="셋팅온도(℃)", bg="#FFFFFF", anchor="center", font=('arial', 14), fg="red")
lbl_2_rightframe1.grid(row=1, column=0, pady=15)
textEntry2_rightframe1 = Label(RightFrame1, text="0", width=6, font=('arial', 35, 'bold'), fg="black",
                               bg="white").grid(row=2, column=0, pady=5)

lbl_3_rightframe1 = Label(RightFrame1, text="내부온도(℃)", bg="#FFFFFF", anchor="center", font=('arial', 14), fg="red")
lbl_3_rightframe1.grid(row=3, column=0, pady=15)
textEntry3_rightframe1 = Label(RightFrame1, text="0", width=6, font=('arial', 35, 'bold'), fg="black",
                               bg="white").grid(row=4, column=0, pady=5)

lbl_4_rightframe1 = Label(RightFrame1, text="투입속도(RPM)", bg="#FFFFFF", anchor="center", font=('arial', 14))
lbl_4_rightframe1.grid(row=5, column=0, pady=15)
textEntry4_rightframe1 = Label(RightFrame1, text="0", width=6, font=('arial', 35, 'bold'), fg="black",
                               bg="white").grid(row=6, column=0, pady=5)

lbl_5_rightframe1 = Label(RightFrame1, text="내부속도(RPM)", bg="#FFFFFF", anchor="center", font=('arial', 14))
lbl_5_rightframe1.grid(row=7, column=0, pady=15)
textEntry5_rightframe1 = Label(RightFrame1, text="0", width=6, font=('arial', 35, 'bold'), fg="black",
                               bg="white").grid(row=8, column=0, pady=5)

# lbl_6_rightframe1 = Label(RightFrame1)
# lbl_6_rightframe1.grid(row=9, column=0, pady=10)

# ===RightFrame1-2=========================================================================================================

# lbl_1_rightframe2 = Label(RightFrame2)
# lbl_1_rightframe2.grid(row=0, column=0, pady=10)

textEntry1_rightframe2 = Label(RightFrame2, text="준비", width=6, font=('arial', 25, 'bold'), fg="black",
                               bg="white").grid(row=0, column=0, pady=5)
lbl_1_rightframe2 = Label(RightFrame2, text="셋팅온도(℃)", bg="#FFFFFF", anchor="center", font=('arial', 14), fg="red")
lbl_1_rightframe2.grid(row=1, column=0, pady=15)
textEntry1_rightframe2 = Label(RightFrame2, text="0", width=6, font=('arial', 35, 'bold'), fg="black",
                               bg="white").grid(row=2, column=0, pady=5)

lbl_2_rightframe2 = Label(RightFrame2, text="내부온도(℃)", bg="#FFFFFF", anchor="center", font=('arial', 14), fg="red")
lbl_2_rightframe2.grid(row=3, column=0, pady=15)
textEntry2_rightframe2 = Label(RightFrame2, text="0", width=6, font=('arial', 35, 'bold'), fg="black",
                               bg="white").grid(row=4, column=0, pady=5)

lbl_3_rightframe2 = Label(RightFrame2, text="투입속도(RPM)", bg="#FFFFFF", anchor="center", font=('arial', 14))
lbl_3_rightframe2.grid(row=5, column=0, pady=15)
textEntry3_rightframe2 = Label(RightFrame2, text="0", width=6, font=('arial', 35, 'bold'), fg="black",
                               bg="white").grid(row=6, column=0, pady=5)

lbl_4_rightframe2 = Label(RightFrame2, text="내부속도(RPM)", bg="#FFFFFF", anchor="center", font=('arial', 14))
lbl_4_rightframe2.grid(row=7, column=0, pady=15)
textEntry4_rightframe2 = Label(RightFrame2, text="0", width=6, font=('arial', 35, 'bold'), fg="black",
                               bg="white").grid(row=8, column=0, pady=5)

# lbl_1_rightframe2 = Label(RightFrame2)
# lbl_1_rightframe2.grid(row=9, column=0, pady=10)

# ===RightFrame1-3=========================================================================================================
lbl_2_rightframe3 = Label(RightFrame3, text="준비", bg="#FFFFFF", anchor="center", font=('arial', 25,'bold'), fg="black")
lbl_2_rightframe3.grid(row=0, column=0, pady=15)

lbl_3_rightframe3 = Label(RightFrame3, text="셋팅온도(℃)", bg="#FFFFFF", anchor="center", font=('arial', 14), fg="red")
lbl_3_rightframe3.grid(row=1, column=0, pady=15)
textEntry1_rightframe3 = Label(RightFrame3, text="0", width=6, font=('arial', 35, 'bold'), fg="black",
                               bg="white").grid(row=2, column=0, pady=5)

lbl_4_rightframe3 = Label(RightFrame3, text="내부온도(℃)", bg="#FFFFFF", anchor="center", font=('arial', 14), fg="red")
lbl_4_rightframe3.grid(row=3, column=0, pady=15)
textEntry2_rightframe3 = Label(RightFrame3, text="0", width=6, font=('arial', 35, 'bold'), fg="black",
                               bg="white").grid(row=4, column=0, pady=5)

lbl_5_rightframe3 = Label(RightFrame3, text="투입속도(RPM)", bg="#FFFFFF", anchor="center", font=('arial', 14))
lbl_5_rightframe3.grid(row=5, column=0, pady=15)
textEntry3_rightframe3 = Label(RightFrame3, text="0", width=6, font=('arial', 35, 'bold'), fg="black",
                               bg="white").grid(row=6, column=0, pady=5)

lbl_6_rightframe3 = Label(RightFrame3, text="내부속도(RPM)", bg="#FFFFFF", anchor="center", font=('arial', 14))
lbl_6_rightframe3.grid(row=7, column=0, pady=15)
textEntry4_rightframe3 = Label(RightFrame3, text="0", width=6, font=('arial', 35, 'bold'), fg="black",
                               bg="white").grid(row=8, column=0, pady=5)

# lbl_7_rightframe3 = Label(RightFrame3)
# lbl_7_rightframe3.grid(row=9, column=0, pady=10)

# #===BottomFrame=========================================================================================================

lbl_1_Bottom = Label(BottomFrame1, text="검색건수 :", bg="#FFFFFF", anchor=E, width=20)
lbl_1_Bottom.grid(row=0, column=0, padx=5)
lbl_2_Bottom = Label(BottomFrame1, text="", bg="#FFFFFF", anchor=W, width=15)
lbl_2_Bottom.grid(row=0, column=2, padx=50)
lbl_4_Bottom = Label(BottomFrame1, text="", bg="#FFFFFF", anchor=W, width=15)
lbl_4_Bottom.grid(row=1, column=2, padx=50)
lbl_3_Bottom = Label(BottomFrame1, text="최대값(Max) :", bg="#FFFFFF", anchor=E, width=15)
lbl_3_Bottom.grid(row=0, column=3, padx=6)
lbl_5_Bottom = Label(BottomFrame1, text="최소값(Mmin) :", bg="#FFFFFF", anchor=E, width=15)
lbl_5_Bottom.grid(row=1, column=3, padx=6)
lbl_40_Bottom = Label(BottomFrame1, text="셋팅온도", bg="#FFFFFF", anchor=E, width=8)
lbl_40_Bottom.grid(row=2, column=4, padx=6)
lbl_41_Bottom = Label(BottomFrame1, text="내부온도", bg="#FFFFFF", anchor=E, width=8)
lbl_41_Bottom.grid(row=2, column=5, padx=6)
lbl_42_Bottom = Label(BottomFrame1, text="투입속도", bg="#FFFFFF", anchor=E, width=7)
lbl_42_Bottom.grid(row=2, column=6, padx=2)
lbl_43_Bottom = Label(BottomFrame1, text="내부속도", bg="#FFFFFF", anchor=E, width=7)
lbl_43_Bottom.grid(row=2, column=7, padx=2)
lbl_44_Bottom = Label(BottomFrame1, text="수분값", bg="#FFFFFF", anchor=E, width=5)
lbl_44_Bottom.grid(row=2, column=8, padx=2)



# print("========")
# print(total_cnt0)
# lbl_2_Bottom = Label(BottomFrame1, bg="#FFFFFF", anchor=W, width=10, textvariable=total_cnt0)
# lbl_2_Bottom.grid(row=0, column=1)

# lbl_2_Bottom = Label(BottomFrame1, text="9999", bg="#FFFFFF", anchor=W, width=10, textvariable=total_cnt)
# lbl_2_Bottom.grid(row=0, column=1)

# lbl_3_Bottom = Label(BottomFrame2, text=company_name, bg="#FFFFFF", anchor=E)
# lbl_3_Bottom.pack()

# lbl_4_Bottom = Label(BottomFrame1, text="Copyright © KOVIS All Rights Reserved.", bg="#FFFFFF")
# lbl_4_Bottom.pack(row=0, column=2,  pady=5)

# lbl_5_Bottom = Label(BottomFrame2, text="서울서 양천구 목동서로 77, 1024호", bg="#FFFFFF")
# lbl_5_Bottom.pack(row=2, column=2, pady=5)

# ===kdemo 서버 들어가기 ==================================================================================================

# conn = pymysql.connect(host=host_ip, port=port_no, user=user_id, password=password_no, db=db_name, charset=charset_no)
# curs = conn.cursor()
# # wr_plc 테이블에서 id, itime, wno, v21, v22, v23 컬럼 100만 가져오기
# sql = "SELECT a.id, a.itime, case a.stat when '1' then '가동' when '0' then '비가동' else '수분' end as stat, \
#       b.wtit, d.bno, d.btit, a.v11, a.v12, a.v13, a.v14, a.v21 \
#        FROM k7dg a \
#        left join aw b on a.wcd = b.wcd \
#        left join wo c on a.lno = c.oid \
#        left join ab d on c.bcd = d.bcd\
#        order by a.id desc \
#       limit 50"
#
# curs.execute(sql)
# rows = curs.fetchall()
# print(rows)
# print(len(rows))
# conn.commit()
# conn.close()

# #===트리뷰 프레임 전체=====================================================================================================
# 스타일 추가
style = ttk.Style()
# Pick A Theme
style.theme_use('default')
# 트리뷰 색상 속성 정의
style.configure("Treeview", background="#FFFFFF", foreground="black", rowheight=20, fieldbackground="white")  # D3D3D3"
# 트리뷰 ROW 선택 시 색상 변경
style.map("Treeview", background=[('selected', "#347083")])

# 트리뷰 프레임 정의
tree_frame = Frame(LeftFrame)
# tree_frame.pack(pady=2, padx=10)  # 자동 비율 조정시 fill/expand 입력
tree_frame.pack(fill='both', expand=1, pady=2, padx=10)  # 자동 비율 조정시 fill/expand 입력

# 트리뷰 프레임 스크롤바 정의
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# 트리뷰 정의 height="30"은 row의 개수
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended", height="32")
# my_tree.pack()   # 자동 비율 조정시 fill/expand 입력
my_tree.pack(fill=BOTH, expand=1)   # 자동 비율 조정시 fill/expand 입력
# 스크롤바 속성
tree_scroll.config(command=my_tree.yview)
# 트리뷰 더블클릭시 서브화면에 사원정보 나타나게 하기
# 컬럼정의
my_tree['columns'] = ("id", "itime", "stat", "wtit", "bno", "btit", "v11", "v12", "v13", "v14", "v21", "LOT_NO")
# 트리뷰 컬럼 포멧("#0", width=0, stretch=NO를 설정하면 화면에 빈 값이 없음)
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("id", anchor=CENTER, width=70, stretch=True)
my_tree.column("itime", anchor=CENTER, width=140, stretch=True)
my_tree.column("stat", anchor=CENTER, width=70, stretch=True)
my_tree.column("wtit", anchor=CENTER, width=110, stretch=True)
my_tree.column("bno", anchor=CENTER, width=80, stretch=True)
my_tree.column("btit", anchor=CENTER, width=100, stretch=True)
my_tree.column("v11", anchor=CENTER, width=70, stretch=True)
my_tree.column("v12", anchor=CENTER, width=70, stretch=True)
my_tree.column("v13", anchor=CENTER, width=70, stretch=True)
my_tree.column("v14", anchor=CENTER, width=70, stretch=True)
my_tree.column("v21", anchor=CENTER, width=70, stretch=True)
my_tree.column("LOT_NO", anchor=CENTER, width=100, stretch=True)
# 컬럼 머리말로 "wno"을 TEXT="장비번호"는 제목으로 표기
my_tree.heading("id", text="일련번호", anchor=CENTER)
my_tree.heading("itime", text="날짜", anchor=CENTER)
my_tree.heading("stat", text="상태", anchor=CENTER)
my_tree.heading("wtit", text="설비명", anchor=CENTER)
my_tree.heading("bno", text="품목번호", anchor=CENTER)
my_tree.heading("btit", text="품목명", anchor=CENTER)
my_tree.heading("v11", text="셋팅온도", anchor=CENTER)
my_tree.heading("v12", text="내부온도", anchor=CENTER)
my_tree.heading("v13", text="투입속도", anchor=CENTER)
my_tree.heading("v14", text="건조속도", anchor=CENTER)
my_tree.heading("v21", text="수분", anchor=CENTER)
my_tree.heading("LOT_NO", text="LOT", anchor=CENTER)
# Create Striped 줄무늬 Row Tags 특이한, 예상밖
my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")


root.mainloop()