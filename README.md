# [ccPartner](https://ccpartner.herokuapp.com/)
本專案使用Django框架建置具會員系統、專案管理、團隊申請、站內訊息等功能的網站，希望能輔助讀書會學員專案媒合使用。
<br />
<br />

## Authentication & Authorization

* 專案部署於Heroku為公開網站，任何使用者可看到讀書會學員名片的首頁瀏覽頁面
* 需通過註冊會員才可具有專案管理(Project)、站內訊息(Inbox)功能的權限
* 若為專案的建立者則額外具有審核團隊人員申請加入與離開(Apply)的權限

<div>
    <img src="https://user-images.githubusercontent.com/69707312/149081604-50142ac5-edcf-413f-8a92-3f30f68545aa.png" height="250"/> <img src="https://user-images.githubusercontent.com/69707312/149082930-e80331a1-cbd7-4b38-84e0-11fc1a267115.png" height="250"/>
<div/>
  
## User Proflie

* 登入使用者後點選Account可填寫個人Profile，讓其他人了解你的人格特質、興趣與專業領域等資訊
* 在個人Account中可以建立專案資料成為該專案的Leader
* 首次建立專案於Account頁面點擊Add Project 透過填寫表單建立專案
* 專案Leader具備專案與團隊人員的管理權限
  
<div>
<img src="https://user-images.githubusercontent.com/69707312/149089081-923f8772-6a6e-4e07-bedf-82d61abe5914.png" height="243"/> <img src="https://user-images.githubusercontent.com/69707312/149086848-28ce3a8a-c068-4e09-a4d6-6bd9c2a49906.png" height="243"/>
<div/>
  
## Project
  
* 點選Project 瀏覽目前開放申請加入的所有專案
* 專案內文呈現包含主題、應用類型、技術運用、專案Leader及簡介等資訊
* 若使用者尚未參與專案可對該專案Leader發送申請

<div>
<img src="https://user-images.githubusercontent.com/69707312/149093365-950ac586-4fce-47ce-b425-0710651bc616.png" height="258"/> <img src="https://user-images.githubusercontent.com/69707312/149096065-ed38d6e7-0cf1-47e8-bc9d-98146a9c0169.png" height="258"/>
<div/>
  
## Inbox

* 在Inbox頁面可以查看所有站內訊息的標題列表
* 點選訊息後可查看內文及選擇回復或刪除
  
<div>
<img src="https://user-images.githubusercontent.com/69707312/149091705-30338481-8df0-42e9-8f66-c5b4af489509.png" height="275"/> <img src="https://user-images.githubusercontent.com/69707312/149091107-73607c2b-512d-49ae-bd3a-cd21ba81293b.png" height="275"/>
<div/>
  
## Group Application
* 專案Leader可點選Apply 查看所有收到的申請加入、離開團隊的列表
* 點選申請後選擇同意或拒絕

<div>
<img src="https://user-images.githubusercontent.com/69707312/149094361-d9c1b8b6-964b-43fa-be82-f9ce2f8041f7.png" height="275"/> <img src="https://user-images.githubusercontent.com/69707312/149095343-452e2dff-5fa1-44ef-aed5-6c404a211392.png" height="275"/>
<div/>

