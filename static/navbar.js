function getTree(){
    let local = localStorage.getItem('appacademycoaches');
    if (local)
        return JSON.parse(local)
    return {};
}

let controller = new AbortController();

function addOption(component, value){
    let option = document.createElement("option");
    option.value = value;
    option.text = value;
    component.appendChild(option)
}


function searchContributions(e){
    controller.abort();
    controller = new AbortController();
    clearRoot();
    let tree = getTree();
    if (Object.entries(tree).length) {
        let coach = document.getElementById('coach')
        let cohort = document.getElementById('cohort');
        let coach_text = coach.options[coach.selectedIndex].text;
        let cohort_text = cohort.options[cohort.selectedIndex].text;

        let results = {};
        if (cohort_text === 'all') {
            Object.entries(tree[coach_text]).forEach(pair => {
                let [cohort, users] = pair;
                results = {...results, ...users};
            });
        } else {
            results = tree[coach_text][cohort_text]
        }

        Object.entries(results).forEach(pair => {
            let div = userContainer();
            let [name, username] = pair;
            addUser(div, name, username);
        })
    }
}


function reloadTree(){
    let tree = getTree();
    let coach = document.getElementById('coach')
    let cohort = document.getElementById('cohort')
    while (cohort.firstChild)
        cohort.removeChild(cohort.firstChild);
    while (coach.firstChild)
        coach.removeChild(coach.firstChild);
    if (Object.entries(tree).length) {
        addOption(coach, 'all');
        Object.keys(tree).forEach(c => {if (c !== 'all') addOption(coach, c)});

        addOption(cohort, "all");
        Object.keys(tree['all']).forEach(c => {if (c !== 'all') addOption(cohort, c)});
        coach.options.selectedIndex = 0;
    }
}


function onCoachChange(){
    document.getElementById("coach").addEventListener('change', (e)=>{
        let tree = getTree();
        if (Object.entries(tree).length) {
            let coach = e.currentTarget.options[e.currentTarget.selectedIndex].text;
            let cohort = document.getElementById('cohort')
            while (cohort.firstChild) {
                cohort.removeChild(cohort.firstChild)
            }

            addOption(cohort, "all");
            Object.keys(tree[coach]).forEach(c => {
                addOption(cohort, c);
            })
        }
    })
}


window.addEventListener('DOMContentLoaded', e=>{
    reloadTree();
    onCoachChange();
})


window.navbar = {
    reloadTree
}