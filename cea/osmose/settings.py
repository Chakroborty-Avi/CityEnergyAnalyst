
# import from config # TODO: add to config

## GENERAL ##
T_b_CDD = 25.0
# TECHS = ['HCS_LD', 'HCS_coil', 'HCS_ER0', 'HCS_3for2', 'HCS_IEHX']
# TECHS = ['HCS_base_LD', 'HCS_base_coil', 'HCS_base_3for2', 'HCS_base_ER0', 'HCS_base_IEHX',  'HCS_base']
TECHS = ['HCS_base_hps']
# timesteps = [5136, 5144, 5145, 5147, 5148]  # 168 (week) [5389]
# timesteps = [5145]  # 168 (week) [5389]
# timesteps = 24  # 168 (week) [5389]
# timesteps = "typical days"  # 168 (week)
timesteps = 'dtw hours'
typical_days_path = "E:\\WP2"
PLOTS = ['electricity_usages','air_flow','OAU_T_w_supply','exergy_usages', 'humidity_balance', 'humidity_storage', 'heat_balance']
new_calculation = False

# GENERAL INPUTS
season = 'Summer'
specified_buildings = ["B005"]
# specified_buildings = ["B001","B002","B005","B006","B009"]
# specified_buildings = ["B003","B008"]
# specified_buildings = ["B001","B002","B003","B004","B005","B006","B007","B008","B009","B010"]
# cases = ['WTP_CBD_m_WP1_RET','WTP_CBD_m_WP1_HOT','WTP_CBD_m_WP1_OFF']
cases = ['WTP_CBD_m_WP1_HOT']

## LAPTOP ##
ampl_lic_path = "C:\\Users\\Shanshan\\Desktop\\ampl"

# Branch mk
# osmose_project_path = "E:\\OSMOSE_projects\\HCS_mk\\Projects"
osmose_project_path = "E:\\ipese_new\\osmose_mk\\Projects"
osmose_outMsg_path = "\\s_001\\opt\\hc_outmsg.txt"

# Branch master
# osmose_project_path = "E:\\OSMOSE_projects\\HCS\\Projects"
# osmose_outMsg_path = "\\scenario_1\\tmp\\OutMsg.txt"

osmose_project_data_path = osmose_project_path + '\\data'
result_destination = "E:\\HCS_results_1015"

## WORK STATION ##
# ampl_lic_path = "C:\\Users\\Zhongming\\Desktop\\SH\\ampl"
# osmose_project_path = "C:\\Users\\Zhongming\\Documents\\HCS\\Projects"
# result_destination = "D:\\SH\\test_0805"


# == HKG Summer ==
# season = 'Summer'
# cases = ['HKG_CBD_m_WP1_OFF', 'HKG_CBD_m_WP1_HOT', 'HKG_CBD_m_WP1_RET']
# specified_buildings = ["B001","B002","B003","B004","B005","B006","B007","B008","B009","B010"]
# osmose_project_path = "C:\\Users\\Zhongming\\Documents\\HCS\\Projects"
# result_destination = "D:\\SH\\Google Drive\\WP2\\HKG_Summer"
# ==============================================================================================

# == HKG Spring ==
# season = 'Spring'
# cases = ['HKG_CBD_m_WP1_OFF', 'HKG_CBD_m_WP1_HOT', 'HKG_CBD_m_WP1_RET']
# specified_buildings = ["B001","B002","B003","B004","B005","B006","B007","B008","B009","B010"]
# osmose_project_path = "C:\\Users\\Zhongming\\Documents\\HCS\\Projects"
# result_destination = "D:\\SH\\Google Drive\\WP2\\HKG_Spring"
# ==============================================================================================

# == HKG Autumn ==
# season = 'Autumn'
# cases = ['HKG_CBD_m_WP1_OFF', 'HKG_CBD_m_WP1_HOT', 'HKG_CBD_m_WP1_RET']
# specified_buildings = ["B001","B002","B003","B004","B005","B006","B007","B008","B009","B010"]
# osmose_project_path = "C:\\Users\\Zhongming\\Documents\\HCS\\Projects"
# result_destination = "D:\\SH\\Google Drive\\WP2\\HKG_Autumn"
# ==============================================================================================

# == ABU Summer ==
# season = 'Summer'
# cases = ['ABU_CBD_m_WP1_OFF','ABU_CBD_m_WP1_HOT','ABU_CBD_m_WP1_RET']
# specified_buildings = ["B001","B002","B003","B004","B005","B006","B007","B008","B009","B010"]
# osmose_project_path = "C:\\Users\\Zhongming\\Documents\\HCS\\Projects"
# result_destination = "D:\\SH\\Google Drive\\WP2\\ABU_Summer"
# ==============================================================================================

# == ABU Spring ==
# season = 'Spring'
# cases = ['ABU_CBD_m_WP1_OFF','ABU_CBD_m_WP1_HOT','ABU_CBD_m_WP1_RET']
# specified_buildings = ["B001","B002","B003","B004","B005","B006","B007","B008","B009","B010"]
# osmose_project_path = "C:\\Users\\Zhongming\\Documents\\HCS\\Projects"
# result_destination = "D:\\SH\\Google Drive\\WP2\\ABU_Spring"
# ==============================================================================================

# == ABU Autumn ==
# season = 'Autumn'
# cases = ['ABU_CBD_m_WP1_HOT']
# specified_buildings = ["B006","B002"]
# # cases = ['ABU_CBD_m_WP1_OFF','ABU_CBD_m_WP1_HOT','ABU_CBD_m_WP1_RET']
# # specified_buildings = ["B001","B002","B003","B004","B005","B006","B007","B008","B009","B010"]
# osmose_project_path = "C:\\Users\\Zhongming\\Documents\\HCS\\Projects"
# result_destination = "D:\\SH\\WP2\\ABU_Autumn"
# ==============================================================================================



