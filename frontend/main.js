
let domain = "http://127.0.0.1:8000";
let projectUrl = `${domain}/api/projects/`;

let loginBtn = document.getElementById("login-btn");
let logoutBtn = document.getElementById('logout-btn');
let token = localStorage.getItem('token');

if (token)
    loginBtn.remove();
else
    logoutBtn.remove();

logoutBtn.addEventListener('click', (e)=>
{
    e.preventDefault();
    localStorage.removeItem('token');
    window.location = './login.html';
})


let getProjects = () => 
{
    fetch(projectUrl)
        .then(response => response.json())
        .then(data => {
            buildProjects(data);
        })
}

let buildProjects = (projects)=>
{
    let projectsWrapper = document.getElementById('projects--wrapper');
    for (let i=0; i<projects.length; i++)
    {
        let project = projects[i];
        let projectCard = `
            <div class="project--card">
                <img src="${domain}${project.featured_image}"/>
                <div>
                    <div class="card--header">
                        <h3>${project.title}</h3>
                    </div>
                    <p>${project.description.substring(0, 150)}</p>
                </div>

            </div>
        `
        projectsWrapper.innerHTML += projectCard
    }
}

getProjects();
