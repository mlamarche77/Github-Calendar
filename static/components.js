function clearUserComponents(){
    let root = document.getElementById("root");
    while (root.firstChild){
        root.removeChild(root.firstChild);
    }
}

function login(e){
    let password = document.getElementById('password');
    localStorage.setItem('pss', password.value);
    loginStatus().then(isLoggedIn => {
        if (isLoggedIn){
            removeLoginComponent();
            addLogoutComponent();
            reloadTree();
        } else {
            loginError("Invalid password");
        }
    })
}

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
    password.onkeyup = enter_key_listener.bind(this);
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

function loginError(message){
    let label = document.getElementById('error');
    label.textContent = "";
    let timeoutId = setTimeout(() => {
        label.textContent = message;
    }, 200);
}

function enter_key_listener(e){
    if (e.keyCode === 13)
        login();
}



function logout(){
    controller.abort();
    addLoginComponent();
    localStorage.clear();
    removeLogoutComponent();
    reloadTree();
    clearRoot();
}

function removeLogoutComponent(){
    let button = document.getElementById('logout');
    if (button)
        button.remove();
    let file = document.getElementById('file');
    if (file)
        file.remove();
    let fileLabel = document.getElementById('fileLabel');
    if (fileLabel)
        fileLabel.remove();
    let fileSpan = document.getElementById('fileSpan');
    if (fileSpan)
        fileSpan.remove();
}

function addLogoutComponent(){
    removeLogoutComponent();
    let options = document.getElementById('options');
    let button = document.createElement('button');
    let file = document.createElement('input');
    let fileLabel = document.createElement('label');

    button.id = "logout";
    button.type = "button";
    button.textContent = "Logout";
    button.onclick = logout.bind(this);
    options.appendChild(button);

    file.type = "file";
    file.id = "file";
    fileLabel.id = "fileLabel"
    fileLabel.htmlFor = "file";
    fileLabel.textContent = "Upload csv file";
    fileLabel.className = "file";
    file.hidden = true;

    file.addEventListener('change', (e) => {
        let file = e.currentTarget.files[0];
        let fileName = file.name;
        fileSpan.textContent = fileName;
        let formData = new FormData();
        formData.append('file', file, fileName);
        fetch('/upload', { method: 'POST', body: formData })
            .then(resp => resp.json())
            .then(data => {
                if (data.error)
                    console.log("Got an error.");
                else{
                    reloadTree();
                }
            })
            .catch(error => {
                error.textContent = error.toString();
                console.log(error);
            })
    })

    options.appendChild(file);
    options.appendChild(fileLabel);
}


function setDefault(){
    let coach = document.getElementById('coach')
    coach.options.selectedIndex = 0;
    let cohort = document.getElementById('cohort');
    cohort.options.selectedIndex = -1;
}


window.addEventListener('DOMContentLoaded', e =>{
    loginStatus().then(isLoggedIn => {
        if (isLoggedIn) {
            addLogoutComponent();
            removeLoginComponent();
        } else {
            addLoginComponent();
            removeLogoutComponent();
        }
    })
})