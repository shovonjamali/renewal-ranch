import pandas as pd

def into_numeric(df):
    '''Accepts a dataframe as input, convert columns into numeric,
    and returns the updated dataframe'''
    for col in  df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df
    


############ Data Preparation ###############
def data_prep(input_f, input_m, constant_f, constant_a, constant_o):
    ############### Preparing the input feed and manure information ###################
    input_f = input_f.T
    input_f.columns = input_f.iloc[0,:]
    input_f= input_f[1:]
    input_f = input_f.rename_axis('Animal Category').reset_index()
    input_f = into_numeric(input_f)
    
    input_m = input_m.T
    input_m.columns = input_m.iloc[0,:]
    input_m= input_m[1:]
    input_m = input_m.rename_axis('Animal Category').reset_index()
    input_m = into_numeric(input_m)
    
    farm_info = pd.merge(input_f, input_m, on='Animal Category')
    
    ############### Preparing the constants related to feed, animal categories and other information ###################
    constant_f =constant_f.T
    constant_f.columns = constant_f.iloc[0,:]
    constant_f= constant_f[1:]
    
    constant_a = constant_a.T
    constant_a.columns = constant_a.iloc[0,:]
    constant_a= constant_a[1:]
    
    constant_o = constant_o.T
    constant_o.columns = constant_o.iloc[0]
    constant_o = constant_o.drop('Unnamed: 0')

    return input_f, input_m, constant_f, constant_a, constant_o


def emission_calc(input_f, input_m, constant_f, constant_a, constant_o):
    '''Accepts the farm information and constants as input and 
    return the total emission and cost'''
    
    input_feed, input_manure, constant_feed, constant_animal, constant_other=data_prep(input_f, input_m, constant_f, constant_a, constant_o)

    emission_cal = pd.DataFrame(input_feed['Animal Category'])
    cost_cal = pd.DataFrame(input_feed['Animal Category'])
    cost_cal['Original Cost'] = (input_feed.iloc[:,4:]*list(constant_feed.loc['Feed Cost'])).sum(axis=1)
    ######################## Enteric CH4 estimation
    GE = (input_feed.iloc[:,4:]*list(constant_feed.loc['GE'])).sum(axis=1)/239
    DE = (input_feed.iloc[:,4:]*list(constant_feed.loc['DE'])).sum(axis=1)/239
    DE_perc = DE/GE*100
    Ym = -0.0038 *DE_perc*DE_perc + 0.3501 *DE_perc - 0.811
    emission_cal['Enteric EF'] = ((GE* (Ym/100)*365)/55.65).to_frame()
    emission_cal['CH4-Enteric (t/An)'] = input_feed['Animal Numbers']* emission_cal['Enteric EF']/1000
    ###################### Nex. eqn 10.31-10.33
    perc_ratio = input_feed.iloc[:,4:].div(list(constant_animal.loc['%ratio']),axis='index')
    emission_cal['N Intake'] = (GE/18.45)*(perc_ratio*list(constant_feed.loc['PB From SU'])).sum(axis=1)/6.25
    emission_cal['N Retention'] = ((26*(constant_animal.loc['milk_pr_perc']/6.38)*0.01) + (((268-((7.03*constant_animal.loc['NEg'])/constant_animal.loc['WG']))/1000)*constant_animal.loc['WG'])/6.25).tolist()
    emission_cal['Nex'] = (emission_cal['N Intake'] - emission_cal['N Retention'])*365
    ################## NH3 EMEP/EEA guidelines
    aap = (list(constant_animal.loc['life_days'])*(input_feed['Animal Numbers']/365)).reset_index(drop=True)
    Nex_per_app_an = aap*emission_cal['Nex']
    m_graz_N = Nex_per_app_an*input_manure['X Grazing']
    m_yard_N = Nex_per_app_an*input_manure['X Yard']
    m_hous_N = Nex_per_app_an*input_manure['X House']
    m_graz_TAN =  m_graz_N * constant_other['X TAN'] #total ammoniacal nitrogen (TAN)
    m_yard_TAN =  m_yard_N * constant_other['X TAN'] 
    m_hous_TAN =  m_hous_N * constant_other['X TAN']
    m_hous_namol_TAN =  m_hous_TAN * constant_other['X namol']
    m_hous_namol_N = m_hous_N * constant_other['X namol']
    m_hous_solid_TAN = (1-constant_other['X namol']) * m_hous_TAN
    m_hous_solid_N = (1-constant_other['X namol'])* m_hous_N
    E_hous_namol = m_hous_namol_TAN * constant_other['EF hous namol']
    E_hous_solid = m_hous_solid_TAN * constant_other['EF hous solid']
    E_yard = m_yard_TAN * constant_other['EF yard']
    E_graz = m_graz_TAN * constant_other['EF graz']
    E_NH3_kg = E_hous_namol + E_hous_solid + E_yard + E_graz
    #emission_cal['E NH3 t'] = E_NH3_kg/1000
    emission_cal['NH3'] = E_NH3_kg
    #################### NO2 manure (Kg)
    emission_cal['NO2'] = constant_animal.loc['NO2_EF'] * aap
    #################### N2O manure (Kg)
    emission_cal['N2O'] = (input_feed['Animal Numbers'] * emission_cal['Nex'] * input_manure['MS Solid'] * constant_other['EF n2o'])*44/28
    #################### CH4 manure
    ue_ge = ((3.3+0.233*constant_animal.loc['PB_perc_din_SU']+0.016*constant_animal.loc['g_wt']-0.00002*pow(constant_animal.loc['g_wt'],2))/239).tolist()
    vs = (GE*(1-DE_perc/100)+ue_ge)*((1-constant_other['ash']/100)/18.45).Value
    inter = ((input_manure['MS Grazing'].reset_index(drop=True)*constant_animal.loc['MCF Graz'].reset_index(drop=True))+(input_manure['MS Daily Spread'].reset_index(drop=True)*constant_animal.loc['MCF Daily Spread'].reset_index(drop=True))+(input_manure['MS Solid'].reset_index(drop=True)*constant_animal.loc['MCF Solid'].reset_index(drop=True))+(input_manure['MS Liquid Slurry'].reset_index(drop=True)*constant_animal.loc['MCF Liquid Slurry'].reset_index(drop=True))+(input_manure['MS Anaerobic Lagoon'].reset_index(drop=True)*constant_animal.loc['MCF Anaerobic Lagoon'].reset_index(drop=True))+(input_manure['MS Pit Storage'].reset_index(drop=True)*constant_animal.loc['MCF Pit Storage'].reset_index(drop=True))+(input_manure['MS Poultry With Bedding'].reset_index(drop=True)*constant_animal.loc['MCF Poultry With Bedding'].reset_index(drop=True))+  (input_manure['MS Poultry Without Bedding'].reset_index(drop=True)*constant_animal.loc['MCF Poultry Without Bedding'].reset_index(drop=True)))
    EF_ch4manure = (vs*365)* (0.67* constant_animal.loc['Bo'].reset_index(drop=True) *inter).tolist()
    emission_cal['CH4-Manure'] = (aap*EF_ch4manure)/1000
    ################### N volatilization
    inter_nvol = (input_manure['MS Solid'].reset_index(drop=True)*constant_animal.loc['FracGas Solid'].reset_index(drop=True))+(input_manure['MS Daily Spread'].reset_index(drop=True)*constant_animal.loc['FracGas Daily Spread'].reset_index(drop=True))+ (input_manure['MS Grazing'].reset_index(drop=True)*constant_animal.loc['FracGas Graz'].reset_index(drop=True)) + (input_manure['MS Liquid Slurry'].reset_index(drop=True)*constant_animal.loc['FracGas Slurry'].reset_index(drop=True)) +(input_manure['MS Anaerobic Lagoon'].reset_index(drop=True)*constant_animal.loc['FracGas Aanaerobic Lagoon'].reset_index(drop=True))+ (input_manure['MS Pit Storage'].reset_index(drop=True)*constant_animal.loc['FracGas Pit Storage'].reset_index(drop=True))+ (input_manure['MS Poultry With Bedding'].reset_index(drop=True)*constant_animal.loc['FracGas Poultry With Bedding'].reset_index(drop=True))+ (input_manure['MS Poultry Without Bedding'].reset_index(drop=True)*constant_animal.loc['MCF Poultry Without Bedding'].reset_index(drop=True))
    nvol =  aap*emission_cal['Nex']*inter_nvol
    emission_cal['Nvol N2O'] = nvol*constant_animal.loc['EF_nvol'].reset_index(drop=True)*44/28
    
    return emission_cal, cost_cal


   
