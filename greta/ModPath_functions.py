#%% ----------------------------------------------------------------------------
# A. Hockin, March 2021
# KWR BO 402045-247
# ZZS verwijdering bodempassage
# AquaPriori - Transport Model
# With Martin Korevaar, Martin vd Schans, Steven Ros
#
# Based on Stuyfzand, P. J. (2020). Predicting organic micropollutant behavior 
#               for 4 public supply well field types, with TRANSATOMIC Lite+
#               (Vol. 2). Nieuwegein, Netherlands.
# ------------------------------------------------------------------------------

#### CHANGE LOG ####
# things which must be checked indicated in comm ents with AH
# specific questions flagged for;
# @MartinvdS // @steven //@martinK
####

#%% ----------------------------------------------------------------------------
# INITIALISATION OF PYTHON e.g. packages, etc.
# ------------------------------------------------------------------------------

# %reset -f #reset all variables for each run, -f 'forces' reset, !! 
# only seems to work in Python command window...

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
# from pandas import read_excel
from pandas import read_csv
from pandas import read_excel
from tqdm import tqdm  # tqdm gives a progress bar for the simultation
# import pyarrow.parquet as pq
import math
from scipy.special import kn as besselk

path = os.getcwd()  # path of working directory

#%% 

#%% 

# ------------------------------------------------------------------------------
# Questions
# ------------------------------------------------------------------------------

# 1. 

# ------------------------------------------------------------------------------
# Phreatic and Semi-Confined Aquifer Functions
# ------------------------------------------------------------------------------
# %%

# ########### Defaults ###########
WELL_SCREEN_DIAMETER = .75  # m
BOREHOLE_DIAMETER = .75  # m -> equal to screen diameter to ignore backfilling
TEMPERATURE = 11  # Celcius
K_HOR_AQUIFER = 10  # m/d
VANI_AQUIFER = 1.  # -
K_HOR_CONFINING = .001  # m/d
VANI_CONFINING = 1.  # -
K_HOR_GRAVELPACK = 100  # m/d
VANI_GRAVELPACK = 1.  # -
K_HOR_CLAYSEAL = .001  # m/d
VANI_CLAYSEAL = 1.  # -

DENSITY_AQUIFER = 2650.  # kg/m3
REMOVAL_FUNCTION = 'omp'

DZ_WELL = 0.5  # preferred height of layer [m]

"""
Parameters
----------
schematisation: string
    'freatic', 'semi-confined', 'riverbankfiltration', 'basinfiltration'
removal_function: string
    'omp' -> get parameters for OMP
    'microbiology' -> get parameters for microbiology
"""


# ########### INPUT PARAMETERS Aquapriori Bodem "Phreatic OMP" ###########
schematisation = 'freatic'
thickness_vadoze_zone = 1.  # m
thickness_shallow_aquifer = 5.  # m
thickness_target_aquifer = 10.  # m
porosity_vadoze_zone = .2  # m3/m3
porosity_shallow_aquifer = .3  # m3/m3
porosity_target_aquifer = .25  # m3/m3
organic_carbon_vadoze_zone = .2  # kg/m3 ??
organic_carbon_shallow_aquifer = .3  # kg/m3 ??
organic_carbon_target_aquifer = .25  # kg/m3 ??
redox_vadoze_zone = 1.  # 1 = (sub)oxic; 2 = anoxic; 3 = deeply anoxic
redox_shallow_aquifer = 2
redox_target_aquifer = 3
well_discharge_m3hour = 20 #m3/h
recharge_rate = .001
recharge_conc = 1.
substance = 'chloridazon'
vertical_resistance_aquitard   # [d], c_V
soil_moisture_content           # [m3/m3], θ


#@basin paramters
length_basin
width_basin
_depth_basin
horizontal_distance_basin_gallery = horizontal distance between basin bank and drainage gallery [m];
porosity_recharge_basin 
groundwater_level_above_saturated_zone = normal maximum rise of watertable above H0 [m];

class HydroChemicalSchematisation():
    """ Converts input parameters of AquaPriori GUI to a complete parameterisation."""

    def __init__(self,
        well_screen_diameter = .75  # m
        BOREHOLE_DIAMETER = .75  # m -> equal to screen diameter to ignore backfilling
        TEMPERATURE = 11  # Celcius
        K_HOR_AQUIFER = 10  # m/d
        VANI_AQUIFER = 1.  # -
        K_HOR_CONFINING = .001  # m/d
        VANI_CONFINING = 1.  # -
        K_HOR_GRAVELPACK = 100  # m/d
        VANI_GRAVELPACK = 1.  # -
        K_HOR_CLAYSEAL = .001  # m/d
        VANI_CLAYSEAL = 1.  # -

        DENSITY_AQUIFER = 2650.  # kg/m3
        REMOVAL_FUNCTION = 'omp'):

recharge = {
    'recharge1': {
        'recharge_rate': 0.001
        'compound': ....
        'concentration': ....
        'x_start': ....
        'x_end': ....
        },
    'recharge2': {
        'recharge_rate': 0.001
        'compound': ....
        'concentration': ....
        'x_start': ....
        'x_end': ....
        },
  
geo_parameters = {
    'geolayer1': {
        'vadoze': True  # not part of modflow
        'top': 0,  # flow parameters
        'bot': 0 - thickness_shallow_aquifer,
        'K_hor': 1,
        'K_vert': 0.1,
        'porosity': 0.3
        'redoxzone': 1,  # concentration parameters
        'organic_carbon': 0.1,
      	''
    },
    'geolayer2': {
        ....
    },
}

well_parameters = {
    'well1': {
        'top': 0 - thickness_vadoze_zone - thickness_shallow_aquifer,
        'bot': 0 - thickness_vadoze_zone - thickness_shallow_aquifer - thickness_target_aquifer,
        'discharge': - well_discharge_m3hour / 24,
        'screenradius': WELL_SCREEN_DIAMETER / 2,
      	'dz_well': DZ_WELL,
        'endpoint_id': 'well1',  # default: same as well key
    },
    'well2': {
        'IBOUND': 0,  # 0=inactive, -1 -> fixed head
      	'head': 0,
        'top': 0,
        'screenradius': WELL_SCREEN_DIAMETER / 2,
      	'dz_well': DZ_WELL,
        'bot': 0 - thickness_vadoze_zone - thickness_shallow_aquifer,
        'endpoint_id': 'well2',
    },

backfill_parameters = {
    'backfill1': {
        'boreholeradius' : BOREHOLE_DIAMETER / 2,
        'K_hor': 
        }

drain_parameters = {
    'depth':
    'discharge':
    }
  
surfacewater_parameters = {
   'water_level': ....
    } 
# ->  hierboven is alles 1 class of 1 dict, hoort in ieder geval in 1 entiteit thuis
--------------------------------


class Substance():
    """ Returns transport properties for a given Organic Micro Pollutant."""
    def __init__(self):
  def getCid(self):
		pass
  def getSmiles(cid):
  	pass
  def getKow(self, redox_zone):
  	pass
# -> check hoe dit in huidige AQP zit. alleen getKow etc. is nieuw


class MicrobialProperties():
    """ Return transport properties for a given virus or bacteria species."""
    # to implement in next project phase


class AnalyticalWell():
    """ Compute travel time distribution using analytical well functions."""
 
  	def __init__(self):
    		""" 'unpack/parse' all the variables from the hydrogeochemical schematizization """
  	  	for key, item for input_dict.items():
          self.thickness_vadoze_zone = from dict
          self.df_flowline = .... get all fucking user input .... #make the df hee, add what we have
          self.df_particle = .... get all fucking user input ....
  
  
    def _check_init_freatic():
       	#check the variables that we need for the individual aquifer types are not NONE aka set by the user
  			pass
    def _blablaequation():
        pass
  
  	def _check_init_confined():
  			pass
  	def _thiemequation():
        pass
  
  	def freatic():
  		  self._check_init_freatic
  		  self._blablaequation
        pass
  
    def semiconfined():
  			self._check_init_confined
  			self._thiemequation()
  			# solve freatic functions
  		  pass
  
  	def export_to_df(self, what_to_export='all')
  	    """ Export to dataframe....

        Parameters
        ----------
        what_to_export: String
        		options: 'all', 'omp_parameters', 'microbial_parameters'
        """
  			#delete the unwanted columns depending on what the user asks for here
  			returns df_flowline, df_particle

  
# the python user will call the function as follows
well = AnalyticalWell()
if schematisation == 'freatic':
		well.freatic()
elif schematisation == 'semiconfined':
		well.semiconfined()
else:
  	raise KeyError('schematisation argument not recognized')
df_flow, df_particle = well.export_to_df('all')


class ModPathWell():
    """ Compute travel time distribution using MODFLOW and MODPATH.""" 
    def _check_init_freatic():
        # check the variables that we need for the individual aquifer types are not NONE aka set by the user
  
    def _check_init_semi_confined():
        # check the variables that we need for the individual aquifer types are not NONE aka set by the user

 		def make_radial_discretisation()
  			""" Generate distance between columns for axisymmetric model.
            Sets it to self.delr
        """
  			self.delr
  
   		def make_vertical_discretisation()
  			""" Generate top's and bot's of MODFLOW layers.
            Sets it to self.tops, self.bots
        """
				self.top
  			self.bots
  
  	def make_discretisation():
  			self.grid
 
  	def assign_material  
  			self.material  # name of dictionary
  			self.wells
   
  
  	def assign_aquifer_parameters():
        self.khor
  			self.VANI
  			etc.,

  	def assign_wells():
  	    self.WELL_pacakage  # np.array
  			self.Q
  			self.well_id

    	def assign_multi_nodal_well():
  	    self.wellid  # np.array
  			self.....

  
	  def assign_ibound():
        self.ibound  # 3 D grid
  			self.head

  	def assign_recharge_boundary():
  			self.recharge  #2 D grid
  
  
    def create_modflow_packages(... , *kwargs):
				""" Generate flopy files."""
				self.dry_cells  #
  			self.other_general_parameters  #
  
    def generate_modflow_files():
				""" Generate input files for modflow computation."""

    def run_modflow():
  			run modflow
  			if condition X is met:
						self.modflow_has_run = True
 
  	def modpath_startpoints_recharge():
				""" Generate startpoints for MODPATH forward computation.
        
        Parameters
        ----------
        xmin_start_particle  # close to well, default = 0
  			xmax_start_particle  # far away from well, default = model radius
  			number_of_particles  # user defined, defualt 100        
        
        Return
        ------
        df_startpoints: pd.DataFrame  # OR DICTIONARY IF THAT IS EASIER -> STEVEN
		        columns: col, row, lay, localx, localy, localz, flowline_id, startpoint_id, discharge
        """
  			init: self.xmin_start_particle = 0
  			self.number_of_particles = ....
	  		self.xmax_start_particle = well_radius if not defined
  
  			# distribute start point particles based on equal distance
				dx = (xmax - xmin) / number_of_particles
	
  			discharge = integrate volume
  
  			self.df_startpoints
  			
  
   	def modpath_endpoints_from_well():
  			# same as above, for wells
 
    def create_modpath_packages(self.df_startpoints):
				self.track_direction  # forward or backward
 
    def generate_modpath_files():
  
    def run_modpath():
 				self.modpath_has_run
  			if condition X is met:
						self.modpath_has_run = True

  	def export_to_df(self, grid_material, what_to_export='all')
  	    """ Export to dataframe....

        Parameters
        ----------
        what_to_export: String
        		options: 'all', 'omp_parameters', 'microbial_parameters'
        """
  			#delete the unwanted columns depending on what the user asks for here
  			returns df_flowline, df_particle
  
#%%  
class ModPathWell_OLD():
    """ Compute travel time distribution using MODFLOW and MODPATH.""" 

    def _check_init_freatic():
        # check the variables that we need for the individual aquifer types are not NONE aka set by the user
  
    def _check_init_semi_confined():
        # check the variables that we need for the individual aquifer types are not NONE aka set by the user

	  def model_size_freatic():
				""" Compute Radius based on discharge of wells and recharge rate.
        
        Returns
        -------
        Radius of model
        """

 		def make_hydrogeological_schematisation()
  			""" make hydrogeological schematisation.
            Sets it to self.radius
        """
        #  convert dict with geological schematisation at well1 location to df 
        df = pd.DataFrame([self.geodict])
  		  # order df from top to bot
  
  			# to do later: give warning if space between top-bottom

  			# identify aquifers and confining layers
  			mask = df['k_vertical'] < 0.01
  
  			# add column to df -> contains well True/False
  
        # find all layers containing well screen
			  # target_layers --> (top 'well' > bottom 'formation') & (bottom 'well' < top 'formation')
  
  			# get aquifer properties (kD, c) in layer containing well -> kD, c_below, c_above
  
  			self.df_schematisation = df
  
    def model_size_semiconfined():
				""" Compute radius based on 5 * spreading distance (labda = sqrt[kDc]).
            Sets it to self.radius
        """
  			KD = .... functie -> 
  			c = .... functie ->  1/ (1/c_above + 1/c_below)
  			labda = sqrt(KD * c)
  			radius = 5 * labda
  			self.radius = radius

    def discretization(radius, df_schematisation):
  			""" Generate discretisation of model.
        
        Parameters
        ----------
        borehole -> 0, 1 or many columns 
        """"
	  	  # Make extra second row to allow modpath
  
  			# horizontal: filterscreen
  
  		  # horizontal: borehole
  
  			# horizontal: tot 1xlengte  filters (of target aquifer)
  
  			# horizontal: tot modelrand
  
  			# verticaal: lagen met putten -> user defined dZ binnen putfilter
  
  			# verticaal: lagen zonder putten -> user defined dZ
  
  			# verticaal: phreatic aquifer -> prevent that cells fall dry
  
  			return del_r, del_c, del_l  #also x_mid, z_mid??

  	def assign_array()
  		'""" for each grid cell -> geo1, geo2, well1, well2, etc."""
  	    self.grid_material  # np.array
 
  	def fixed_head_well_boundary():
        self.grid_ibound

	  def fixed_discharge_well_boundary():
        self.grid_fixed_discharge

  	def recharge_boundary():
  			self.grid2D_recharge
  
  	def fixed_head_model_boundary():

  
	  def no_flow_model_boundary():
  
  
  	def assign_parameters():
  			""" Convert grid_material to parameters."""
  	    self.K_vertical_grid =function(grid_material, dictionary_material_properties)

    def assign_parameters_axisysmetric():

    def create_modflow_packages(... , *kwargs):
				""" Generate flopy files."""
				self.dry_cells  #
  			self.other_general_parameters  #
  
    def generate_modflow_files():
				""" Generate input files for modflow computation."""

    def run_modflow():
  			run modflow
  			if condition X is met:
						self.modflow_has_run = True
 
  	def modpath_startpoints_from_recharge():
				""" Generate startpoints for MODPATH computation.
        
        Parameters
        ----------
        xmin_start_particle  # close to well, default = 0
  			xmax_start_particle  # far away from well, default = model radius
  			number_of_particles  # user defined, defualt 100        
        
        Return
        ------
        df_startpoints: pd.DataFrame  # OR DICTIONARY IF THAT IS EASIER -> STEVEN
		        columns: col, row, lay, localx, localy, localz, flowline_id, startpoint_id, discharge
        """
  			init: self.xmin_start_particle = 0
  			self.number_of_particles = ....
	  		self.xmax_start_particle = well_radius if not defined
  
  			# distribute start point particles based on equal distance
				dx = (xmax - xmin) / number_of_particles
	
  			discharge = integrate volume
  
  			self.df_startpoints
  			
  
   	def modpath_endpoints_from_well():
  			# same as above, for wells
 
    def create_modpath_packages(self.df_startpoints):
				self.track_direction  # forward or backward
 
    def generate_modpath_files():
  
    def run_modpath():
 				self.modpath_has_run
  			if condition X is met:
						self.modpath_has_run = True

  	def export_to_df(self, grid_material, what_to_export='all')
  	    """ Export to dataframe....

        Parameters
        ----------
        what_to_export: String
        		options: 'all', 'omp_parameters', 'microbial_parameters'
        """
  			#delete the unwanted columns depending on what the user asks for here
  			returns df_flowline, df_particle

well = ModpathWell()
if tracking_direction = 'forward'
		well.modpath_startpoints_from_recharge()
elif tracking_direction = 'backward'
		well.modpath_endpoints_from_well()
else
  	raise KeyError('tracking direction argument not recognized')
df_flow, df_particle = well.export_to_df('all')
 
  
#%%
class Concentration():
    """ Returns concentration in a groundwater well for a given Organic Micro Pollutant or microbial species.

    Parameters
    ----------
    df_flowline: pandas.DataFrame
        Column 'flowline_id': Integer
        Column 'discharge': Float
            Discharge associated with the flowline (m3/d)
        Column 'particle_release_date': Float
        Column 'input_concentration'
        Column 'start_or_end_point_id': Integer ######################################
        		ID of Well (or drain) where the flowline ends

    df_particle: pandas.DataFrame
        Column 'flowline_id'
        Column 'travel_time'
        Column 'xcoord'
        Column 'ycoord'
        Column 'zcoord'
        Column 'redox_zone'
        Column 'temperature'
        Column 'Kow'  # only necessary for OMP
        Column 'Labda'  # only necessary for microbiology

    Returns
    -------    
		

    """

    def __init__(self, substance: Substance, df_particle, df_flowline, removel_function?):
        self.omp_inialized = False

  
  	def _init_omp()
  		if self.omp_inialized:
	  		self.df_part['Kow'] = self.df_part['redox_zone'].apply(lambda x: substance.get_Kow(x)
   		self.omp_inialized = True


  	def _init_microbiology()


  	def compute_omp_removal(self):
       """ Returns the concentrain at each particle point.
       
       Paramneters
       -----------
       df_flowline, df_particle
       
       Returns
       -------
       df_particle: pandas.DataFrame
       			extra column: 
       			extra column: concentration
            extra column: Retardation
            extra column: break_through_time
       
       """
			 self._init_omp()
       self.df_part...

    def compute_microbiology_removal(self):
                                                             
	  def compute_well_concentration(self, evaluation_time = None)
        """ Returns the concentration in the raw water of each well (as defined by endpoind_id)."""
      	if evaluation_time is None:
          select all flowlines
        else:
          select flowline with break_through_time < evaluation_time                                                  
		  	conc_flowline = concentration at end of selected flowline
				concentration_well = sum (conc_selected_flowline_i * discharge_flowline_i) / sum discharge_all_flowline                                                             


    def plot_concentration(self)
                                           
    def plot_age_distribution(self)

    def plot_logremoval(self)
#%%
class Test():
	def __init__(self):
		self.alex = None
                                                             
	def call_alex(self):                                    
		self.alex = 'called'
	def print_it(self):
		print(self.alex)
                                                    
# %%                       
# the python user will call the function as follows
concentration = Concentration()
if removal_function = 'omp':
		concentration.compute_omp_removal
elif removal_function = 'omp':
		concentration.compute_microbiology_removal
else
  	raise KeyError('schematisation argument not recognized')
                       