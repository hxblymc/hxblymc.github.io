# 摄影作品集网站 · 使用说明

极简白底画廊。**日常更新只需一件事:往 `photos/` 文件夹丢图,推送后网站 1-2 分钟自动更新**(缩略图、排版、分类全部自动生成)。

## 文件结构

```
photo-portfolio/
├── index.html        网站页面(一般不用动)
├── site.json         你的名字、简介、联系方式 ← 先改这个
├── photos/           照片放这里,子文件夹名 = 分类名
│   ├── 风光/
│   └── 街头/
├── build.py          自动构建脚本(不用动,云端自动运行)
├── thumbs/ photos.js 自动生成的缩略图和清单(不用动)
└── .github/          自动部署配置(不用动)
```

当前 `photos/` 里是 8 张灰色示例图,**替换成你的照片即可**。

## 第一次上线(约 15 分钟,全程免费)

1. 注册 [GitHub](https://github.com) 账号。
2. 登录后点右上角 **+** → **New repository**:
   - Repository name 填 `photo`(或任意英文名);想要更短的网址可填 `你的用户名.github.io`
   - 选 **Public**(免费版 Pages 要求公开)
   - 点 **Create repository**
3. 安装 [GitHub Desktop](https://desktop.github.com)(中文界面,免命令行),登录你的账号。
4. GitHub Desktop 里:**Clone repository** → 选刚建的仓库 → 记住克隆到本地的文件夹位置。
5. 把本项目的**全部文件**(包括 `.github` 文件夹)复制进那个本地文件夹。
6. 回到 GitHub Desktop,左下角 Summary 随便填(如"首次上传"),点 **Commit to main** → 点 **Push origin**。
7. 打开 github.com 上的仓库页面 → **Settings** → 左栏 **Pages** → Build and deployment 的 Source 选 **GitHub Actions**。
8. 等 1-2 分钟(仓库页面 Actions 标签里能看进度),访问:
   - `https://你的用户名.github.io/仓库名/`
   - (若仓库名是 `用户名.github.io`,网址就是 `https://用户名.github.io`)

## 日常更新照片

1. 把照片拖进本地文件夹的 `photos/分类名/` 里(删图同理,直接删文件)。
2. 打开 GitHub Desktop → Commit → Push。
3. 完事,1-2 分钟后网站自动更新。

手机或临时电脑上也可以:仓库页面 → 进入 `photos/` 的分类文件夹 → **Add file → Upload files** → 拖入照片 → Commit。

## 照片规则

- **子文件夹名 = 网站导航里的分类名**(中文没问题)。新建分类 = 在 `photos/` 里新建文件夹放图。
- 直接放在 `photos/` 根目录的图只出现在"全部"里。
- 支持 JPG / PNG / WebP,**不支持 HEIC**(iPhone 照片请导出为 JPG)。
- 排序:按拍摄时间(EXIF)从新到旧;无拍摄信息则按文件名。
- 文件名会成为灯箱里的图片标题(如 `海平线.jpg` 显示"海平线");相机默认名(`DSC_0001` 等)自动隐藏。
- 建议导出:JPG、长边 2000-3500px、单张 5MB 以内。仓库总容量建议 1GB 以内(约几百张)。
- 注意:照片在 Public 仓库中公开可见(作品集本身就是公开的,但别放私密图)。

## 修改个人信息

编辑 `site.json`(推送后生效):

```json
{
  "name": "你的名字",              ← 网站大标题
  "tagline": "Photographer",      ← 副标题
  "email": "you@example.com",     ← 页脚邮箱,留空 "" 则不显示
  "instagram": "",                ← 填 Instagram 用户名
  "weibo": "",                    ← 填微博主页完整网址
  "category_order": ["风光","街头"] ← 分类显示顺序,留空 [] 按拼音排
}
```

## 本地预览(可选)

双击 `index.html` 即可在浏览器看效果。刚加的新照片要在本地立即看到,需装 Python 后运行 `pip install Pillow` 和 `python build.py`;不装也没关系,推送后云端会自动构建。

## 进阶(可选)

- **自定义域名**:买一个域名(约 ¥60/年),仓库 Settings → Pages → Custom domain 绑定,再在域名商处加一条 CNAME 记录指向 `你的用户名.github.io`。
- **国内访问加速**:github.io 在大陆偶尔慢。可在 [Cloudflare Pages](https://pages.cloudflare.com) 免费绑定同一个 GitHub 仓库,构建命令填 `pip install Pillow && python build.py`,输出目录填 `/`,再配自定义域名,国内访问会明显改善。

## 常见问题

- **推送后网站没更新**:看仓库 Actions 标签,绿勾 = 成功(再强刷浏览器 Ctrl+F5);红叉 = 点进去看哪步报错。
- **某张图没显示**:多半是 HEIC 或损坏文件,构建日志里会写"跳过"。
- **404**:确认第 7 步 Pages 的 Source 已选 GitHub Actions,且网址包含仓库名。
