function loginStatus(){
    let password = localStorage.getItem('pss') || '';
    let formData = new FormData()
    formData.append('password', password)
    return fetch('/authenticated', {method: 'POST', body: formData})
        .then(resp => resp.json())
        .then(data => !!data.authenticated)
        .catch(error => false);
}


function authenticate(password){
    let formData = new FormData()
    formData.append('password', password)
    return fetch('/session', { method: 'POST', body: formData })
        .then(resp => resp.json())
}


function hasUpdates(){
    return fetch('/updates', { method: 'GET' })
        .then(resp => resp.json())
        .then(date => {
            let localDate = localStorage.getItem('date');
            if (localDate === date)
                return false;
            localStorage.setItem('date', date);
            return true;
        })
        .catch(error => {
            console.error(error);
            return false;
        })
}


function getContribution(username){
    return fetch(`/contribution?username=${username}`, {signal: controller.signal})
        .then(response => {
            if (response.ok)
                return response.json()
            throw new Error(response.statusText);
        })
        .then(data => data)
}


function upload(e){
    let file = e.currentTarget.files[0];
    let fileSpan = document.getElementById("fileSpan");
    let fileName = file.name;
    let formData = new FormData();
    formData.append('file', file, fileName);
    fetch('/upload', { method: 'POST', body: formData })
        .then(resp => resp.json())
        .then(data => reloadTree())
        .catch(error => {
            fileSpan.textContent = "file not compatible";
        })
}