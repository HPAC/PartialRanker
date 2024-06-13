# Partial Ranker
#
# Copyright (C) 2019-2024, Aravind Sankaran
# IRTG-2379: Modern Inverse Problems, RWTH Aachen University, Germany
# HPAC, Umeå University, Sweden
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contributors:
# - Aravind Sankaran

# REQUIREMENTS: pycelonis==1.7.*
# pip install --extra-index-url=https://pypi.celonis.cloud/ pycelonis=="1.7.*"

from pycelonis import get_celonis
from pycelonis.celonis_api.pql.pql import PQLColumn
from pycelonis.celonis_api.pql.pql import PQL

import warnings
warnings.filterwarnings('ignore')

## ENTER YOUR CREDENTIALS
URL = "ENTER_CELONIS_CLOUD_URL"
API_TOKEN = "YOUR_API_TOKEN" 

celonis = get_celonis(
    url=URL,
    api_token = API_TOKEN
)

## GET THE SAP_P2P Data Model
sap_p2p = celonis.datamodels[1]

## GET THE EVENTS DATA
query = PQL()
query += PQLColumn(query='"_CEL_P2P_ACTIVITIES_EN_parquet"."_CASE_KEY"', name="case:concept:name")
query += PQLColumn(query='"_CEL_P2P_ACTIVITIES_EN_parquet"."ACTIVITY_EN"', name="concept:name")
query += PQLColumn(query=' VARIANT ( "_CEL_P2P_ACTIVITIES_EN_parquet"."ACTIVITY_EN" )', name="case:variant")
query += PQLColumn(query='"_CEL_P2P_ACTIVITIES_EN_parquet"."EVENTTIME"', name="timestamp")


df_events = sap_p2p._get_data_frame(query)
df_events.to_csv('data/sap_p2p_events.csv')

## COMPUTE DURATION OF THE VARIANTS AND GET THE DATA
query = PQL()
query += PQLColumn(query='"_CEL_P2P_ACTIVITIES_EN_parquet"."_CASE_KEY"', name="case:concept:name")
query += PQLColumn(query=' VARIANT ( "_CEL_P2P_ACTIVITIES_EN_parquet"."ACTIVITY_EN" )', name="case:variant")
query += PQLColumn(
        f'AVG ('
        f'  CALC_THROUGHPUT ( '
        f'      CASE_START TO CASE_END, '
        f'      REMAP_TIMESTAMPS ( "_CEL_P2P_ACTIVITIES_EN_parquet"."EVENTTIME", MINUTES ) '
        f'  ) '
        f')',
        "duration"
    )

df_duration = sap_p2p._get_data_frame(query)
df_duration.to_csv('data/sap_p2p_cases.csv')
