# ¬ : Negative
# Λ : Conjunction
# V : Disjunction
# → : Conditional
# ↔ : biconditional
import numpy as np
import codecs
import pandas as pd

class stack():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    

List_operator=('¬','Λ','V','→','↔')

def ReadFileInput(FileInput):
    List_Expression=''
    
    with open(FileInput,'r',encoding='UTF-8') as fr:
        reader=fr.read()
        List_Expression=reader[1:]
    
    return List_Expression

def Negative(a):
    return np.logical_not(a)

def Conjunction(a,b):
    return np.logical_and(a,b)

def Disjunction(a,b):
    return np.logical_or(a,b)

def Conditional(a,b):
    return np.logical_or(np.logical_not(a),b)

def biconditional(a,b):
    return np.logical_or(np.logical_and(a,b),np.logical_not(np.logical_or(a,b)))

def cal(oparetor,a):
    if oparetor=='¬':
        return Negative(a[0])
    elif oparetor == 'Λ' :
        return Conjunction(a[0],a[1])
    elif oparetor == 'V' :
        return Disjunction(a[0],a[1])
    elif oparetor == '→' :
        return Conditional(a[0],a[1])
    elif oparetor == '↔' :
        return biconditional(a[0],a[1])


def calExpression(Expression):
    list_variable_appeared=list()
    Truth_Table_Variable=list()

    for l in Expression:
        if (l.isalpha() and l!='V')and l!='Λ':
            if (l not in list_variable_appeared):
                list_variable_appeared.append(l)
    
    for len_iter in range(len(list_variable_appeared)):
        Cur_array=list()
        lenpack=2**len_iter
        active_node=True
        for p in range(2**len(list_variable_appeared)):
            for i in range(lenpack):
                Cur_array.append(active_node)
            active_node=not active_node
            if len(Cur_array)>=2**len(list_variable_appeared):
                break
        
        Truth_Table_Variable.append(Cur_array)

    Truth_Table_Variable=np.array(Truth_Table_Variable)

    temp_exp=list()
    temp_oper=''
    Stack_exp=list()
    for l in Expression:
        if l in list_variable_appeared:
            if temp_oper=='':
                temp_exp.append(Truth_Table_Variable[list_variable_appeared.index(l)])
            else :
                temp_exp.append(Truth_Table_Variable[list_variable_appeared.index(l)])
                temp_exp[0]=cal(temp_oper,temp_exp)
                if len(temp_exp)>=2 :
                    temp_exp.pop()
                temp_oper=''
        elif l in List_operator:
            temp_oper=l
        elif l=='(':
            if temp_oper!='':
                cur_exp=np.copy(temp_exp)
                cur_oper=np.copy(temp_oper)
                tmp_stack=stack(cur_exp,cur_oper)
                Stack_exp.append(tmp_stack)
                temp_exp.clear()
                temp_oper=''
        elif l==')':
            if len(temp_exp)!=0:
                prev_exp=Stack_exp[-1].x
                prev_oper=Stack_exp[-1].y
                if prev_exp.size!=0:
                    cur_cal=(prev_exp[0],temp_exp[0])
                else:
                    cur_cal=temp_exp
                temp_exp[0]=cal(prev_oper,cur_cal)
                Stack_exp.pop()
        

    DataWriter={}
    for i in range(len(Truth_Table_Variable)):
        DataWriter.update({list_variable_appeared[i] : Truth_Table_Variable[i]})
    DataWriter.update({Expression:temp_exp[0]})
    df=pd.DataFrame(DataWriter)
    df.to_excel('result.xlsx',sheet_name='sheet 1')
    
    return 0
if __name__ == "__main__":
    exp=ReadFileInput('input.txt')
    calExpression(exp)






        





    
