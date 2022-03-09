function addLoginComponent(){
    removeLoginComponent();
    let div = document.getElementById('login-dashboard');

    let label = document.createElement('label');
    label.textContent = "Password: ";
    label.id = 'label-password';

    let password = document.createElement("input");
    password.type = "password";
    password.name = "password";
    password.id = "password";
    label.appendChild(password)
    div.appendChild(label);

    let button = document.createElement('button');
    button.type = "button";
    button.onclick = login.bind(this);
    button.textContent = "Login";
    button.id = 'login';
    div.appendChild(button);

    let error = document.createElement('label');
    error.id = "error";
    div.appendChild(error);
}

function removeLoginComponent(){
    let password = document.getElementById('password');
    if (password)
        password.remove();
    let error = document.getElementById('error');
    if (error)
        error.remove();
    let button = document.getElementById('login');
    if (button)
        button.remove();
    let label = document.getElementById('label-password');
    if (label)
        label.remove();
}

function login(e){
    let password = document.getElementById('password');
    let formData = new FormData()
    formData.append('password', password.value)
    fetch('/session', { method: 'POST', body: formData })
        .then(resp => resp.json())
        .then(data => {
            if (data.error)
                document.getElementById('error').textContent = data.error;
            else{
                localStorage.setItem('appacademycoaches', JSON.stringify(data));
                reloadTree();
                removeLoginComponent();
                addLogoutComponent();
            }
        })
        .catch(error => {
            error.textContent = error.toString();
            console.log(error)
        })
}


function removeLogoutComponent(){
    let button = document.getElementById('logout');
    if (button)
        button.remove();
}

function addLogoutComponent(){
    removeLogoutComponent();
    let options = document.getElementById('options');
    let button = document.createElement('button');
    button.id = "logout";
    button.type = "button";
    button.textContent = "Logout";
    button.onclick = logout.bind(this);
    options.appendChild(button);
}

function logout(){
    controller.abort();
    addLoginComponent();
    localStorage.clear();
    removeLogoutComponent();
    reloadTree();
    clearRoot();
}


window.addEventListener('DOMContentLoaded', e =>{
    if (Object.entries(getTree()).length) {
        addLogoutComponent();
        removeLoginComponent();
    } else {
        addLoginComponent();
        removeLogoutComponent();
    }
})