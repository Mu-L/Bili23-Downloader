import wx
import asyncio
import gettext
from functools import partial

from utils.config import Config
from utils.auth.login_v2 import Login

from utils.common.enums import ParseStatus, ParseType, ExitOption, ProcessingType
from utils.common.exception import GlobalException, show_error_message_dialog
from utils.common.update import Update
from utils.common.thread import Thread
from utils.common.model.download_info import DownloadInfo

from utils.module.ffmpeg.env import FFEnv
from utils.module.clipboard import ClipBoard
from utils.module.pic.cover import Cover

from gui.dialog.misc.about import AboutWindow
from gui.dialog.setting.edit_title import EditTitleDialog
from gui.dialog.download_option.download_option_dialog import DownloadOptionDialog
from gui.dialog.login.login_v2 import LoginDialog
from gui.dialog.search_episode_list import SearchEpisodeListDialog
from gui.dialog.setting.select_batch import SelectBatchDialog
from gui.dialog.guide.guide import GuideDialog
from gui.dialog.confirm.duplicate import DuplicateDialog
from gui.dialog.history import HistoryDialog

from gui.id import ID

from gui.window.debug import DebugWindow
from gui.window.format_factory import FormatFactoryWindow
from gui.window.settings.settings_v2 import SettingWindow
from gui.window.download.download_v4 import DownloadManagerWindow
from gui.window.live_recording import LiveRecordingWindow

from gui.dialog.misc.update import UpdateDialog
from gui.dialog.misc.changelog import ChangeLogDialog
from gui.dialog.misc.processing import ProcessingWindow

_ = gettext.gettext

class Window:
    dialog_show = False

    flag_list: list = []
    
    def show_dialog(func):
        def function(*args, **kwargs):
            rtn = None

            if not Window.dialog_show:
                Window.dialog_show = True

                rtn = func(*args, **kwargs)

            Window.dialog_show = False
            
            return rtn

        return function
    
    def show_frame(func):
        def function(*args, **kwargs):
            frame: wx.Frame = func(*args, **kwargs)

            name = frame.GetName()

            if name in Window.flag_list:
                frame = wx.FindWindowByName(name)

                frame.Raise()

                wx.Bell()
            else:
                frame.Bind(wx.EVT_CLOSE, Window.reset_flag)

                Window.flag_list.append(name)

                frame.Show()

        return function

    @staticmethod
    @show_dialog
    def welcome_dialog(parent: wx.Window):
        def worker():
            dlg = GuideDialog(parent)
            dlg.ShowModal()

        wx.CallAfter(worker)
    
    @staticmethod
    def message_dialog(parent: wx.Window, message: str, caption: str, style: int):
        def worker():
            dlg = wx.MessageDialog(parent, message, caption, style)
            dlg.ShowModal()

        wx.CallAfter(worker)

    @staticmethod
    @show_dialog
    def about_window(parent: wx.Window):
        window = AboutWindow(parent)
        window.ShowModal()

    @staticmethod
    @show_dialog
    def edit_title_dialog(parent: wx.Window, title: str):
        dlg = EditTitleDialog(parent, title)

        if dlg.ShowModal() == wx.ID_OK:
            return dlg.title_box.GetValue() 

    @staticmethod
    @show_dialog
    def download_option_dialog(parent: wx.Window, source: str, init: bool = True):
        dlg = DownloadOptionDialog(parent, source, init)

        if init:
            return dlg.ShowModal()
    
    @staticmethod
    @show_dialog
    def duplicate_dialog(parent: wx.Window, duplicate_episode_list: list = []):
        dlg = DuplicateDialog(parent, duplicate_episode_list)

        return dlg.ShowModal()

    @staticmethod
    @show_dialog
    def login_dialog(parent: wx.Window):
        dlg = LoginDialog(parent)
        dlg.ShowModal()

    @staticmethod
    @show_dialog
    def settings_window(parent: wx.Window):
        window = SettingWindow(parent)
        window.ShowModal()

    @staticmethod
    @show_dialog
    def update_dialog(parent: wx.Window, info: dict):
        dlg = UpdateDialog(parent, info)
        dlg.ShowModal()

    @staticmethod
    @show_dialog
    def changelog_dialog(parent: wx.Window, info: dict):
        dlg = ChangeLogDialog(parent, info)
        dlg.ShowModal()

    @staticmethod
    @show_dialog
    def select_batch_dialog(parent: wx.Window):
        dlg = SelectBatchDialog(parent)
        
        if dlg.ShowModal() == wx.ID_OK:
            return dlg.range_box.GetValue()

    @staticmethod
    @show_frame
    def debug_window(parent: wx.Window):
        return DebugWindow(parent)

    @classmethod
    @show_frame
    def search_dialog(cls, parent: wx.Window):
        return SearchEpisodeListDialog(parent)
    
    @classmethod
    @show_dialog
    def history_dialog(cls, parent: wx.Window):
        dlg = HistoryDialog(parent)
        dlg.ShowModal()

    @staticmethod
    @show_frame
    def format_factory_window(parent: wx.Window):
        return FormatFactoryWindow(parent)

    @classmethod
    def reset_flag(cls, event: wx.CloseEvent):
        frame: wx.Frame = event.GetEventObject()

        cls.flag_list.remove(frame.GetName())

        event.Skip()

    @staticmethod
    def processing_window(show: bool):
        window = wx.FindWindowByName("processing")

        if show:
            wx.CallAfter(window.ShowModal, ProcessingType.Parse)
        else:
            if window.IsShown():
                wx.CallAfter(window.Close)

    @staticmethod
    def create_processing_window(parent: wx.Window):
        return ProcessingWindow(parent)
    
    @staticmethod
    def create_download_window(parent: wx.Window):
        return DownloadManagerWindow(parent)
    
    @staticmethod
    def create_live_window(parent: wx.Window):
        return LiveRecordingWindow(parent)

class TheClipBoard:
    @staticmethod
    def write(text: str):
        ClipBoard.Write(text)

    @classmethod
    def read(cls, event: wx.TimerEvent):
        url: str = ClipBoard.Read()

        if url:
            main_window = Utils.get_main_window()

            if cls.validate_url(url) and cls.check_parse_status():
                main_window.utils.copy_from_menu = False

                main_window.top_box.url_box.SetValue(url)

                wx.CallAfter(main_window.onParseEVT, event, False)

    @staticmethod
    def validate_url(url: str):
        main_window = Utils.get_main_window()

        if url != main_window.url:
            if hasattr(main_window, "parser"):
                if main_window.parser.get_parse_type(url):
                    return True
            
    @staticmethod
    def check_parse_status():
        main_window = Utils.get_main_window()

        if main_window.utils.copy_from_menu:
            return False
        
        if Window.dialog_show:
            return False
        
        if main_window.url_manual:
            return False

        if main_window.IsShown():
            if main_window.utils.status != ParseStatus.Parsing:
                return True

class Async:
    @staticmethod
    async def check_update_async():
        Utils.check_update()

    @staticmethod
    async def check_ffmpeg_async():
        if Config.Merge.ffmpeg_check_available_when_launch:
            Utils.check_ffmpeg()

    @staticmethod
    async def show_user_info_async():
        Utils.show_user_info()

    @classmethod
    async def async_worker(cls):
        tasks = [
            asyncio.create_task(cls.show_user_info_async()),
            asyncio.create_task(cls.check_ffmpeg_async()),
            asyncio.create_task(cls.check_update_async())
        ]

        await asyncio.gather(*tasks, return_exceptions = True)

    @classmethod
    def run(cls):
        asyncio.run(cls.async_worker())

class Utils:
    def __init__(self, parent: wx.Window):
        from gui.window.main.main_v3 import MainWindow

        self.main_window: MainWindow = parent
        self.status = ParseStatus.Success

        self.copy_from_menu = False

    def init_timer(self):
        if Config.Basic.listen_clipboard:
            if not self.main_window.clipboard_timer.IsRunning():
                self.main_window.clipboard_timer.Start(1000)
        else:
            if self.main_window.clipboard_timer.IsRunning():
                self.main_window.clipboard_timer.Stop()

    @classmethod
    def check_update(cls, from_menu: bool = False):
        def onError():
            show_error_message_dialog(_("检查更新失败"), _("当前无法检查更新，请稍候再试。"), cls.get_main_window())

        try:
            info = Update.get_update_json()

            version = info.get("version_code")

            if version > Config.APP.version_code:
                if info.get("force") or version != Config.Misc.ignore_version:
                    wx.CallAfter(Window.update_dialog, cls.get_main_window(), info)
            else:
                if from_menu:
                    Window.message_dialog(cls.get_main_window(), _("当前没有可用的更新。"), _("检查更新"), wx.ICON_INFORMATION)

        except Exception as e:
            raise GlobalException(callback = onError) from e

    def get_changelog(self):
        def onError():
            show_error_message_dialog(_("获取更新日志失败"), _("当前无法获取更新日志，请稍候再试。"), self.main_window)

        try:
            info = Update.get_changelog()

            wx.CallAfter(Window.changelog_dialog, self.main_window, info)

        except Exception as e:
            raise GlobalException(callback = onError) from e

    def user_logout(self):
        def on_error():
            show_error_message_dialog(_("注销登录失败"), _("无法完成注销登录操作"), self.main_window)

        try:
            Login.logout()

            self.show_user_info()

        except Exception as e:
            raise GlobalException(callback = on_error) from e

    def user_refresh(self):
        def on_error():
            show_error_message_dialog(_("刷新登录信息失败"), _("无法刷新登录信息"), self.main_window)

        try:
            Login.refresh()

            self.show_user_info()

        except Exception as e:
            raise GlobalException(callback = on_error) from e

    @classmethod
    def show_user_info(cls):
        main_window = cls.get_main_window()

        if Config.Misc.show_user_info:
            if Config.User.login:
                worker = main_window.bottom_box.show_user_info
            else:
                worker = main_window.bottom_box.set_not_login
        else:
            worker = main_window.bottom_box.hide_user_info

        wx.CallAfter(worker)

    def view_cover(self, url: str):
        Cover.view_cover(self.main_window, url)

    def save_exit_dialog_settings(self, flag: int): 
        save = ExitOption(Config.Basic.exit_option) == ExitOption.AskOnce

        match flag:
            case wx.ID_YES:
                Config.Basic.exit_option = ExitOption.TaskIcon.value

            case wx.ID_NO:
                Config.Basic.exit_option = ExitOption.Exit.value

        if save:
            Config.save_app_config()

    def save_window_params_settings(self):
        if Config.Basic.remember_window_status:
            Config.Basic.window_pos = list(self.main_window.GetPosition())
            Config.Basic.window_size = list(self.main_window.GetSize())
            Config.Basic.window_maximized = self.main_window.IsMaximized()

            Config.save_app_config()

    @classmethod
    def check_ffmpeg(cls):
        def worker():
            dlg = wx.MessageDialog(cls.get_main_window(), _("未检测到 FFmpeg\n\n未检测到 FFmpeg，无法进行视频合并、截取和转换。\n\n请检查是否为 FFmpeg 创建环境变量或 FFmpeg 是否已在运行目录中。"), _("警告"), wx.ICON_WARNING | wx.YES_NO)
            dlg.SetYesNoLabels(_("安装 FFmpeg"), _("忽略"))

            if dlg.ShowModal() == wx.ID_YES:
                wx.LaunchDefaultBrowser("https://bili23.scott-sloan.cn/doc/install/ffmpeg.html")

        result = FFEnv.check_availability()

        if result:
            wx.CallAfter(worker)

    def set_status(self, status: ParseStatus):
        wx.CallAfter(self.set_status_worker, status)

    def set_status_worker(self, status: ParseStatus):
        def set_type_lab(enable: bool, label: str):
            self.main_window.top_box.processing_icon.Show(enable)
            self.main_window.top_box.type_lab.SetLabel(label)

        def enable_url_box(enable: bool):
            self.main_window.top_box.url_box.Enable(enable)
            self.main_window.top_box.get_btn.Enable(enable)

            self.main_window.episode_list.Enable(enable)
            
        def enable_buttons(download: bool, episode: bool, option: bool, graph: bool):
            self.main_window.bottom_box.download_btn.Enable(download)

            self.main_window.top_box.episode_option_btn.Enable(episode)
            self.main_window.top_box.download_option_btn.Enable(option)

            self.main_window.top_box.graph_btn.Show(graph)

        def get_episode_enable():
            match self.main_window.parser.parse_type:
                case ParseType.Video:
                    return not self.main_window.parser.parser.is_interactive_video()

                case ParseType.Bangumi | ParseType.Cheese | ParseType.List:
                    return True
                
                case _:
                    return False
                
        self.status = status

        match status:
            case ParseStatus.Parsing:
                set_type_lab(True, _("正在解析中"))

                enable_url_box(True)
                enable_buttons(download = False, episode = False, option = False, graph = False)

                Window.processing_window(show = True)
                
            case ParseStatus.Success:
                set_type_lab(False, "")

                is_interactive = self.main_window.parser.parser.is_interactive_video()
                not_live = self.main_window.parser.parse_type != ParseType.Live

                enable_url_box(True)
                enable_buttons(download = not_live, episode = get_episode_enable(), option = not_live, graph = is_interactive)

                Window.processing_window(show = False)

            case ParseStatus.Error:
                set_type_lab(False, "")

                enable_url_box(True)
                enable_buttons(download = False, episode = False, option = False, graph = False)

                Window.processing_window(show = False)

        self.main_window.panel.Layout()

    @staticmethod
    def get_main_window():
        from gui.window.main.main_v3 import MainWindow

        main_window: MainWindow = wx.FindWindowByName("main")

        return main_window
    
    def download(self):
        def add_to_list_callback():
            Window.processing_window(show = False)

            self.main_window.onShowDownloadWindowEVT()    

        def detail_mode_callback(episode_info_list: list[dict]):
            for entry in episode_info_list:
                self.main_window.episode_list.download_task_info_list.extend(DownloadInfo.get_download_info(entry))

            Thread(target = self.main_window.download_window.add_to_download_list, args = (self.main_window.episode_list.download_task_info_list, add_to_list_callback, True, True)).start()

        if self.main_window.parser.parse_type in [ParseType.FavList, ParseType.Space]:
            video_info_to_parse = self.main_window.episode_list.GetAllCheckedItemEx()

            if self.check_duplicate():
                return

            Thread(target = self.main_window.parser.parser.parse_video_info, args = (video_info_to_parse, detail_mode_callback)).start()
        else:
            self.main_window.episode_list.GetAllCheckedItem()

            if self.check_duplicate():
                return

            Thread(target = self.main_window.download_window.add_to_download_list, args = (self.main_window.episode_list.download_task_info_list, add_to_list_callback, True, True)).start()

    def check_duplicate(self):
        duplicate_task_list = self.main_window.download_window.find_duplicate_task(self.main_window.episode_list.download_task_info_list)

        Window.processing_window(show = False)

        if duplicate_task_list:
            if Window.duplicate_dialog(self.main_window, duplicate_task_list) != wx.ID_OK:
                return True
            else:
                if Config.Temp.duplicate_option == 0:
                    self.main_window.episode_list.download_task_info_list = self.main_window.download_window.remove_duplicate_task(self.main_window.episode_list.download_task_info_list, [entry.hash_id for entry in duplicate_task_list])

        Window.processing_window(show = True)

    def update_history(self):
        history = self.main_window.parser.main_window.history.get()

        history_menu = wx.Menu()

        if history:
            for entry in history[-10:]:
                url = entry.get("url")

                item = history_menu.Append(wx.ID_ANY, url)
                self.main_window.Bind(wx.EVT_MENU, partial(self.main_window.onHistoryMenuItemEVT, url = url), item)
        else:
            history_menu.Append(ID.HISTORY_EMPTY, _("无记录"))
            history_menu.Enable(ID.HISTORY_EMPTY, False)

        history_menu.AppendSeparator()
        history_menu.Append(ID.HISTORY_MORE, _("更多..."))
        history_menu.AppendSeparator()
        history_menu.Append(ID.HISTORY_CLEAR, _("清除历史记录..."))

        menu_bar: wx.MenuBar = self.main_window.GetMenuBar()
        menu_bar.Replace(1, history_menu, _("历史(&S)"))
