// 'tree' is a global variable declared in the contribution.html file

function clearRoot(){
    let root = document.getElementById("root");
    while (root.firstChild){
        root.removeChild(root.firstChild);
    }
}

function userContainer(){
    let root = document.getElementById("root");
    let div = document.createElement("div");
    div.className = "user-container";
    root.appendChild(div);
    return div;
}

function addUser(div, name, username){
    let data = getData(name, username);
    div.appendChild(data.name);
    div.appendChild(data.url);
    div.appendChild(data.profileImage);
    div.appendChild(data.graphImage);
}

function initalData(name, username){
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

    let top = document.createElement("h1");
    top.textContent = name;

    let bottom = document.createElement("h3");
    bottom.textContent = `GitHub: ${username}`;
    url.appendChild(bottom);

    return {
        name: top,
        graphImage: graphImage,
        url: url,
        profileImage: profileImage
    };
}

function getData(name, username){
    let results = initalData(name, username);
    fetch(`http://127.0.0.1:5000/contribution?username=${username}`)
        .then(response => response.json())
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
        }).catch(error => {
        console.log(error)
        results.graphImage = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/ProhibitionSign2.svg/1024px-ProhibitionSign2.svg.png"
        results.profileImage = "https://icon-library.com/images/unknown-person-icon/unknown-person-icon-4.jpg"
    })
    return results;
}


function addOption(component, value){
    let option = document.createElement("option");
    option.value = value;
    option.text = value;
    component.appendChild(option)
}


function buttonClick(e){
    clearRoot();
    let coach = document.getElementById('coach')
    let cohort = document.getElementById('cohort');
    let coach_text = coach.options[coach.selectedIndex].text;
    let cohort_text = cohort.options[cohort.selectedIndex].text;

    let results = {};
    if (cohort_text === 'all'){
        Object.entries(tree[coach_text]).forEach(pair => {
            let [cohort, users] = pair;
            results = {...results, ...users};
        });
    } else{
        results = tree[coach_text][cohort_text]
    }

    Object.entries(results).forEach(pair => {
        let div = userContainer();
        let [name, username] = pair;
        addUser(div, name, username);
    })
}

function setDefault(){
    let coach = document.getElementById('coach')
    coach.options.selectedIndex = 0;
    let cohort = document.getElementById('cohort');
    cohort.options.selectedIndex = -1;
}
window.addEventListener('DOMContentLoaded', e=>{
    let coach = document.getElementById('coach')
    let coach_text = coach.options[coach.selectedIndex].text;
    let cohort = document.getElementById('cohort')
    while (cohort.firstChild){
        cohort.removeChild(cohort.firstChild)
    }

    addOption(cohort, "all");
    Object.keys(tree[coach_text]).forEach(c => {
      addOption(cohort, c);
    })
    coach.options.selectedIndex = 0;
})
document.getElementById("coach").addEventListener('change', (e)=>{
    let coach = e.currentTarget.options[e.currentTarget.selectedIndex].text;
    let cohort = document.getElementById('cohort')
    while (cohort.firstChild){
        cohort.removeChild(cohort.firstChild)
    }

    addOption(cohort, "all");
    Object.keys(tree[coach]).forEach(c => {
      addOption(cohort, c);
    })
})
