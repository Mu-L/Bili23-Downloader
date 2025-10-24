import wx
import gettext

from utils.config import Config
from utils.common.style.icon_v4 import Icon, IconID, IconSize
from utils.common.enums import EpisodeDisplayType
from utils.module.web.page import WebPage

from gui.window.main.utils import Window

from gui.component.text_ctrl.search_ctrl import SearchCtrl
from gui.component.button.flat_button import FlatButton
from gui.component.button.bitmap_button import BitmapButton
from gui.component.panel.panel import Panel
from gui.component.staticbitmap.staticbitmap import StaticBitmap

from gui.component.menu.url import URLMenu
from gui.component.menu.episode_option import EpisodeOptionMenu

_ = gettext.gettext

class TopBox(Panel):
    def __init__(self, parent: wx.Window):
        from gui.window.main.main_v3 import MainWindow

        self.main_window: MainWindow = wx.FindWindowByName("main")

        Panel.__init__(self, parent)

        self.init_UI()

        self.Bind_EVT()

    def init_UI(self):
        url_lab = wx.StaticText(self, -1, _("链接"))
        self.url_box = SearchCtrl(self, _("在此处粘贴链接进行解析"), search_btn = True, clear_btn = True)
        self.url_box.SetMenu(URLMenu())

        self.get_btn = wx.Button(self, -1, "Get")

        url_hbox = wx.BoxSizer(wx.HORIZONTAL)
        url_hbox.Add(url_lab, 0, wx.ALL & (~wx.BOTTOM) | wx.ALIGN_CENTER, self.FromDIP(6))
        url_hbox.Add(self.url_box, 1, wx.ALL & (~wx.LEFT) & (~wx.BOTTOM) | wx.EXPAND, self.FromDIP(6))
        url_hbox.Add(self.get_btn, 0, wx.ALL & (~wx.LEFT) & (~wx.BOTTOM) | wx.ALIGN_CENTER, self.FromDIP(6))

        self.processing_icon = StaticBitmap(self, bmp = Icon.get_icon_bitmap(IconID.Loading), size = self.FromDIP((16, 16)))
        self.processing_icon.Hide()
        self.type_lab = wx.StaticText(self, -1, "")
        self.graph_btn = FlatButton(self, _("剧情树"), IconID.Tree_Structure, split = True)
        self.graph_btn.setToolTip(_("查看互动视频剧情树"))
        self.graph_btn.Hide()
        self.search_btn = BitmapButton(self, Icon.get_icon_bitmap(IconID.Search, icon_size = IconSize.SMALL_EX), tooltip = _("搜索剧集列表"))
        self.episode_option_btn = BitmapButton(self, Icon.get_icon_bitmap(IconID.List, icon_size = IconSize.SMALL_EX), enable = False, tooltip = _("剧集列表显示设置"))
        self.download_option_btn = BitmapButton(self, Icon.get_icon_bitmap(IconID.Setting, icon_size = IconSize.SMALL_EX), enable = False, tooltip = _("下载选项"))

        info_hbox = wx.BoxSizer(wx.HORIZONTAL)
        info_hbox.Add(self.processing_icon, 0, wx.ALL & (~wx.RIGHT) | wx.ALIGN_CENTER, self.FromDIP(6))
        info_hbox.Add(self.type_lab, 0, wx.ALL | wx.ALIGN_CENTER, self.FromDIP(6))
        info_hbox.AddSpacer(self.FromDIP(6))
        info_hbox.Add(self.graph_btn, 0, wx.EXPAND, self.FromDIP(6))
        info_hbox.AddStretchSpacer()
        info_hbox.Add(self.search_btn, 0, wx.ALL | wx.ALIGN_CENTER, self.FromDIP(6))
        info_hbox.Add(self.episode_option_btn, 0, wx.ALL & (~wx.LEFT) | wx.ALIGN_CENTER, self.FromDIP(6))
        info_hbox.Add(self.download_option_btn, 0, wx.ALL & (~wx.LEFT) | wx.ALIGN_CENTER, self.FromDIP(6))

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(url_hbox, 0, wx.EXPAND)
        vbox.Add(info_hbox, 0, wx.EXPAND)

        self.SetSizer(vbox)

    def Bind_EVT(self):
        self.search_btn.Bind(wx.EVT_BUTTON, self.onShowSearchDialogEVT)
        self.episode_option_btn.Bind(wx.EVT_BUTTON, self.onShowEpisodeOptionMenuEVT)
        self.download_option_btn.Bind(wx.EVT_BUTTON, self.onShowDownloadOptionDialogEVT)

        self.url_box.Bind(wx.EVT_KEY_DOWN, self.onSearchKeyDownEVT)

        self.graph_btn.onClickCustomEVT = self.onShowGraphWindowEVT

    def onShowSearchDialogEVT(self, event: wx.CommandEvent):
        Window.search_dialog(self.main_window)

    def onShowEpisodeOptionMenuEVT(self, event: wx.CommandEvent):
        menu = EpisodeOptionMenu(self.main_window.parser.parser.is_in_section_option_enable())

        self.PopupMenu(menu)

    def onShowDownloadOptionDialogEVT(self, event: wx.CommandEvent, source: str = "menu", init: bool = True):
        return Window.download_option_dialog(self.main_window, source, init)
    
    def onSearchKeyDownEVT(self, event: wx.KeyEvent):
        keycode = event.GetKeyCode()

        if keycode in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
            self.main_window.onParseEVT(event)
                    
        event.Skip()

    def onShowGraphWindowEVT(self):
        WebPage.show_webpage(self.main_window, "graph.html")

    def update_checked_item_count(self, count: int):
        if count:
            label = _("(共 %s 项，已选择 %s 项)") % (self.main_window.episode_list.count, count)
        else:
            label = _("(共 %s 项)") % self.main_window.episode_list.count

        self.type_lab.SetLabel(f"{self.main_window.parser.parse_type_str} {label}")

        self.Layout()

    def set_episode_full_name(self):
        Config.Misc.show_episode_full_name = not Config.Misc.show_episode_full_name

        self.main_window.show_episode_list()

    def set_episode_display_mode(self, mode: EpisodeDisplayType):
        Config.Misc.episode_display_mode = mode.value

        self.main_window.show_episode_list()

    def check_url(self):
        url = self.url_box.GetValue()

        if not url:
            Window.message_dialog(self.main_window, _("解析失败\n\n链接不能为空"), _("警告"), wx.ICON_WARNING)
            return True

    def reset_search_window(self):
        if search_dialog := wx.FindWindowByName("search"):
            search_dialog.reset()

    def show_download_option_dialog(self, parent: wx.Window):
        if Config.Basic.auto_popup_option_dialog:
            if self.onShowDownloadOptionDialogEVT(0, "main", True) != wx.ID_OK:
                return True
        else:
            self.onShowDownloadOptionDialogEVT(0, "main", False)