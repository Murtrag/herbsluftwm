from utils.system import _cmd
# --theme-bg-color: #0f1925;
# --theme-bg-active-color: #3a558c;
# --theme-normal-color: #412521; /* brown elements on the panel */
# --theme-active-color: #5d3232; /* window frame */
# bgcolor=$(hc get frame_border_normal_color|sed 's,^\(\#[0-9a-f]\{6\}\)[0-9a-f]\{2\}$,\1,')
# selbg=$(hc get window_border_active_color|sed 's,^\(\#[0-9a-f]\{6\}\)[0-9a-f]\{2\}$,\1,')
def _extractVariable(var_name):
	try:
		return _cmd(['herbstclient', 'get', var_name]) 
	except Exception:
		return "red" #handler for not herbst environment

colors = {
	'theme_bg_color': _extractVariable('theme.background_color'),
	'theme_bg_active_color': _extractVariable('frame_bg_active_color'),
	'theme_normal_color': _extractVariable('theme.normal.color'),
	'theme_active_color': _extractVariable('theme.active.color'),

}
		


		
		
