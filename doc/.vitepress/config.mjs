import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  lang: 'zh-CN',
  title: "Bili23 Downloader",
  description: "一个 B 站视频下载工具",
  lastUpdated: true,
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      {
        text: '首页',
        link: '/'
      },
      {
        text: '文档',
        link: '/doc/waht-is-bili23-downloader'
      },
      {
        text: '博客',
        link: 'https://www.scott-sloan.cn'
      }
    ],

    sidebar: [
      {
        text: '简介',
        items: [
          {
            text: '什么是 Bili23 Downloader？',
            link: '/doc/waht-is-bili23-downloader'
          }
        ]
      },
      {
        text: '安装',
        collapsed: true,
        items: [
          {
            text: '安装程序',
            link: '/doc/install/main'
          },
          {
            text: '安装 FFmpeg',
            link: '/doc/install/ffmpeg'
          }
        ]
      },
      {
        text: '使用',
        collapsed: true,
        items: [
          {
            text: '基础使用',
            link: '/doc/use/basic'
          },
          {
            text: '支持的链接',
            link: '/doc/use/url'
          },
          {
            text: '进阶使用',
            link: '/doc/use/advanced'
          },
          {
            text: '更新程序',
            link: '/doc/use/update'
          }
        ]
      },
      {
        text: '常见问题',
        collapsed: true,
        items: [
          {
            text: '运行相关',
            link: '/doc/faq/run'
          },
          {
            text: '下载相关',
            link: '/doc/faq/download'
          }
        ]
      },
      {
        text: '免责声明',
        link: '/doc/announcement'
      },
      {
        text: '开源许可',
        link: '/doc/license'
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/ScottSloan/Bili23-Downloader' }
    ],

    search: {
      provider: 'local',
      options: {
        translations: {
          button: {
            buttonText: '搜索文档',
            buttonAriaLabel: '搜索文档'
          },
          modal: {
            searchBoxPlaceholder: '搜索文档',
            displayDetails: '显示详情',
            backButtonTitle: '后退',
            resetButtonTitle: '清除查询条件',
            footer: {
              selectText: '选择',
              closeText: '关闭',
              navigateText: '导航'
            }
          }
        }
      }
    },

    docFooter: {
      prev: '上一页',
      next: '下一页'
    },

    lastUpdated: {
      text: '最后更新于',
      formatOptions: {
        dateStyle: 'short',
        timeStyle: 'medium'
      }
    },
    
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '菜单',
    outlineTitle: '页面导航'
  }
})
