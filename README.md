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
Create admin user in keycloak:
<br>
<img src="https://user-images.githubusercontent.com/106651068/172534035-a551137a-c5e9-45fb-8ecb-f3a6aa7462a8.png" width=”10%” height=”10%”>
<br>
Enter using credentials admin/password:
<br>
<img src="https://user-images.githubusercontent.com/106651068/172534442-4a397872-ffc0-4a17-97a0-224f708dfe65.png"width=”10%” height=”10%”>
<br>
Add user with credentials admin/password:
<br>
<img src="https://user-images.githubusercontent.com/106651068/172534861-5add6c26-05ff-4bbc-84ec-5ee59f306630.png" height=”10%”>
<br>
<img src="https://user-images.githubusercontent.com/106651068/172534975-6fe5ada5-95f3-4a35-8438-a135bd9773ad.png" height=”10%”>
<br>
<img src="https://user-images.githubusercontent.com/106651068/172535039-329b64fa-99de-43cc-82dd-75460fce9d62.png" height=”10%”>
<br>
Make sure that your configuration looks as following:
<br>
<img src="https://user-images.githubusercontent.com/106651068/172535122-ee6c8623-6f90-4338-bc0b-0e964c7dbedb.png" height=”10%”>
<br>
Now it is time to create admin user and add competitions and challanges. Go to address localhost:5000 and click blue button:
<br>
<img src="https://user-images.githubusercontent.com/106651068/172536041-54fb2d75-178f-4133-be9e-cf5e703225e4.png" height=”10%”>
<br>
Go to register section and fill the form:
<br>
<img src="https://user-images.githubusercontent.com/106651068/172536180-9fcae087-4853-47a3-ae52-7e61365cbabc.png" height=”10%”>
<br>
We need to assign created user to admin role. Come back to keycloak and click hiperlink related to created user:
<br>
<img src="https://user-images.githubusercontent.com/106651068/172536671-6f0064b4-948c-4084-ae0d-3c583876038b.png" height=”10%”>
<br>
Take role admin to assigned roles:
<br>
<img src="https://user-images.githubusercontent.com/106651068/172536964-6956e0f4-5746-41f9-9369-1bca5b06617b.png" height=”10%”>
<br>
Log into app:
<br>
<img src="https://user-images.githubusercontent.com/106651068/172537259-0b8b3343-db8a-43cd-9d3e-ef0ea246614d.png" height=”10%”>
<br>
Create new competition:
<br>
<img src="https://user-images.githubusercontent.com/106651068/172537363-c5f180e6-4e6b-4d18-b721-0a50bdbd15c5.png" height=”10%”>
<br>
<img src="https://user-images.githubusercontent.com/106651068/172537506-4ff56cc3-ac09-4b0c-ad10-41961093efde.png" height=”10%”>
<br>
Create new challange assigned to newly created competition:
<br>
<img src="https://user-images.githubusercontent.com/106651068/172537635-38865b4a-d148-449b-9397-b01a9ef73ed1.png" height=”10%”>
<br>
Come back to main page (localhost:5000) and get into newly created competition:
<br>
<img src="https://user-images.githubusercontent.com/106651068/172541264-33544584-00a9-46d0-ac25-df5488737505.png" height=”10%”>
<br>
Go to register section and register new basic user:
<br>
<img src="https://user-images.githubusercontent.com/106651068/172541485-484ecd1c-670a-45ef-a3a9-96a3b1175cd1.png" height=”10%”>
<br>
Log in as new user:
<br>
<img src="htps://user-images.githubusercontent.com/106651068/172541588-25d52588-7216-4f89-a872-f0710a51915c.png" height=”10%”>
<br>
Enroll to challange:
<br>
<img src="https://user-images.githubusercontent.com/106651068/172542086-a223efc5-f60d-417c-a650-42fa24de91b8.png" height=”10%”>
</details>
