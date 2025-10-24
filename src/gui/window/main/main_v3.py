import wx
import gettext

from utils.config import Config

from utils.common.enums import Platform, EpisodeDisplayType, ExitOption
from utils.common.thread import Thread
from utils.common.exception import GlobalException
from utils.common.style.font import SysFont

from gui.component.window.frame import Frame
from gui.component.panel.panel import Panel

from gui.id import ID

from gui.window.main.parser import Parser
from gui.window.main.utils import Utils, Window, TheClipBoard, Async
from gui.window.main.top_box import TopBox
from gui.window.main.bottom_box import BottomBox

from gui.component.misc.taskbar_icon import TaskBarIcon
from gui.component.tree_list_v2 import TreeListCtrl

_ = gettext.gettext

class MainWindow(Frame):
    def __init__(self, parent: wx.Window):
        self.url, self.url_manual = None, False
        self.search_keywords = ""

        self.utils = Utils(self)

        Frame.__init__(self, parent, Config.APP.name, style = self.get_window_style(), name = "main")

        self.set_window_params()

        self.get_sys_settings()

        self.init_UI()

        self.Bind_EVT()

        self.init_utils()

    def init_UI(self):
        self.panel = Panel(self)

        self.top_box = TopBox(self.panel)

        self.episode_list = TreeListCtrl(self.panel)

        self.bottom_box = BottomBox(self.panel)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.top_box, 0, wx.EXPAND)
        vbox.Add(self.episode_list, 1, wx.ALL & (~wx.TOP) & (~wx.BOTTOM) | wx.EXPAND, self.FromDIP(6))
        vbox.Add(self.bottom_box, 0, wx.EXPAND)

        self.panel.SetSizer(vbox)

        self.init_menubar()

        self.clipboard_timer = wx.Timer(self, -1)

        self.taskbar_icon = TaskBarIcon()

    def init_menubar(self):
        menu_bar = wx.MenuBar()

        tool_menu = wx.Menu()
        help_menu = wx.Menu()

        if Config.User.login:
            tool_menu.Append(ID.LOGOUT_MENU, _("注销(&L)"))
        else:
            tool_menu.Append(ID.LOGIN_MENU, _("登录(&L)"))

        tool_menu.AppendSeparator()

        if Config.Misc.enable_debug:
            tool_menu.Append(ID.DEBUG_MENU, _("调试(&D)"))

        tool_menu.Append(ID.LIVE_RECORDING_MENU, _("直播录制(&R)"))
        tool_menu.Append(ID.FORMAT_FACTORY_MENU, _("视频工具箱(&F)"))
        tool_menu.AppendSeparator()
        tool_menu.Append(ID.SETTINGS_MENU, _("设置(&S)"))

        help_menu.Append(ID.CHECK_UPDATE_MENU, _("检查更新(&U)"))
        help_menu.Append(ID.CHANGELOG_MENU, _("更新日志(&P)"))
        help_menu.AppendSeparator()
        help_menu.Append(ID.HELP_MENU, _("使用帮助(&C)"))
        help_menu.AppendSeparator()
        help_menu.Append(ID.FEEDBACK_MENU, _("报告问题(&B)"))
        help_menu.Append(ID.COMMUNITY_MENU, _("社区交流(&G)"))
        help_menu.AppendSeparator()
        help_menu.Append(ID.ABOUT_MENU, _("关于(&A)"))

        menu_bar.Append(tool_menu, _("工具(&T)"))
        menu_bar.Append(help_menu, _("帮助(&H)"))

        self.SetMenuBar(menu_bar)

    def Bind_EVT(self):
        self.Bind(wx.EVT_MENU, self.onMenuEVT)
        self.Bind(wx.EVT_CLOSE, self.onCloseEVT)
        
        self.top_box.get_btn.Bind(wx.EVT_BUTTON, self.onParseEVT)

        self.bottom_box.download_mgr_btn.Bind(wx.EVT_BUTTON, self.onShowDownloadWindowEVT)
        self.bottom_box.download_btn.Bind(wx.EVT_BUTTON, self.onDownloadEVT)

        self.episode_list.Bind(wx.EVT_MENU, self.onEpisodeListContextMenuEVT)

        self.Bind(wx.EVT_TIMER, TheClipBoard.read, self.clipboard_timer)

    def init_utils(self):
        def worker():
            Async.run()

            if Config.Basic.is_new_user:
                Window.welcome_dialog(self)

        self.parser = Parser(self)

        self.processing_window = Window.create_processing_window(self)
        self.download_window = Window.create_download_window(self)
        self.live_recording_window = Window.create_live_window(self)

        self.utils.init_timer()

        Thread(target = worker).start()

    def onMenuEVT(self, event: wx.MenuEvent):
        match event.GetId():
            case ID.LOGIN_MENU:
                Window.login_dialog(self)

            case ID.LOGOUT_MENU:
                dlg = wx.MessageDialog(self, _("退出登录\n\n是否要退出登录？"), _("警告"), wx.ICON_WARNING | wx.YES_NO)

                if dlg.ShowModal() == wx.ID_YES:
                    self.utils.user_logout()

            case ID.REFRESH_MENU:
                Thread(target = self.utils.user_refresh).start()

            case ID.DEBUG_MENU:
                Window.debug_window(self)

            case ID.LIVE_RECORDING_MENU:
                self.onShowLiveRecordingWindowEVT(event)

            case ID.FORMAT_FACTORY_MENU:
                wx.MessageDialog(self, _("不可用\n\n当前不可用，请等待后续版本更新。"), _("提示"), wx.ICON_INFORMATION).ShowModal()

                #Window.format_factory_window(self)

            case ID.SETTINGS_MENU:
                Window.settings_window(self)

            case ID.CHECK_UPDATE_MENU:
                Thread(target = self.utils.check_update, args = (True,)).start()

            case ID.CHANGELOG_MENU:
                Thread(target = self.utils.get_changelog).start()

            case ID.HELP_MENU:
                wx.LaunchDefaultBrowser("https://bili23.scott-sloan.cn/doc/use/basic.html")

            case ID.FEEDBACK_MENU:
                wx.LaunchDefaultBrowser("https://github.com/ScottSloan/Bili23-Downloader/issues")

            case ID.COMMUNITY_MENU:
                wx.LaunchDefaultBrowser("https://bili23.scott-sloan.cn/doc/community.html")

            case ID.SUPPORTTED_URL_MENU:
                wx.LaunchDefaultBrowser("https://bili23.scott-sloan.cn/doc/use/url.html")

            case ID.ABOUT_MENU:
                Window.about_window(self)

            case ID.EPISODE_SINGLE_MENU:
                self.top_box.set_episode_display_mode(EpisodeDisplayType.Single)

            case ID.EPISODE_IN_SECTION_MENU:
                self.top_box.set_episode_display_mode(EpisodeDisplayType.In_Section)

            case ID.EPISODE_ALL_SECTIONS_MENU:
                self.top_box.set_episode_display_mode(EpisodeDisplayType.All)
                
            case ID.EPISODE_FULL_NAME_MENU:
                self.top_box.set_episode_full_name()

    def onCloseEVT(self, event: wx.CloseEvent):
        def show_exit_dialog():
            dlg = wx.MessageDialog(self, _("退出程序\n\n确定要退出程序吗？"), _("提示"), style = wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL)
            dlg.SetYesNoCancelLabels(_("最小化到托盘"), _("退出程序"), _("取消"))

            return dlg.ShowModal()
        
        if ExitOption(Config.Basic.exit_option) in [ExitOption.Ask, ExitOption.AskOnce]:
            flag = show_exit_dialog()

            if flag == wx.ID_CANCEL:
                return
        
            self.utils.save_exit_dialog_settings(flag)

        self.utils.save_window_params_settings()

        match ExitOption(Config.Basic.exit_option):
            case ExitOption.TaskIcon:
                self.Hide()
                return
            
            case ExitOption.Exit:
                self.clipboard_timer.Stop()
                self.taskbar_icon.Destroy()

                event.Skip()

    def onShowDownloadWindowEVT(self, event: wx.CommandEvent = None):
        if not event and not Config.Basic.auto_show_download_window:
            return

        if not self.download_window.IsShown():
            self.download_window.Show()
        
        elif self.download_window.IsIconized():
            if Config.Basic.auto_show_download_window:
                self.download_window.Iconize(False)
        
        self.download_window.Raise()

    def onShowLiveRecordingWindowEVT(self, event: wx.CommandEvent):
        if not self.live_recording_window.IsShown():
            self.live_recording_window.Show()

        elif self.live_recording_window.IsIconized():
            self.Iconize(False)

        self.live_recording_window.Raise()

    def onDownloadEVT(self, event: wx.CommandEvent):
        try:
            if self.episode_list.check_download_items():
                return
            
            if self.top_box.show_download_option_dialog(self):
                return

            self.bottom_box.download_tip()

            self.utils.download()

        except Exception as e:
            raise GlobalException(callback = self.parser.onError) from e
        
    def onParseEVT(self, event: wx.CommandEvent, url_manual = True):
        url = self.top_box.url_box.GetValue()

        if self.top_box.check_url():
            return

        self.episode_list.init_episode_list()

        Thread(target = self.parser.parse_url, args = (url, )).start()

        self.url = url
        self.url_manual = url_manual

        self.top_box.reset_search_window()

    def onEpisodeListContextMenuEVT(self, event: wx.MenuEvent):
        match event.GetId():
            case ID.EPISODE_LIST_VIEW_COVER_MENU:
                item_data = self.episode_list.GetItemData(self.episode_list.GetSelection())

                if item_data.cover_url:
                    self.utils.view_cover(item_data.cover_url)
                
            case ID.EPISODE_LIST_COPY_TITLE_MENU:
                TheClipBoard.write(self.episode_list.GetItemTitle())

            case ID.EPISODE_LIST_COPY_URL_MENU:
                self.utils.copy_from_menu = True

                item_data = self.episode_list.GetItemData(self.episode_list.GetSelection())

                TheClipBoard.write(item_data.link)

            case ID.EPISODE_LIST_OPEN_IN_BROWSER_MENU:
                item_data = self.episode_list.GetItemData(self.episode_list.GetSelection())

                wx.LaunchDefaultBrowser(item_data.link)

            case ID.EPISODE_LIST_EDIT_TITLE_MENU:
                item = self.episode_list.GetSelection()

                if (title := Window.edit_title_dialog(self, self.episode_list.GetItemTitle())):
                    self.episode_list.SetItemTitle(item, title)

            case ID.EPISODE_LIST_CHECK_MENU:
                self.episode_list.CheckCurrentItem()

            case ID.EPISODE_LIST_COLLAPSE_MENU:
                self.episode_list.CollapseCurrentItem()

            case ID.EPISODE_LIST_SELECT_BATCH_MENU:
                Window.select_batch_dialog(self)

            case ID.EPISODE_LIST_REFRESH_MEDIA_INFO_MENU:
                item_data = self.episode_list.GetItemData(self.episode_list.GetSelection())

                self.parser.refresh_media_info(item_data)

    def show_episode_list(self, from_menu: bool = True):
        if from_menu:
            self.parser.parse_episode()

        self.episode_list.show_episode_list()

        if Config.Misc.auto_check_episode_item or self.episode_list.count == 1:
            self.episode_list.CheckAllItems()

        self.top_box.update_checked_item_count(self.episode_list.GetCheckedItemCount())

        self.top_box.url_box.SelectNone()

    def set_window_params(self):
        match Platform(Config.Sys.platform):
            case Platform.Windows | Platform.macOS:
                self.SetSize(self.FromDIP((800, 450)))

            case Platform.Linux:
                self.SetSize(self.FromDIP((1000, 550)))
        
        self.CenterOnParent()

        if Config.Basic.remember_window_status:
            if Config.Basic.window_maximized:
                self.Maximize()
            else:
                if Config.Basic.window_size:
                    self.SetSize(Config.Basic.window_size)
                
                if Config.Basic.window_pos:
                    self.SetPosition(Config.Basic.window_pos)

    def get_window_style(self):
        style = wx.DEFAULT_FRAME_STYLE

        if Config.Basic.always_on_top:
            style |= wx.STAY_ON_TOP

        return style

    def get_sys_settings(self):
        Config.Sys.dark_mode = False if Platform(Config.Sys.platform) == Platform.Windows else wx.SystemSettings.GetAppearance().IsDark()
        Config.Sys.dpi_scale_factor = self.GetDPIScaleFactor()
        Config.Sys.default_font = self.GetFont().GetFaceName()

        SysFont.sys_font_list = sorted(wx.FontEnumerator().GetFacenames())