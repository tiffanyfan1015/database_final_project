# Database Final Project - Backend API Server with mysql 
## Environment

Ubuntu 22.04
mysql  Ver 8.0.37-0ubuntu0.23.10.2 for Linux on aarch64 ((Ubuntu))

## Step
1. Create database and table.
2. Download flask
    * `sudo apt update`
    * `sudo apt install python3-flask`
3. Check whether flask is downloaded
    * `python3 -m flask --version`
4. Run app by  
    *  `python3 app.py`
    or
    * `export FLASK_APP=app.py` then `flask run `

The app will be run on http://127.0.0.1:5000 by default.

## 一些開發規範
* 記得開新 branch 再發PR，讓其他人去 merge。不要直接推到`main`
* 記得寫 commit message
* 記得定期更新到最新版
    * 更新到最新後開始新 branch
        * Step 1. 確認到 main branch 中 
            * `git checkout master` 
            * `git pull`
        * Step 2. 開新的 branch 
            * `git branch feature/<newFeature>` 
            * `git checkout feature/<newFeature>`
        * Step 3. 開發好新功能
            * `git add .`
            * `git commit -am "<commitMessage>"`
            * `git rebase --continue`
            * `git push origin feature-branch`*# 如果是新分支*
            * `git push -f origin feature-branch`*# 如果分支已存在（因為rebase後需要強制推送）*
        * Step 4. 到 Github 發送 PR
    * 單純更新到最新
        * Step 1. 確認到主支把 repo 的抓下來
            * `git checkout main` 
            * `git pull`
        * Step 2. 切回我自己的 branch 
            * `git checkout feature/<newFeature>`
        * Step 3. 把 master 合併到我自己的 branch
            * `git merge main`
        * Step 4. 修 conflict（如果有的話）