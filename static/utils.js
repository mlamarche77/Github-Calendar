
function authenticate(password){
    let formData = new FormData()
    formData.append('password', password)
    return fetch('/session', { method: 'POST', body: formData })
        .then(resp => resp.json())
}


function hasUpdates(){
    return fetch('/updates', { method: 'GET' })
        .then(resp => resp.json())
        .then(data => {
            let localDate = localStorage.getItem('date');
            console.log(localDate, data.date);
            if (localDate === data.date)
                return false;
            localStorage.setItem('date', data.date);
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
        .then(data => {
            return data
        })
}


