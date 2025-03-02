import pandas as pd
import numpy as np
from scipy.optimize import minimize
import math

def milk_yield_formula(quantities):
    total_DMI = (constant_feed.loc['DMI'] * quantities).sum()
    FCM4 = float((total_DMI - (4.048 - (0.00387 * lact_cow_wt))) / 0.0584)
    milk_yield = float((FCM4 - (15 * m_fat)) / 0.4)
    return milk_yield

def ech4_objective(x1):
    x= x1[0:]
    GE = sum(x*GE_const)
    DE = sum(x*DE_const)
    DE_perc = DE/GE*100
    Ym = -0.0038 * DE_perc * DE_perc + 0.3501 * DE_perc - 0.811
    EF1 = (GE* (Ym/100)*365)/55.65
    t_cost = sum(x*constant_feed.loc['Feed Cost'])
    
    milk_yield = milk_yield_formula(x)
    
    EF_t = wt_em * EF1 + wt_cost * t_cost + wt_new * milk_yield
    if wt_new > 0.75:
        EF_t = -EF_t
    return EF_t
    
def ech4_constraint_lact(x):
    return sum(x[0:])-total_feed_lact

def ech4_constraint_preg(x):
    return sum(x[0:])-total_feed_heif

def ech4_cons_young(x): 
    return sum(x[0:])-total_feed_young

def optimize(weight_em, weight_cost, weight_new, input_feed, input_manure, constant_f, constant_animal, constant_other, constraints, boundary, emission_cal, cost_cal, lactating_cow_weight, milk_fat):
    
    global GE_const, DE_const, DMI_const, constant_feed, wt_em, wt_cost, wt_new, total_feed_lact, total_feed_heif, total_feed_young, lact_cow_wt, m_fat, min_milk_yield, max_milk_yield
    constant_feed = constant_f
    GE_const = list(constant_feed.loc['GE']/239)
    DE_const =  list(constant_feed.loc['DE']/239)
    DMI_const = list(constant_feed.loc['DMI'])
    wt_em = weight_em/100
    wt_cost = weight_cost/100
    
    # new weight
    wt_new = weight_new/100 #0 #weight_new/100
    lact_cow_wt = lactating_cow_weight
    m_fat = milk_fat

    min_milk_yield = 18
    max_milk_yield = 28

    boundary = boundary.set_index(boundary.columns[0])
    total_feed_lact = boundary.loc['total feed','Lactating cows']
    total_feed_heif = boundary.loc['total feed','Heifers and pregnant cows']
    total_feed_young = boundary.loc['total feed','Youth 3-6 months']


    x1 = np.array(constraints['Lactating cows'])
    x2 = np.array(constraints['Heifers and pregnant cows'])
    x3 = np.array(constraints['Youth 3-6 months ']) 
    ch4_cons_lact =({'type':'ineq', 'fun': ech4_constraint_lact})
    # new constraints
    min_milk_yield_con = {'type': 'ineq', 'fun': lambda quantities: milk_yield_formula(quantities) - min_milk_yield}
    max_milk_yield_con = {'type': 'ineq', 'fun': lambda quantities: max_milk_yield - milk_yield_formula(quantities)}
    # all constraints
    cons = [ch4_cons_lact, min_milk_yield_con, max_milk_yield_con]

    b = (boundary.loc['minimum_feedquantity','Lactating cows'],boundary.loc['maximum_feedquantity','Lactating cows'])
    bnds_lact = (b,b,b,b,b,b,b)
    ###################### ECH4 lactating cows
    lactating = minimize(ech4_objective, x1, method='SLSQP', bounds = bnds_lact, constraints = cons)
    result_lactating = lactating.success
    np.round(lactating.x, 4)
    ######################### ECH4 pregnant cows
    ch4_cons_preg =({'type':'ineq', 'fun': ech4_constraint_preg})
    b2 = (boundary.loc['minimum_feedquantity','Heifers and pregnant cows'],boundary.loc['maximum_feedquantity','Heifers and pregnant cows'])
    bnds_preg = (b2,b2,b2,b2,b2,b2,b2)
    
    pregnant = minimize(ech4_objective, x2, method='SLSQP', bounds = bnds_preg, constraints = ch4_cons_preg )    
    np.round(pregnant.x, 4)
    ######################### ECH4 young cattle
    ch4_cons_young =({'type':'ineq', 'fun': ech4_cons_young})
    b1 = (boundary.loc['minimum_feedquantity','Youth 3-6 months'],boundary.loc['maximum_feedquantity','Youth 3-6 months'])
    bnds_young = (b1,b1,b1,b1,b1,b1,b1)
    young = minimize(ech4_objective, x3, method='SLSQP', bounds = bnds_young, constraints = ch4_cons_young )    
    np.round(young.x, 4)
    
    opt_feed = pd.DataFrame(list(zip(np.round(lactating.x, 4).tolist(), np.round(pregnant.x, 4).tolist(), np.round(young.x, 4).tolist()))).transpose()
    opt_feed.columns = constant_feed.columns.tolist()
    opt_feed.insert(0,'Animal Category',(input_feed['Animal Category']))
    opt_feed.insert(1,'Animal Numbers',(input_feed ['Animal Numbers']))
    opt_feed = round(opt_feed,2)

    num_feed = 2+opt_feed.iloc[:,2:].shape[1]   
    GE = (opt_feed.iloc[:,2:]*list(constant_feed.loc['GE'])).sum(axis=1)/239
    DE = (opt_feed.iloc[:,2:]*list(constant_feed.loc['DE'])).sum(axis=1)/239
    DE_perc = DE/GE*100
    Ym = -0.0038 *DE_perc*DE_perc + 0.3501 *DE_perc - 0.811
    opt_ef = ((GE* (Ym/100)*365)/55.65)
    ############ New output dataframe with optimized feed combination #############
    opt_feed_output = pd.DataFrame(columns=['Animal Category'])
    opt_feed_output['Animal Category']=opt_feed['Animal Category']
    opt_feed_output['CH4-Enteric (t/An)'] = opt_feed['Animal Numbers']* opt_ef/1000
    opt_feed_output['CH4-Reduction (t/An)%'] =  round(((opt_feed_output['CH4-Enteric (t/An)']- emission_cal['CH4-Enteric (t/An)'])/emission_cal['CH4-Enteric (t/An)']*-100),2)
    opt_feed_output['Estimated Cost'] =  (opt_feed.iloc[:,2:]*list(constant_feed.loc['Feed Cost'])).sum(axis=1)
    opt_feed_output['Estimated Net Energy'] =  0.84*DE - .77
    opt_feed_output = round(opt_feed_output,2)

    return opt_feed, opt_feed_output, str(result_lactating)
