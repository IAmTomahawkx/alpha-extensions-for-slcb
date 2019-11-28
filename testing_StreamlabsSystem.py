import os
import sys
import clr
import time
import json
import codecs
import System

# Required
from System.Reflection import *
clr.AddReference([asbly for asbly in System.AppDomain.CurrentDomain.GetAssemblies() if "AnkhBotR2" in str(asbly)][0])
import AnkhBotR2
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms.MessageBox import Show
msgbox = lambda obj: Show(str(obj))

# Script Information
Creator = "LuisSanchezDev"
Description = "description"
ScriptName = "New folder"
Version = "1.0"
Website = "https://www.fiverr.com/luissanchezdev"

path = os.path.dirname(os.path.realpath(__file__))
global test_hotkey
test_hotkey = None

# +----------------------+
# |  Required functions  |
# +----------------------+
def Init():
  msgbox("Try pressing Ctrl + Alt + Q after pressing OK")
  test_hotkey = Hotkey("test hotkey","Q",["Control", "Alt"], lambda: msgbox("We have global hotkeys now!!!"))
  test_hotkey.register()
def Execute(data): pass
def Tick(): pass
def Unload():
  global test_hotkey
  if test_hotkey != None:
    test_hotkey.unload()

# UI Button function
def test(): pass

# +--------------------+
# |  Utility functions |
# +--------------------+
def save_array_to_file(a,fp):
  with codecs.open(fp,"w",encoding="utf-8-sig") as f:
    f.write('\n'.join([str(a_item) for a_item in a]))

# +--------------+
# |  Extensions  |
# +--------------+
class Hotkey:
  """Create your custom hotkeys to run any function you want!"""
  def __init__(self,name,key_name,modifiers_names, callback):
    """ key_names found in https://docs.microsoft.com/en-us/dotnet/api/system.windows.input.key?view=netframework-4.8 """
    """ modifiers found in https://docs.microsoft.com/en-us/dotnet/api/system.windows.input.modifierkeys?view=netframework-4.8 """
    if isinstance(modifiers_names, str): modifiers_names = [modifiers_names]
    self.manager = AnkhBotR2.Managers.HotKeyManager.Instance
    ClrHotkey = AnkhBotR2.Managers.GlobalHotKey
    hotkey_ctor = clr.GetClrType(ClrHotkey).GetConstructors()[0]
    KeyType = hotkey_ctor.GetParameters()[1].ParameterType
    ModifierKeyType = hotkey_ctor.GetParameters()[2].ParameterType
    
    key_values = KeyType.GetEnumValues()
    key = [k for k in key_values if key_name == str(k)]
    if len(key) <= 0:
      raise ValueError("Specified key not found. requested="+key_name)
    key = key.pop()
    
    modifierkey_values = ModifierKeyType.GetEnumValues()
    
    m_keys = [k for k in modifierkey_values if str(k) in modifiers_names]
    if len(m_keys) != len(modifiers_names):
      raise ValueError(
        "One or all of the specified modifier keys was not found. requested={0}  found={1} ".format(
          modifiers_names, m_keys
        )
      )
    m_key = m_keys.pop()
    for m in m_keys: m_key = m_key | m
    
    self.hotkey = ClrHotkey(
      name, key, m_key, callback
    )
    #msgbox(self.hotkey)
  def register(self):
    self.manager.AddHotkey(self.hotkey)
  def unload(self):
    """Always unload on Unload to have the correct callback"""
    fields = get_all_fields_from_type(self.manager.GetType(),True)
    hotkeys_list = [f for f in fields if f.Name == "Hotkeys"][0].GetValue(self.manager)
    hotkeys_list.Remove(self.hotkey)
    del self.hotkey
  # hks = get_all_fields_from_type(hk_mgr.GetType(), True)[0].GetValue(hk_mgr)[0]

class TwithAPI:
  def __init__(self):
    asm = AnkhBotR2.App.Current.GetType().Assembly
    self.instance = asm.GetType("AnkhBotR2.Managers.TwitchAPI").GetProperty("Instance").GetValue(None, None)
  def _get_property(self,name):
    prop = [p for p in self.instance.GetType().GetProperties(BindingFlags.Instance | BindingFlags.NonPublic) if p.Name == name][0]
    return prop.GetValue(self.instance, None)
  
  def _run_method(self, method_name, params):
    method = [m for m in self.instance.GetType().GetMethods(BindingFlags.Instance | BindingFlags.NonPublic) if m.Name == method_name][0]
    return method.Invoke(self.instance, params)
  @property
  def ChannelName(self): return self._get_property("ChannelName")
  @property
  def CurrentGame(self): return self._get_property("CurrentGame")
  @property
  def IsStreaming(self): return self._get_property("IsStreaming")
  @property
  def FollowerCount(self): return self._get_property("FollowerCount")
  @property
  def SubCount(self): return self._get_property("SubCount")
  @property
  def ViewerCount(self): return self._get_property("ViewerCount")
  @property
  def StreamStartTime(self): return self._get_property("StreamStartTime")
  @property
  def PreviewUrl(self): return self._get_property("PreviewUrl")
  @property
  def ActiveId(self): return self._get_property("ActiveId")  
  def GetChannel(self, target): return self._run_method("GetChannel", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def GetCommunity(self, name): return self._run_method("GetCommunity", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def GetCurrentCommunity(self): return self._run_method("GetCurrentCommunity", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def GetFollowerCount(self): return self._run_method("GetFollowerCount", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def GetSubCount(self): return self._run_method("GetSubCount", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def GetSuggestedGames(self, game): return self._run_method("GetSuggestedGames", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def GetUserData(self, token): return self._run_method("GetUserData", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def GetUserID(self, user): return self._run_method("GetUserID", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def IsVerifiedBot(self, userId): return self._run_method("IsVerifiedBot", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def IsFollowing(self, user): return self._run_method("IsFollowing", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def IsValidToken(self, user, token, isStreamer): return self._run_method("IsValidToken", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def IsTargetLive(self, name): return self._run_method("IsTargetLive", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def RetrieveAllSubscribers(self): return self._run_method("RetrieveAllSubscribers", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def RetrieveAllFollowers(self): return self._run_method("RetrieveAllFollowers", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def RetrieveLiveChannels(self, channels, streamtype): return self._run_method("RetrieveLiveChannels", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def RetrieveCurrentHosts(self, perpage, page): return self._run_method("RetrieveCurrentHosts", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def RetrieveServers(self, channel): return self._run_method("RetrieveServers", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def RunCommercial(self, time): return self._run_method("RunCommercial", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))
  def UpdateGameTitle(self, title, game): return self._run_method("UpdateGameTitle", System.Array[object]([v for k,v in (lambda: locals())().iteritems()]))

def get_loaded_scripts():
  handler = AnkhBotR2.Managers.GlobalManager.Instance.SystemHandler
  fields = get_all_fields_from_type(handler.GetType(),True)
  python_systems = [f for f in fields if "SystemsPython" in f.Name][0].GetValue(handler)
  return [p.Script for p in python_systems]

def print_server_message(msg):
  g_manager = AnkhBotR2.Managers.GlobalManager.Instance
  handler = g_manager.SystemHandler
  handler.StreamerClient.PrintServerMessage(msg)
  handler.StreamerClient.WriteTextToUI()

def send_message_as_streamer(msg):
  g_manager = AnkhBotR2.Managers.GlobalManager.Instance
  handler = g_manager.SystemHandler
  handler.StreamerClient.SendMessage(msg)

def get_parent():
  return AnkhBotR2.Managers.PythonManager()

# +--------------------+
# |  RUN IN UI THREAD  |
# +--------------------+
def _run_in_ui_thread(f):
  AnkhBotR2.App.Current.Dispatcher.Invoke(System.Action(f))

def set_clipboard(text):
  _run_in_ui_thread(lambda: System.Windows.Forms.Clipboard.SetText(str(text)))  

def change_main_window_title(title):
  def ui_change_main_window_title():
    AnkhBotR2.App.Current.MainWindow.Title = title
  _run_in_ui_thread(ui_change_main_window_title)

def add_browser_tab(icon_string, tab_title, url):
  def ui_add_browser_tab():
    clr.AddReferenceToFile('CefSharp.Wpf.dll')
    from CefSharp.Wpf import ChromiumWebBrowser
    browser = ChromiumWebBrowser()
    browser.Address = url

    mynewtab = clone(AnkhBotR2.App.Current.MainWindow.Content.Children[0].Items[0])
    mynewtab.IconTxt = icon_string
    mynewtab.Header = tab_title
    mynewtab.Content = mynewtab.Content.GetType()()
    mynewtab.Content.Children.Add(browser)
    AnkhBotR2.App.Current.MainWindow.Content.Children[0].Items.Add(mynewtab)
  _run_in_ui_thread(ui_add_browser_tab)


def add_command(
  command, response,
  group = "GENERAL",
  perms = "Everyone",
  cooldown = 0,
  user_cooldown = 0,
  cost = 0
):
  def ui_add_command():
    # NEeds invocation from AnkhBotR2.App.Current.Dispatcher.Invoke
    VM_CommandAddEdit = AnkhBotR2.ViewModel.VM_CommandAddEdit

    cmd_add_eddit = VM_CommandAddEdit()
    cmd_add_eddit.Command = command
    cmd_add_eddit.Response = response
    cmd_add_eddit.Group = group
    cmd_add_eddit.Permission = perms
    cmd_add_eddit.Cooldown = cooldown
    cmd_add_eddit.UserCooldown = user_cooldown
    cmd_add_eddit.Cost = str(cost)

    cmd_add_eddit.Submit.Execute(None)
    #cmd_add_eddit.Submit.Execute(cmd_add_eddit)
    del cmd_add_eddit
  _run_in_ui_thread(ui_add_command)

def clone(c):
  from System.ComponentModel import *
  cNew = (c.GetType())()
  pdc = TypeDescriptor.GetProperties(c)
  for entry in pdc:
    val = entry.GetValue(c)
    try:
      entry.SetValue(cNew, val)
    except:
      continue
  return cNew


# +------------------------+
# |  Reflection functions  |
# +------------------------+

def get_all_properties_from_type(t,non_public=False):
  if non_public:
    return t.GetProperties(BindingFlags.Instance | BindingFlags.NonPublic)
  else:
    return t.GetProperties()

def get_all_fields_from_type(t,non_public=False):
  if non_public:
    return t.GetFields(BindingFlags.Instance | BindingFlags.NonPublic)
  else:
    return t.GetFields()