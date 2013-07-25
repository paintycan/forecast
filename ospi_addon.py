#!/usr/bin/python
import ospi

 ### Import fc_addon.py file ###
import fc_addon

 ### Add fc_addon urls ###
ospi.urls.extend(['/mfc', 'fc_addon.modify_forecastRule', '/cfc', 'fc_addon.change_forecastRule', '/vfc', 'fc_addon.view_forecastRules'])
ospi.urls.extend(['/dfc', 'fc_addon.delete_forecastRules', '/fcs', 'fc_addon.view_forecastSettings', '/cfcs', 'fc_addon.change_forecastSettings'])
