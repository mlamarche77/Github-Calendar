// 'tree' is a global variable declared in the contribution.html file

function clearRoot(){
    let root = document.getElementById("root");
    while (root.firstChild){
        root.removeChild(root.firstChild);
    }
}

function getTree(){
    let local = localStorage.getItem('appacademycoaches');
    if (local)
        return JSON.parse(local).root
    return {};
}

function userContainer(){
    let root = document.getElementById("root");
    let div = document.createElement("div");
    div.className = "user-container";
    root.appendChild(div);
    return div;
}

function addUser(div, name, username, coach, cohort){
    let data = getData(name, username, coach, cohort);
    div.appendChild(data.name);
    div.appendChild(data.coach);
    div.appendChild(data.url);
    div.appendChild(data.profileImage);
    div.appendChild(data.graphImage);
}

function initalData(name, username, coach, cohort){
    let graphImage = document.createElement("img");
    graphImage.className = "graph-image"
    graphImage.src = "https://media0.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif?cid=ecf05e47qgat0gh5s49q8ymszpqlmseyaqzi10leo077t1td&rid=giphy.gif&ct=g"
    graphImage.width = "50";
    graphImage.height = "50";
    graphImage.style.display = "none";
    graphImage.alt = `${username}_graph`

    let profileImage = document.createElement("img")
    profileImage.className = "profile-image"
    profileImage.src = "https://media0.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif?cid=ecf05e47qgat0gh5s49q8ymszpqlmseyaqzi10leo077t1td&rid=giphy.gif&ct=g"
    profileImage.width = "50";
    profileImage.height = "50";
    profileImage.style.display = "none";
    profileImage.alt = `${username}_profile`

    let url = document.createElement("a");
    url.href = "#";
    url.target = "_blank";

    let top = document.createElement("h1");
    top.textContent = `${name} - ${cohort}`;

    let bottom = document.createElement("h3");
    bottom.textContent = `GitHub: ${username}`;
    url.appendChild(bottom);

    let coachLabel = document.createElement("h4");
    coachLabel.textContent = `Coach: ${coach}`;

    return {
        name: top,
        graphImage: graphImage,
        url: url,
        profileImage: profileImage,
        coach: coachLabel
    };
}

function getData(name, username, coach, cohort){
    let results = initalData(name, username, coach, cohort);
    fetch(`/contribution?username=${username}`, {signal: controller.signal})
        .then(response => {
            if (response.ok)
                return response.json()
            throw new Error(response.statusText);
        })
        .then(data => {
            let graphImage = results.graphImage;
            graphImage.src = data.graph_image;
            graphImage.width = "1000";
            graphImage.height = "150";
            graphImage.style.display = "";
            let profileImage = results.profileImage;
            profileImage.src = data.profile_image;
            profileImage.width = "150";
            profileImage.height = "150";
            profileImage.style.display = "";
            results.url.href = data.url;
        })
        .catch(error => {
            console.log(error)
            results.graphImage.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/ProhibitionSign2.svg/1024px-ProhibitionSign2.svg.png"
            results.profileImage.src = "https://icon-library.com/images/unknown-person-icon/unknown-person-icon-4.jpg"
            results.profileImage.style.display = "";
            results.graphImage.style.display = "";
        })
    return results;
}


function setDefault(){
    let coach = document.getElementById('coach')
    coach.options.selectedIndex = 0;
    let cohort = document.getElementById('cohort');
    cohort.options.selectedIndex = -1;
}