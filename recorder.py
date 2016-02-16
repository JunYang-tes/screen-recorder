from GUI import GUIFactory
from py import RecorderFactory
from py import configuration
from py import localization
from plugins import PluginFactory

def on_start(config,is_screen_recorder=True):

    for p in __enable_plugins:
        try:
            p.run(config)
        except Exception as e:
            print (e)
    if is_screen_recorder:
        cfg.recorder.start(config)
    else:
        cfg.step_recorder.start(config)


def on_stop():
    cfg.recorder.stop()
    for p in __enable_plugins:
        p.stop()


def on_pause():
    cfg.recorder.pause()


def on_restart():
    cfg.recorder.restart()

#load config
cfg=configuration.cfg
GUIFactory.setGUIImpl(cfg.get("gui"))
localization.set_location(cfg.get("language"))
cfg.recorder=RecorderFactory.get_by_name(cfg.get("screen_recorder"))
cfg.step_recorder=RecorderFactory.get_by_name(cfg.get("step_recorder"))
if cfg.recorder is not None:
    cfg.recorder_filter=cfg.recorder.filter
if cfg.step_recorder is not None:
    cfg.step_recorder_filter=cfg.step_recorder.filter
cfg_item_name=cfg.get("gui")


#get main object

main = GUIFactory.getClass("Main")(cfg.gui_cfg_item(cfg_item_name),cfg.gui_user_cfg_item(cfg_item_name))
#set callbacks
main.set_on_start(on_start)
main.set_on_pause(on_pause)
main.set_on_restart(on_restart)
main.set_on_stop(on_stop)


#load plugin
__enable_plugins=[]
for name in cfg.get("plugins"):
    program_cfg={}
    user_cfg={}
    program_cfg=cfg.plugin_cfg_item(name)
    user_cfg=cfg.plugin_user_cfg_item(name)
    __enable_plugins.append(PluginFactory.get_plugin_instance(name,program_cfg,user_cfg))


main.run()



#save config
cfg.set(cfg_item_name,main.get_cfg())
cfg.set(cfg_item_name,main.get_user_cfg(),True)

for p in __enable_plugins:
    cfg.set(p.name,p.get_cfg())
    cfg.set(p.name,p.get_user_cfg(),True)
cfg.save()


