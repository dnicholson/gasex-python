#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 21:33:50 2017

Functions for calculating dissolved gas solubility

@author: dnicholson
"""

from __future__ import division
import numpy as np
from gsw import pt_from_CT,SP_from_SA
from ._utilities import match_args_return


__all__ = ['O2sol_SP_pt','Hesol_SP_pt','Nesol_SP_pt','Arsol_SP_pt', \
           'Krsol_SP_pt','N2sol_SP_pt','N2Osol_SP_pt','O2sol','Hesol', \
           'Nesol','Arsol','Krsol','N2sol','N2Osol']


UNITS = 'umol kg-1'
    
@match_args_return
def O2sol_SP_pt(SP,pt):

    """
     gsw_O2_SP_pt                              solubility of O2 in seawater
    ==========================================================================
    
     USAGE: 
    import sol
    O2sol = sol.O2_SP_pt(35,20)
    
     DESCRIPTION:
      Calculates the oxygen concentration expected at equilibrium with air at 
      an Absolute Pressure of 101325 Pa (sea pressure of 0 dbar) including 
      saturated water vapor.  This function uses the solubility coefficients 
      derived from the data of Benson and Krause (1984), as fitted by Garcia 
      and Gordon (1992, 1993).
    
      Note that this algorithm has not been approved by IOC and is not work 
      from SCOR/IAPSO Working Group 127. It is included in the GSW
      Oceanographic Toolbox as it seems to be oceanographic best practice.
    
     INPUT:  
      SP  =  Practical Salinity  (PSS-78)                         [ unitless ]
      pt  =  potential temperature (ITS-90) referenced               [ deg C ]
             to one standard atmosphere (0 dbar).
    
      SP & pt need to have the same dimensions.
    
     OUTPUT:
      O2sol = solubility of oxygen in micro-moles per kg           [ umol/kg ] 
     
     AUTHOR:  Roberta Hamme, Paul Barker and Trevor McDougall
                                                          [ help@teos-10.org ]
    
     VERSION NUMBER: 3.05 (27th January 2015)
    
     REFERENCES:
      IOC, SCOR and IAPSO, 2010: The international thermodynamic equation of 
       seawater - 2010: Calculation and use of thermodynamic properties.  
       Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
       UNESCO (English), 196 pp.  Available from http://www.TEOS-10.org
    
      Benson, B.B., and D. Krause, 1984: The concentration and isotopic 
       fractionation of oxygen dissolved in freshwater and seawater in 
       equilibrium with the atmosphere. Limnology and Oceanography, 29, 
       620-632.
    
      Garcia, H.E., and L.I. Gordon, 1992: Oxygen solubility in seawater: 
       Better fitting equations. Limnology and Oceanography, 37, 1307-1312.
    
      Garcia, H.E., and L.I. Gordon, 1993: Erratum: Oxygen solubility in 
       seawater: better fitting equations. Limnology and Oceanography, 38,
       656.
    
      The software is available from http://www.TEOS-10.org
    
    ==========================================================================
    """


    x = SP        # Note that salinity argument is Practical Salinity, this is
             # beacuse the major ionic components of seawater related to Cl  
          # are what affect the solubility of non-electrolytes in seawater.   

    pt68 = pt * 1.00024     # pt68 is the potential temperature in degress C on 
              # the 1968 International Practical Temperature Scale IPTS-68.
    y = np.log((298.15 - pt68)/(273.15 + pt68))

# The coefficents below are from the second column of Table 1 of Garcia and
# Gordon (1992)
    a = [5.80871,3.20291,4.17887,5.10006,-9.86643e-2,3.80369] 
    b = [-7.01577e-3,-7.70028e-3,-1.13864e-2,-9.51519e-3]
    c = -2.75915e-7


    lnC = (a[0] + y * (a[1] + y * (a[2] + y * (a[3] + y * (a[4] + a[5] * y))))\
          + x * (b[0] + y * (b[1] + y * (b[2] + b[3] * y)) + c * x))

    return np.exp(lnC)


@match_args_return
def O2sol(SA,CT,p,long,lat):
    """
     O2      Solubility of O2 in seawater from absolute salinity and cons temp
    ==========================================================================
    """
    SP = SP_from_SA(SA,p,long,lat)
    pt = pt_from_CT(SA,CT)
    return O2sol_SP_pt(SP,pt)
    

@match_args_return
def Hesol_SP_pt(SP,pt):
    """
     gsw_Hesol_SP_pt                              solubility of He in seawater
    ==========================================================================
    
     USAGE:  
      Hesol = gsw_Hesol_SP_pt(SP,pt)
    
     DESCRIPTION:
      Calculates the helium concentration expected at equilibrium with air at 
      an Absolute Pressure of 101325 Pa (sea pressure of 0 dbar) including 
      saturated water vapor.  This function uses the solubility coefficients
      as listed in Weiss (1971).
    
      Note that this algorithm has not been approved by IOC and is not work 
      from SCOR/IAPSO Working Group 127. It is included in the GSW
      Oceanographic Toolbox as it seems to be oceanographic best practice.
    
     INPUT:  
      SP  =  Practical Salinity  (PSS-78)                         [ unitless ]
      pt  =  potential temperature (ITS-90) referenced               [ deg C ]
             to one standard atmosphere (0 dbar).
    
      SP & pt need to have the same dimensions.
    
     OUTPUT:
      Hesol = solubility of helium in micro-moles per kg           [ umol/kg ] 
     
     AUTHOR:  Roberta Hamme, Paul Barker and Trevor McDougall
                                                          [ help@teos-10.org ]
    
     VERSION NUMBER: 3.05 (27th January 2015)
    
     REFERENCES:
      IOC, SCOR and IAPSO, 2010: The international thermodynamic equation of 
       seawater - 2010: Calculation and use of thermodynamic properties.  
       Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
       UNESCO (English), 196 pp.  Available from http://www.TEOS-10.org
    
      Dymond and Smith, 1980: The virial coefficients of pure gases and
       mixtures. Clarendon Press, Oxford.
    
      Weiss, R.F., 1971: Solubility of Helium and Neon in Water and Seawater.
       J. Chem. and Engineer. Data, 16, 235-241.
    
      The software is available from http://www.TEOS-10.org
    
    ==========================================================================
    """
    x = SP        # Note that salinity argument is Practical Salinity, this is
             # beacuse the major ionic components of seawater related to Cl  
          # are what affect the solubility of non-electrolytes in seawater.   

    pt68 = pt * 1.00024 # pt68 is the potential temperature in degress C on 
                  # the 1968 International Practical Temperature Scale IPTS-68.
    y = pt68 + 273.15
    y_100 = y * 1e-2
    
    # The coefficents below are from Table 3 of Weiss (1971)
    a = [-167.2178, 216.3442, 139.2032, -22.6202]
    b = [-0.044781, 0.023541, -0.0034266]
    
    Hesol_mL = np.exp(a[0] + a[1] * 100/y + a[2] * np.log(y_100) + a[3] * \
                      y_100 + x * (b[0] + y_100 * (b[1] + b[2] * y_100)))
    
    Hesol = Hesol_mL * 4.455817671505537e1
    # mL/kg to umol/kg for He (1/22.44257e-3) 
    #Molar volume at STP (Dymond and Smith, 1980).
    return Hesol


@match_args_return
def Hesol(SA,CT,p,long,lat):
    """
     He      Solubility of He in seawater from absolute salinity and cons temp
    ==========================================================================
    """
    SP = SP_from_SA(SA,p,long,lat)
    pt = pt_from_CT(SA,CT)
    return Hesol_SP_pt(SP,pt)

@match_args_return
def Nesol_SP_pt(SP,pt):
    """
     gsw_Nesol_SP_pt                              solubility of Ne in seawater
    ==========================================================================
    
     USAGE:  
      Nesol = gsw_Nesol_SP_pt(SP,pt)
    
     DESCRIPTION:
      Calculates the Neon, Ne, concentration expected at equilibrium with air 
      at an Absolute Pressure of 101325 Pa (sea pressure of 0 dbar) including
      saturated water vapor.  This function uses the solubility coefficients
      as listed in Hamme and Emerson (2004).
    
      Note that this algorithm has not been approved by IOC and is not work 
      from SCOR/IAPSO Working Group 127. It is included in the GSW
      Oceanographic Toolbox as it seems to be oceanographic best practice.
    
     INPUT:  
      SP  =  Practical Salinity  (PSS-78)                         [ unitless ]
      pt  =  potential temperature (ITS-90) referenced               [ deg C ]
             to one standard atmosphere (0 dbar).
    
      SP & pt need to have the same dimensions.
    
     OUTPUT:
      Nesol = solubility of neon in nano-moles per kg              [ nmol/kg ] 
     
     AUTHOR:  Roberta Hamme, Paul Barker and Trevor McDougall
                                                          [ help@teos-10.org ]
    
     REFERENCES:
      IOC, SCOR and IAPSO, 2010: The international thermodynamic equation of 
       seawater - 2010: Calculation and use of thermodynamic properties.  
       Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
       UNESCO (English), 196 pp.  Available from http://www.TEOS-10.org
    
      Hamme, R., and S. Emerson, 2004: The solubility of neon, nitrogen and
       argon in distilled water and seawater. Deep-Sea Research, 51, 
       1517-1528.
    
      The software is available from http://www.TEOS-10.org
    
    ==========================================================================
    """
    x = SP     
    # Note that salinity argument is Practical Salinity, this is
    # beacuse the major ionic components of seawater related to Cl  
    # are what affect the solubility of non-electrolytes in seawater.   
    
    y = np.log((298.15 - pt)/(273.15 + pt))  
    # pt is the temperature in degress C on the ITS-90 scale
    
    # The coefficents below are from Table 4 of Hamme and Emerson (2004)
    a =  [2.18156, 1.29108, 2.12504]
    b = [-5.94737e-3, -5.13896e-3]
    
    # umol kg-1 for consistency with other gases
    Nesol = 1e3 * np.exp(a[0] + y * (a[1] + a[2] * y) + x * (b[0] + b[1] * y))
    return Nesol

@match_args_return
def Nesol(SA,CT,p,long,lat):
    """
     Ne      Solubility of Ne in seawater from absolute salinity and cons temp
    ==========================================================================
    """
    SP = SP_from_SA(SA,p,long,lat)
    pt = pt_from_CT(SA,CT)
    return Nesol_SP_pt(SP,pt)

@match_args_return
def Arsol_SP_pt(SP,pt):
    """
     Arsol_SP_pt                              solubility of Ar in seawater
    ==========================================================================
    
     USAGE:  
      Arsol = gsw_Arsol_SP_pt(SP,pt)
    
     DESCRIPTION:
      Calculates the argon, Ar, concentration expected at equilibrium with air 
      at an Absolute Pressure of 101325 Pa (sea pressure of 0 dbar) including
      saturated water vapor  This function uses the solubility coefficients
      as listed in Hamme and Emerson (2004).
    
      Note that this algorithm has not been approved by IOC and is not work 
      from SCOR/IAPSO Working Group 127. It is included in the GSW
      Oceanographic Toolbox as it seems to be oceanographic best practice.
    
     INPUT:  
      SP  =  Practical Salinity  (PSS-78)                         [ unitless ]
      pt  =  potential temperature (ITS-90) referenced               [ deg C ]
             to one standard atmosphere (0 dbar).
    
      SP & pt need to have the same dimensions.
    
     OUTPUT:
      Arsol = solubility of argon                                  [ umol/kg ] 
     
     AUTHOR:  David Nicholson
     Adapted from gsw_Arsol_SP_pt authored by Roberta Hamme, Paul Barker and 
         Trevor McDougall
                                                          [ help@teos-10.org ]
    
     REFERENCES:
      IOC, SCOR and IAPSO, 2010: The international thermodynamic equation of 
       seawater - 2010: Calculation and use of thermodynamic properties.  
       Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
       UNESCO (English), 196 pp.  Available from http://www.TEOS-10.org
    
      Hamme, R., and S. Emerson, 2004: The solubility of neon, nitrogen and
       argon in distilled water and seawater. Deep-Sea Research, 51, 
       1517-1528.
    
      The software is available from http://www.TEOS-10.org
    
    ==========================================================================
    """

    x = SP     
    # Note that salinity argument is Practical Salinity, this is
    # beacuse the major ionic components of seawater related to Cl  
    # are what affect the solubility of non-electrolytes in seawater.   
    
    y = np.log((298.15 - pt)/(273.15 + pt))  
    # pt is the temperature in degress C on the ITS-90 scale
    
    # The coefficents below are from Table 4 of Hamme and Emerson (2004)
    a =  [2.79150, 3.17609, 4.13116, 4.90379]
    b = [-6.96233e-3, -7.66670e-3, -1.16888e-2]
    
    Arsol = np.exp(a[0] + y * (a[1] + y * (a[2] + a[3] * y)) + x * \
                   (b[0] + y *(b[1] + b[2] *y )))
    return Arsol

@match_args_return
def Arsol(SA,CT,p,long,lat):
    """
     Ar      Solubility of Ar in seawater from absolute salinity and cons temp
    ==========================================================================
    """
    SP = SP_from_SA(SA,p,long,lat)
    pt = pt_from_CT(SA,CT)
    return Arsol_SP_pt(SP,pt)

@match_args_return
def Krsol_SP_pt(SP,pt):
    """
     Krsol_SP_pt                              solubility of Kr in seawater
    ==========================================================================
    
     USAGE:  
      Krsol = sol.Krsol_SP_pt(SP,pt)
    
     DESCRIPTION:
      Calculates the krypton, Kr, concentration expected at equilibrium with  
      air at an Absolute Pressure of 101325 Pa (sea pressure of 0 dbar) 
      including saturated water vapor.  This function uses the solubility 
      coefficients derived from the data of Weiss (1971).
    
      Note that this algorithm has not been approved by IOC and is not work 
      from SCOR/IAPSO Working Group 127. It is included in the GSW
      Oceanographic Toolbox as it seems to be oceanographic best practice.
    
     INPUT:  
      SP  =  Practical Salinity  (PSS-78)                         [ unitless ]
      pt  =  potential temperature (ITS-90) referenced               [ deg C ]
             to one standard atmosphere (0 dbar).
    
      SP & pt need to have the same dimensions.
    
     OUTPUT:
      Krsol = solubility of krypton in micro-moles per kg          [ umol/kg ] 
     
     AUTHOR:  Roberta Hamme, Paul Barker and Trevor McDougall
                                                          [ help@teos-10.org ]
    
     VERSION NUMBER: 3.05 (27th January 2015)
    
     REFERENCES:
      IOC, SCOR and IAPSO, 2010: The international thermodynamic equation of 
       seawater - 2010: Calculation and use of thermodynamic properties.  
       Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
       UNESCO (English), 196 pp.  Available from http://www.TEOS-10.org
    
      Weiss, R.F. and T.K. Kyser, 1978: Solubility of Krypton in Water and 
       Seawater. J. Chem. Thermodynamics, 23, 69-72.
    
      The software is available from http://www.TEOS-10.org
    
    ==========================================================================
    """
    x = SP        # Note that salinity argument is Practical Salinity, this is
             # beacuse the major ionic components of seawater related to Cl  
          # are what affect the solubility of non-electrolytes in seawater.   

    pt68 = pt * 1.00024 # pt68 is the potential temperature in degress C on 
                  # the 1968 International Practical Temperature Scale IPTS-68.
    y = pt68 + 273.15
    y_100 = y * 1e-2

    # Table 2 (Weiss and Kyser, 1978)
    a = [-112.6840, 153.5817, 74.4690, -10.0189]
    b = [-0.011213, -0.001844, 0.0011201]
    
    Krsol_mL = np.exp(a[0] + a[1] * 100/y + a[2] * np.log(y_100) + a[3] * \
                      y_100 + x * (b[0] + y_100 * (b[1] + b[2] * y_100)))
    
    # mL/kg to umol/kg for Kr (1/22.3511e-3)
    #Molar volume at STP (Dymond and Smith, 1980).
    Krsol = Krsol_mL * 4.474052731185490e1
    return Krsol

@match_args_return
def Krsol(SA,CT,p,long,lat):
    """
     Kr      Solubility of Kr in seawater from absolute salinity and cons temp
    ==========================================================================
    """
    SP = SP_from_SA(SA,p,long,lat)
    pt = pt_from_CT(SA,CT)
    return Krsol_SP_pt(SP,pt)

@match_args_return
def N2sol_SP_pt(SP,pt):
    """
     N2sol_SP_pt                              solubility of N2 in seawater
    ==========================================================================
    
     USAGE:  
      N2sol = sol.N2sol_SP_pt(SP,pt)
    
     DESCRIPTION:
      Calculates the nitrogen, N2, concentration expected at equilibrium with  
      air at an Absolute Pressure of 101325 Pa (sea pressure of 0 dbar) 
      including saturated water vapor.  This function uses the solubility 
      coefficients as listed in Hamme and Emerson (2004).
    
      Note that this algorithm has not been approved by IOC and is not work 
      from SCOR/IAPSO Working Group 127. It is included in the GSW
      Oceanographic Toolbox as it seems to be oceanographic best practice.
    
     INPUT:  
      SP  =  Practical Salinity  (PSS-78)                         [ unitless ]
      pt  =  potential temperature (ITS-90) referenced               [ deg C ]
             to one standard atmosphere (0 dbar).
    
      SP & pt need to have the same dimensions.
    
     OUTPUT:
      N2sol = solubility of nitrogen in micro-moles per kg         [ umol/kg ] 
     
     AUTHOR:  Roberta Hamme, Paul Barker and Trevor McDougall
                                                          [ help@teos-10.org ]
    
     VERSION NUMBER: 3.05 (27th January 2015)
    
     REFERENCES:
      IOC, SCOR and IAPSO, 2010: The international thermodynamic equation of 
       seawater - 2010: Calculation and use of thermodynamic properties.  
       Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
       UNESCO (English), 196 pp.  Available from http://www.TEOS-10.org
    
      Hamme, R., and S. Emerson, 2004: The solubility of neon, nitrogen and
       argon in distilled water and seawater. Deep-Sea Research, 51, 
       1517-1528.
    
      The software is available from http://www.TEOS-10.org
    
    ==========================================================================
"""
    x = SP     
    # Note that salinity argument is Practical Salinity, this is
    # beacuse the major ionic components of seawater related to Cl  
    # are what affect the solubility of non-electrolytes in seawater.   
    
    y = np.log((298.15 - pt)/(273.15 + pt))  
    # pt is the temperature in degress C on the ITS-90 scale
    
    # The coefficents below are from Table 4 of Hamme and Emerson (2004)
    a = [6.42931, 2.92704, 4.32531, 4.69149]
    b = [-7.44129e-3, -8.02566e-3, -1.46775e-2]
    
    N2sol = np.exp(a[0] + y * (a[1] + y * (a[2] + a[3] * y)) + x * \
                   (b[0] + y *(b[1] + b[2] *y )))
    return N2sol

@match_args_return
def N2sol(SA,CT,p,long,lat):
    """
     N2      Solubility of N2 in seawater from absolute salinity and cons temp
    ==========================================================================
    """
    SP = SP_from_SA(SA,p,long,lat)
    pt = pt_from_CT(SA,CT)
    return N2sol_SP_pt(SP,pt)

@match_args_return
def N2Osol_SP_pt(SP,pt):
    """
     gsw_N2Osol_SP_pt                            solubility of N2O in seawater
    ==========================================================================
    
     USAGE:  
      N2Osol = gsw_N2Osol_SP_pt(SP,pt)
    
     DESCRIPTION:
      Calculates the nitrous oxide, N2O, concentration expected at equilibrium  
      with air at an Absolute Pressure of 101325 Pa (sea pressure of 0 dbar) 
      including saturated water vapor  This function uses the solubility 
      coefficients as listed in Hamme and Emerson (2004).
    
      Note that this algorithm has not been approved by IOC and is not work 
      from SCOR/IAPSO Working Group 127. It is included in the GSW
      Oceanographic Toolbox as it seems to be oceanographic best practice.
    
     INPUT:  
      SP  =  Practical Salinity  (PSS-78)                         [ unitless ]
      pt  =  potential temperature (ITS-90) referenced               [ deg C ]
             to one standard atmosphere (0 dbar).
    
      SP & pt need to have the same dimensions.
    
     OUTPUT:
      N2Osol = K' solubility of nitrous oxide                 mol kg-1 atm-1 ] 
              (solubility in moist air at total pressure of 1 atm)
              
     AUTHOR:  Rich Pawlowicz, Paul Barker and Trevor McDougall
                                                          [ help@teos-10.org ]
    
     VERSION NUMBER: 3.05 (27th January 2015)
    
     REFERENCES:
      IOC, SCOR and IAPSO, 2010: The international thermodynamic equation of 
       seawater - 2010: Calculation and use of thermodynamic properties.  
       Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
       UNESCO (English), 196 pp.  Available from http://www.TEOS-10.org
    
      Weiss, R.F. and B.A. Price, 1980: Nitrous oxide solubility in water and
       seawater. Mar. Chem., 8, 347-359.
       https://doi.org/10.1016/0304-4203(80)90024-9
    
      The software is available from http://www.TEOS-10.org
    
    ==========================================================================
    """
    x = SP        # Note that salinity argument is Practical Salinity, this is
             # beacuse the major ionic components of seawater related to Cl  
          # are what affect the solubility of non-electrolytes in seawater.   

    pt68 = pt * 1.00024 # pt68 is the potential temperature in degress C on 
                  # the 1968 International Practical Temperature Scale IPTS-68.
    y = pt68 + 273.15
    y_100 = y * 1e-2
    
    # The coefficents below are from Table 2 of Weiss and Price (1980)
    # These coefficients are for mol L-1 atm-1
    
    a = [-165.8806, 222.8743, 92.0792, -1.48425]
    b = [-0.056235, 0.031619, -0.0048472]
    
    # These coefficents below are from Table 2 of Weiss and Price (1980)
    # These coefficients are for mol kg-1 atm-1
    a = [-168.2459, 226.0894, 93.2817, -1.48693]
    b = [-0.060361 + 0.033765, -0.0051862]
    
    # Moist air correction at 1 atm.
    # fitted the vapor pressure of water as given by Goff and Gratch (1946), 
    # and the vapor pressure lowering by sea salt as given by Robinson (1954), 
    # to a polynomial in temperature and salinity:
    
    m = [24.4543, 67.4509, 4.8489, 0.000544]
    ph2odP = np.exp(m[0] - m[1]*100/y - m[2] * np.log(y_100) - m[3] * x) 
    
    N2Osol = (np.exp(a[0] + a[1] * 100/y + a[2] * np.log(y_100) + a[3] * \
                    y_100**2 + x * (b[0] + y_100 * (b[1] + b[2] * y_100)))) / \
                     (1-ph2odP)
    return N2Osol

@match_args_return
def N2Osol(SA,CT,p,long,lat):
    """
     N2O     Solubility of N2O in seawater from absolute salinity and cons temp
    ==========================================================================
    """
    SP = SP_from_SA(SA,p,long,lat)
    pt = pt_from_CT(SA,CT)
    return N2Osol_SP_pt(SP,pt)

@match_args_return
def CO2sol_SP_pt(SP,pt):
    """
     CO2sol_SP_pt            solubility of CO2 in seawater for 1 atm moist air
    ==========================================================================
    
     USAGE:  
      import gas.sol as sol
      CO2sol = sol.CO2sol_SP_pt(SP,pt)
    
     DESCRIPTION:
      Calculates the carbon dioxide, CO2, concentration expected at equilibrium 
      with air at an Absolute Pressure of 101325 Pa (sea pressure of 0 dbar) 
      including saturated water vapor.  This function uses the solubility 
      coefficients derived from the data of Weiss (1974) and refit in Weiss
      and Price (1980).
    
    
     INPUT:  
      SP  =  Practical Salinity  (PSS-78)                         [ unitless ]
      pt  =  potential temperature (ITS-90) referenced               [ deg C ]
             to one standard atmosphere (0 dbar).
    
      SP & pt need to have the same dimensions.
    
     OUTPUT:
      CO2sol = solubility of carbon dioxide at 1 atm moist   [ mol kg-1 atm-1 ] 
     
     AUTHOR:  David Nicholson
                                                        [ dnicholson@whoi.edu ]
    
    
     REFERENCES:
      Weiss, R.F. and B.A. Price, 1980: Nitrous oxide solubility in water and
        seawater. Mar. Chem., 8, 347-359.
        https://doi.org/10.1016/0304-4203(80)90024-9
      Weiss, R. (1974) Carbon Dioxide in Water and Seawater The Solubility of a 
        Non- Ideal Gas. Mar. Chem., 2, 203-215. 
        https://doi.org/10.1016/0304-4203(74)90015-2
    
    ==========================================================================
    """
    x = SP        # Note that salinity argument is Practical Salinity, this is
             # beacuse the major ionic components of seawater related to Cl  
          # are what affect the solubility of non-electrolytes in seawater.   

    pt68 = pt * 1.00024 # pt68 is the potential temperature in degress C on 
                  # the 1968 International Practical Temperature Scale IPTS-68.
    y = pt68 + 273.15
    y_100 = y * 1e-2

    # Table 6 (Weiss and Price, 1980)
    a = [-162.8301, 218.2968, 90.9241, -1.47696]
    b = [0.025695, -0.025225, 0.0049867]
    
    CO2sol = np.exp(a[0] + a[1] * 100/y + a[2] * np.log(y_100) + a[3] * \
                      y_100**2 + x * (b[0] + b[1] * y_100 + b[2] * y_100**2))
    return CO2sol

@match_args_return
def CO2sol(SA,CT,p,long,lat):
    """
     CO2    Solubility of CO2 in seawater from absolute salinity and cons temp
    ==========================================================================
    """
    SP = SP_from_SA(SA,p,long,lat)
    pt = pt_from_CT(SA,CT)
    return CO2sol_SP_pt(SP,pt)