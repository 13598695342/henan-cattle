# 河南牛价数据 PWA

## 全自动部署设置

### 方案：GitHub → Netlify 自动部署

1. **设置 GitHub Actions 自动更新数据**
2. **Netlify 连接到 GitHub，自动部署**

### 步骤 1: 推送代码到 GitHub

代码已经在 GitHub: https://github.com/13598695342/henan-cattle

### 步骤 2: 在 Netlify 设置自动部署

1. 打开 https://app.netlify.com/sites/dulcet-daifuku-4f5ffe/settings
2. 找到 **Build & Deploy**
3. **Continuous deployment** → **Build hooks**
4. 点击 **Add build hook**
5. 名称: `auto-deploy`
6. 选择分支: `master`
7. 保存

### 步骤 3: 在 GitHub 设置定时更新

1. 打开 https://github.com/13598695342/henan-cattle/actions
2. 点击 **New workflow**
3. 选择 **set up a workflow yourself**
4. 复制以下内容:

```yaml
name: Update Data and Deploy

on:
  schedule:
    - cron: '0 1 * * 5'  # 每周五9点
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: pip install requests beautifulsoup4
      - run: python data_update.py
      - uses: peter-evans/commit-from@v4
        with:
          commit-message: "自动更新数据 $(date)"
```

5. 点击 **Start commit**

### 步骤 4: 添加 Netlify 构建钩子

1. 复制 Netlify 提供的构建钩子 URL
2. 在 GitHub 仓库 → Settings → Secrets → Actions
3. 添加 `NETLIFY_DEPLOY_HOOK` 密钥

4. 修改 workflow 添加:

```yaml
- name: Trigger Netlify Deploy
  run: curl -X POST -d "" ${{ secrets.NETLIFY_DEPLOY_HOOK }}
```

---

设置完成后，每周五9点会自动：
1. 更新数据
2. 推送到 GitHub
3. Netlify 自动部署
