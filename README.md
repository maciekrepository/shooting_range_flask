# Content of project
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Guideline](#guideline)



## General info
<details>
<summary>Click here to see general information about <b>Project</b>!</summary>
<br>
This app is dedicated to manage shooting range competitions. Basic concept looks as following:
<br>
<ol>
  <li>Admin creates competitions and challanges</li>
  <li>User registers account</li>
  <li>User enrolls to challange</li>
  <li>Referee edit results</li>
  <li>User checks results</li>
  </ol>
  Application usage scope is dependend on user logged in profile. Basic user can only enroll to challanges and see results. Referee can moreover edit results. Admin is authorized to create competitions and challanges.
<br>
  The main aim was to do app using concept of microservices and to improve my skills in implementation of various tools with Flask app.

</details>

## Technologies
<details>
<summary>Click here to see information about technologies utilized in the <b>Project</b>!</summary>
<br>
Technologies utilized in the frame of this project are:
<br>
<ul>
  <br>
  <li>Flask</li>
  <p>Main application localized in container 'web' is based on Flask. It allows users to do interaction and it poses as root of whole project. Container 'web1' also consist Flask app and it is dedicated to manage data in ooperation with Postgres database.</p>
  <li>Keycloak</li>
  <p>Keycloak is responsible for management of user profiles. It allows to switch user profiles between basic user, referee or admin. Furthermore it passes to root app info regarding to scope of logged user.</p>
  <li>Postgres</li>
  <p>PostgreSQL database stores data related to competitions, challanges and results.</p>
  <li>Celery</li>
  <p>Celery is responsible for management of mailing queue. Every user during registration process needs to provide emil address. Afterwards messages sent to email addresses of users are processed with utilization of Celery worker.</p>
  <li>Redis</li>
  <p>Redis supports Celery as a message broker.</p>
  <li>Docker</li>
  <p>Docker has been utilized to deploy the app in concept of microservices.</p>
  </ol>
  Application usage scope is dependend on user logged in profile. Basic user can only enroll to challanges and see results. Referee can moreover edit results. Admin is authorized to create competitions and challanges.
<br>
  The main aim was to do app using concept of microservices and to improve my skills in implementation of various tools with Flask app.

</details>

## Setup
<details>
<summary>Click here to see initial steps required to set up application</summary>
<br>
Required action is to create Keycloak admin user. All users are created on behalf of admin user so registration of new users can not be done until Keycloak admin is created.
<br>
Please check guideline section to see how to create Keycloak admin user.
</details>

## Guideline
<details>
<summary>Click here to see how to use the application</summary>
<br>
Required action is to create Keycloak admin user. All users are created on behalf of admin user so registration of new users can not be done until Keycloak admin is created.
<br>
Please check guideline section to see how to create Keycloak admin user.
</details>
