#COLORS
import os 

dark_blue = '#0f1925' 
light_blue = '#3a558c' 
dark_green  = '#162113' 
light_green = '#676a45' 
dark_coat = '#412521 ' 
light_coat = '#5d3232' 

os.environ['frame_border_active_color'] =  '#222222cc' #IDK
os.environ['frame_border_active_color'] = '#ff5d3232'
os.environ['frame_border_normal_color'] = dark_blue # panel top
os.environ['frame_bg_normal_color'] = dark_blue #nieaktywne okno ramka
os.environ['frame_bg_active_color'] = '#3a558c' #aktywne okno ramka


os.environ['theme_active_color'] = light_coat # ramka okna?
os.environ['theme_title_color'] = '#ffffff' # text?
os.environ['theme_normal_color'] = dark_coat # #323232dd okno nieaktywne
os.environ['theme_urgent_color'] = '#7811A1dd'
os.environ['theme_normal_title_color'] = '#898989' # text?
