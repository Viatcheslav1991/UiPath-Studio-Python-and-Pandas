import pandas as pd
import numpy as np


def sort_edit_sum_dupl_from_excel(adres_data_ex):
    
    """ ДАнная функция принимает  excel файл группирует дублирующиеся строки , удаляет по одной строке из каждой группы дублей ,
    и добавляет в результат сумму оставшихся строк """

    data_ex=pd.read_excel(adres_data_ex)
    """создадим таблицу в которой все строки имеют дубли в таблице data_ex"""

    "найдём все дубли в таблице data_ex "
    dupl_mask=data_ex.duplicated()

    """создадим таблицу все строки  которые имеют дубли  в таблице  data_ex """
    dupl_types_data=data_ex[dupl_mask].drop_duplicates()
    dupl_types_data=dupl_types_data.sort_values(by=list(dupl_types_data.columns),ignore_index=True)

    """добавим столбец индекатор"""
    dupl_types_data["ceck_dupl"]=True

    """ теперь присвоим каждой дублироемой строке свой индикатор в таблице dupl_types_data"""
    dupl_types_data["id_dupl"]=dupl_types_data.index

    """обьедимим таблицы  data_ex  dupl_types_data где ключами будут все столбцы таким обраазом все будлированные строки будут иметь индикатор True"""
    data_ex=data_ex.merge(dupl_types_data,on=list(data_ex.columns),how="left")

    """ отсортируем таблицу пусть дублированные строки будут в начале"""
    data_ex=data_ex.sort_values("id_dupl",ignore_index=True)
    """ у уникальных строк в столбце ceck_dupl есть пропуски заменим их на False"""
    data_ex=data_ex.fillna(value={"ceck_dupl":False})

    uniqe_data_ex=data_ex[data_ex["ceck_dupl"]==False]

    """ Тепрь будем отделять дублированные строки суммировать их добавлять к ним строку с суммой и потом получившиеся дата фреймы собрать в список и передать в метод concat """

    list_for_concat=[]
    def add_itogg(id_dupl):
        """ данная функция находит сумму дублированных строк (можно было ещё пощитать их количество и умножить)"""
        mask1=data_ex["id_dupl"]==id_dupl
        mini_dF_for_sum=data_ex[mask1].copy()
        
        """ УДАЛЯЕМ ПЕРВУЮ ДУБЛИРОВАННУЮ СТРОКУ"""
        mini_dF_for_sum=mini_dF_for_sum.iloc[1:]
        
        """ НАХОДИМ СУММУ ОСТАВШИХСЯ ДУБЛЕЙ """
        df_sum=mini_dF_for_sum.sum(numeric_only=True)
        df_sum=pd.DataFrame(df_sum).T
        df_sum=df_sum.drop(labels=["id_dupl"],axis=1)
        
        """ ДОБАВЛЯЕМ ПОМЕТКУ "ИТОГО" """
        df_sum["itog"]="ИТОГО"
        itog_sum=pd.concat([mini_dF_for_sum,df_sum])

        list_for_concat.append(itog_sum)
        
    
    dupl_types_data["id_dupl"].apply(add_itogg)

    dupl_data_ex=pd.concat(list_for_concat)

    """ обьединим уникальные строки с дублированными"""
    data_ex_end=pd.concat([dupl_data_ex,uniqe_data_ex])
    
    data_ex_end =data_ex_end.drop(labels=["id_dupl","ceck_dupl"],axis=1)
    """Сохраняем новыый адрес для обработанной таблицы"""
    adres_data_ex=adres_data_ex.replace(".xlsx","_Итог.xlsx")
    
    
    data_ex_end.to_excel(adres_data_ex)
 
    return data_ex_end


# adres_data_ex="C:/Users/79026/Desktop/prod/Тестовое задание.xlsx"
# A=sort_edit_sum_dupl_from_excel(adres_data_ex)
# print(A.head(10))