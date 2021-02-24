import math

from pandas import Series, DataFrame
import pandas as pd
import matplotlib.pyplot as plt
import csv


print("--Калькулятор значений для лабораторной 1 по электротехнике--\n")

U0=float(input("Введите напряжение холостого хода: "))
r=float(input("Введите значение r: "))
lab_data = {'Resistance': [r], 'Voltage': [U0], 'Current': [0], 'Power': [0], 'Efficiency': [100], 'Source_res': "-"}
lab_dataframe=pd.DataFrame(lab_data)
#print(lab_dataframe)
Isc = round((U0*1000/r),3)
print("\nТок короткого замыкания Isc = ",  Isc, " мА\n")
mode = bool(int(input("Ручной ввод или через csv? (1/0)")))
if (mode==0) :
    csv_file = open('R_U.csv','r')
    csv_reader = csv.DictReader(csv_file, delimiter=' ')



#print(line["Resistance"], " ", line["Voltage"])
#Заполнение таблицы 1.1 в виде датафрейма
k=2
#for k in range (2,11):
for line in csv_reader:
    if (mode==0):
        R=round(float(line['Resistance']), 3)
        U=round(float(line['Voltage']), 3)
    else:
        print("\n---измерения для строки k = ",  k ," ---\n")
        R=round(float(input("Введите установленное сопротивление нагрузки: ")),3)
        U=round(float(input("Введите измеренное напряжение на нагрузке: ")),3)
    I=round((U/R)*1000 ,3)
    P=round(((U*U)/R)*1000 ,  3)
    ECE = round((R/(r+R)) ,3) *100
    
    #print("Ток в нагрузке: ", "%.3f" % (I)," мА")
    #print("Мощность, рассеиваемая в нагрузке: ", "%.3f" %(P), "мВт")
    #print("КПД: ", "%.3f" % (ECE) ,"")        
    
    lab_dataframe=lab_dataframe.append({'Resistance': R, 'Voltage': U, 'Current': I, 'Power': P, 'Efficiency': ECE, 'Source_res': "-"}, ignore_index=True)
    if (k%2 !=0):
        Uold = lab_dataframe.iloc[k-2]['Voltage']
        Iold = lab_dataframe.iloc[k-2]['Current']
        Source_r=((Uold - U)/(I-Iold))*1000
        lab_dataframe.at[k-2, 'Source_res'] = Source_r
        lab_dataframe.at[k - 1, 'Source_res'] = Source_r
    k+=1

print(lab_dataframe)
r_delta=0
for k in range(1,9):
    r_delta+=lab_dataframe.iloc[k]['Source_res']
r_delta= math.sqrt(r_delta/8)
print("Погрешность расчёта внутреннего сопротивления: ", "%.3f" % (r_delta), " Ом")
#Графики

#P(I),
lab_dataframe.plot(kind="line", x='Current',y ='Power')
axis1 = plt.gca()
axis1.set_xlabel('I, мА')
axis1.set_ylabel('P, Вт')
axis1.legend (["P(I)"])
plt.show()

#n(I)
lab_dataframe.plot(kind="line", x='Current',y ='Efficiency')
axis2 = plt.gca()
axis2.set_xlabel('I, мА')
axis2.set_ylabel('%')
axis2.legend(["КПД"])
plt.show()
#plt.clf()
#P(I), n(I)

#lab_dataframe.plot(kind="line", x='Current',y ='Power', ax = axis2)
#lab_dataframe.plot(kind="line", x='Current',y ='Efficiency', ax = axis2)

plt.plot([Isc, 0],[0, U0], linestyle = '--')
#plt.plot(lab_dataframe['Current'],lab_dataframe['Voltage'])
axis3 = plt.gca()
axis3.scatter(lab_dataframe['Current'],lab_dataframe['Voltage'])
axis3.set_xlabel('I, мА')
axis3.set_ylabel('U, В')
plt.show()

end=input("Это всё?")

