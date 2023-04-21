import logging


# Define a custom log format
class ASCII(logging.Formatter):
    header = r"""

\::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\:::::.\::::::::.\::::::::.\::::::::.\


                                ,,                                                                        
`7MMM.     ,MMF'         mm     db               .MMM"bgd                   mm                            
  MMMb    dPMM           MM                     ,MI    "Y                   MM                            
  M YM   ,M MM  .gP"Ya mmMMmm `7MM  ,pP"Ybd     `MMb.  `7M'   `MF',pP"Ybd mmMMmm .gP"Ya `7MMpMMMb.pMMMb.  
  M  Mb  M' MM ,M'   Yb  MM     MM  8I   `"       `YMMNq.VA   ,V  8I   `"   MM  ,M'   Yb  MM    MM    MM  
  M  YM.P'  MM 8M""""""  MM     MM  `YMMMa.     .     `MM VA ,V   `YMMMa.   MM  8Meeeee  MM    MM    MM  
  M  `YM'   MM YM.    ,  MM     MM  L.   I8     Mb     dM  VVV    L.   I8   MM  YM.    ,  MM    MM    MM  
.JML. `'  .JMML.`Mbmmd'  `Mbmo.JMML.M9mmmP'     P"Ybmmd"   ,V     M9mmmP'   `Mbmo`Mbmmd'.JMML  JMML  JMML.
                                                          ,V                                              
                                                       OOb"                           


\::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\:::::.\::::::::.\::::::::.\::::::::.\       


"""
    
    def metis_system_init(self):
        return self.header



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


